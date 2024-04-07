from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse


pacientes = [
    {
        "ci": 1234567,
        "nombre": "María",
        "apellido": "Martínez",
        "edad": 25,
        "genero": "Femenino",
        "diagnostico": "Resfriado",
        "doctor": "Doctor Juan Rodríguez", 
    },
    {
        "ci": 9876543,
        "nombre": "Juan",
        "apellido": "Pérez",
        "edad": 35,
        "genero": "Masculino",
        "diagnostico": "Hipertensión",
        "doctor": "Doctora Laura Gómez",
    },    
    {
       "ci": 4567890,
        "nombre": "Luisa",
        "apellido": "Hernández",
        "edad": 40,
        "genero": "Femenino",
        "diagnostico": "Artritis",
        "doctor": "Doctor Roberto Sánchez",
    }, 
]


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
#Aplicando S de Solid
class PacienteService:
    @staticmethod
    def buscar_paciente_ci(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci), None)

    @staticmethod
    def buscar_paciente_diagnostico(diagnostico):
        return [paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico]
    
    @staticmethod
    def buscar_paciente_doctor(doctor):
        return [paciente for paciente in pacientes if paciente["doctor"] == doctor]
    
    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def update_paciente(ci, data):
        paciente = PacienteService.buscar_paciente_ci(ci)
        if paciente:
            indice = pacientes.index(paciente)
            pacientes[indice].update(data)
            return pacientes
        else:
            return None
    
    @staticmethod
    def delete_paciente(ci):
        for paciente in pacientes:
            if paciente["ci"] == ci:
                pacientes.remove(paciente)
                return pacientes
        return None
class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)
        if parsed_path.path == "/pacientes":            
            HTTPResponseHandler.handle_response(self, 200, pacientes) 
        elif self.path.startswith("/pacientes") and "diagnostico" in query_params:    
            diagnostico = query_params["diagnostico"][0]
            pacientes_diabetes = PacienteService.buscar_paciente_diagnostico(diagnostico)                
            if pacientes_diabetes:
                HTTPResponseHandler.handle_response(self, 200, pacientes_diabetes)
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        elif self.path.startswith("/pacientes") and "doctor" in query_params:            
            doctor = query_params['doctor'][0]
            pacientes_doctor = PacienteService.buscar_paciente_doctor(doctor)
            HTTPResponseHandler.handle_response(self, 200, pacientes_doctor)
        elif self.path.startswith("/pacientes/"):            
            ci = int(self.path.split("/")[-1])
            response_data = PacienteService.buscar_paciente_ci(ci)
            HTTPResponseHandler.handle_response(self, 200, response_data)
        else:
                HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_POST(self):        
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacienteService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_PUT(self):        
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacienteService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})
    def do_DELETE(self):        
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = PacienteService.delete_paciente(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
            print("\nDeteniendo el servidor HTTP...")
            httpd.server_close()
            print("Servidor detenido correctamente.")
if __name__ == "__main__":
    run_server()