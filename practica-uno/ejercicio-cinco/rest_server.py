from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse

animals = {
    1: {
        "name": "Marlin",
        "species": "Clownfish",
        "gender": "Male",
        "age": 2,
        "weight": 0.3
    },
    2: {
        "name": "Polly",
        "species": "Parrot",
        "gender": "Female",
        "age": 6,
        "weight": 0.2
    },
    3: {
        "name": "Rex",
        "species": "Dog",
        "gender": "Male",
        "age": 3,
        "weight": 6.5
    },
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
    
class AnimalService:
    @staticmethod
    def search_animals_species(species):
        return {id_animal: animal for id_animal, animal in animals.items() if animal["species"] == species}
    
    @staticmethod
    def search_animals_gender(gender):
        return {id_animal: animal for id_animal, animal in animals.items() if animal["gender"] == gender}    

    @staticmethod
    def add_animal(data):
        new_animal_id = max(animals.keys()) + 1 if animals else 1
        animals[new_animal_id] = data
        print("New animal added with ID", new_animal_id)
        return animals
    
    @staticmethod
    def update_animal(animal_id, data):         
        if animal_id in animals:
            animals[animal_id].update(data)
            print("Data updated for animal with ID", animal_id)
            return animals
        return None
    
    @staticmethod
    def delete_animal(animal_id):
        if animal_id in animals:
            animals.pop(animal_id)
            print("Animal with ID", animal_id, "deleted")
            return animals
        return None
        
class RESTRequestHandler(BaseHTTPRequestHandler):
            
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)

        if parsed_path.path == "/animals":
            HTTPResponseHandler.handle_response(self, 200, animals)        
        
        elif self.path.startswith("/animals") and "species" in query_params:
            species = query_params["species"][0]
            animals_species = AnimalService.search_animals_species(species)
            if animals_species:
                HTTPResponseHandler.handle_response(self, 200, animals_species)
            else:
                HTTPResponseHandler.handle_response(self, 204, {})
        
        elif self.path.startswith("/animals") and "gender" in query_params:
            gender = query_params["gender"][0]
            animals_gender = AnimalService.search_animals_gender(gender)
            if animals_gender:
                HTTPResponseHandler.handle_response(self, 200, animals_gender)
            else:
                HTTPResponseHandler.handle_response(self, 204, {})
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_POST(self):
        if self.path == "/animals":
            data = self.read_data()
            animals = AnimalService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animals)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Path not found"})
    
    
    def do_PUT(self):
        if self.path.startswith("/animals/"):
            animal_id = int(self.path.split("/")[-1])
            data = self.read_data()
            animals = AnimalService.update_animal(animal_id, data)
            if animals:
                HTTPResponseHandler.handle_response(self, 200, animals)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal not found"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Path not found"})
                
    def do_DELETE(self):
        if self.path.startswith("/animals/"):
            animal_id = int(self.path.split("/")[-1])
            animals = AnimalService.delete_animal(animal_id)
            if animals:
                HTTPResponseHandler.handle_response(self, 200, animals)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal not found"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Path not found"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Starting web server at http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping the HTTP server...")
        httpd.server_close()
        print("Server stopped successfully.")


if __name__ == "__main__":
    run_server()
