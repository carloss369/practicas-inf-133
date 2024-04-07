from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
from urllib import parse as urlparse

class Juego:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.juegos = []
        return cls._instance

class JuegoResult:
    def __init__(self, element):
        self.id = len(Juego()._instance.juegos) + 1
        self.element = element
        self.element_server = random.choice(["piedra", "papel", "tijera"])
        self.resultado = self.calcular_res()

    def calcular_res(self):
        if self.element == self.element_server:
            return "empato"
        elif (self.element == "piedra" and self.element_server == "tijera") or \
             (self.element == "tijera" and self.element_server == "papel") or \
             (self.element == "papel" and self.element_server == "piedra"):
            return "gano"
        else:
            return "perdio"
        
    def to_dict(self):
        return {
            "id": self.id,
            "elemento": self.element,
            "elemento_servidor": self.element_server,
            "resultado": self.resultado
        }

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class JuegoHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            data = HTTPResponseHandler.handle_reader(self)
            new_juego = JuegoResult(data["elemento"])
            Juego()._instance.juegos.append(new_juego)
            HTTPResponseHandler.handle_response(self, 201, new_juego.to_dict())
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)
        if self.path == "/partidas":
            juegos_data = [juego.to_dict() for juego in Juego()._instance.juegos]
            HTTPResponseHandler.handle_response(self, 200, juegos_data)
        elif self.path.startswith("/partidas") and "resultado" in query_params:
            result = query_params["resultado"][0]
            if result in ["gano", "perdio", "empato"]:
                filtered_juegos = [juego.to_dict() for juego in Juego()._instance.juegos if juego.resultado == result]
                HTTPResponseHandler.handle_response(self, 200, filtered_juegos)
            else:
                HTTPResponseHandler.handle_response(self, 400, {"Error": "Resultado no válido"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, JuegoHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()