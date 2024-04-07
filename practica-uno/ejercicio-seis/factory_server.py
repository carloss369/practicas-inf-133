from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse
animales = {}
#Clase animal
class Animal:
    def __init__(self, animal_type, nombre, especie, genero, edad, peso):
        self.animal_type = animal_type
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso
#Especies
class Mamifero(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("Mamifero", nombre, especie, genero, edad, peso)
class Ave(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("Ave", nombre, especie, genero, edad, peso)
class Reptil(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("Reptil", nombre, especie, genero, edad, peso)
class Anfibio(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("Anfibio", nombre, especie, genero, edad, peso)
class Pez(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("Pez", nombre, especie, genero, edad, peso)

class ZooFactory:
    @staticmethod
    def create_animal(animal_type, nombre, especie, genero, edad, peso):
        if animal_type == "Mamifero":
            return Mamifero(nombre, especie, genero, edad, peso)
        elif animal_type == "Ave":
            return Ave(nombre, especie, genero, edad, peso)
        elif animal_type == "Reptil":
            return Reptil(nombre, especie, genero, edad, peso)
        elif animal_type == "Anfibio":
            return Anfibio(nombre, especie, genero, edad, peso)
        elif animal_type == "Pez":
            return Pez(nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")

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
    
class ZooService:
    
    def __init__(self):
        self.factory = ZooFactory()
        
    def add_animal(self, data):
        animal_type = data.get("animal_type", None)
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero =data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)
        delivery_animales = self.factory.create_animal(animal_type, nombre, especie, genero, edad, peso)
        id_nuevo = max(animales.keys()) + 1 if animales else 1
        animales[id_nuevo] = delivery_animales
        
        return delivery_animales
    
    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def buscar_animales_especie(self, especie):
        return {index: animal.__dict__ for index, animal in animales.items() if animal.especie == especie}
    
    def buscar_animales_genero(self, genero):
        return {index: animal.__dict__ for index, animal in animales.items() if animal.genero == genero} 
    
    def update_animal(self, id_animal, data):
        if id_animal in animales:
            animal = animales[id_animal]
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            if edad:
                animal.edad = edad
            if peso:
                animal.peso = peso
            return animal
        return None
    
    def delete_animal(self, id_animal):
        if id_animal in animales:
            animales.pop(id_animal)
            return {"message": "Animal eliminado correctamente"}
        else:
            return {"error": "Animal no encontrado"}


class DeliveryRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.delivery_service = ZooService()
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)
        if parsed_path.path == "/animales":
            data = self.delivery_service.list_animales()
            HTTPResponseHandler.handle_response(self, 200, data)        
        elif self.path.startswith("/animales") and "especie" in query_params:
            especie = query_params["especie"][0]
            animales_especie = self.delivery_service.buscar_animales_especie(especie)
            if animales_especie:
                HTTPResponseHandler.handle_response(self, 200, animales_especie)
            else:
                HTTPResponseHandler.handle_response(self,204,{})
        elif self.path.startswith("/animales") and "genero" in query_params:
            genero = query_params["genero"][0]
            animales_genero = self.delivery_service.buscar_animales_genero(genero)
            if animales_genero:
                HTTPResponseHandler.handle_response(self, 200, animales_genero)
            else:
                HTTPResponseHandler.handle_response(self,204,{})
        
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPResponseHandler.handle_reader(self)
            response_data = self.delivery_service.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            response_data = self.delivery_service.update_animal(id, data)
            if response_data:
                HTTPResponseHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            deleted_animal = self.delivery_service.delete_animal(id)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, deleted_animal)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, DeliveryRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
            print("\nDeteniendo el servidor HTTP...")
            httpd.server_close()
            print("Servidor detenido correctamente.")
if __name__ == "__main__":
    run_server()