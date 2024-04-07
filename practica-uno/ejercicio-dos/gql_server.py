from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

class Plant(ObjectType):
    id = Int()
    common_name = String()
    species = String()
    age = Int() 
    height = Int()
    has_fruits = Boolean()

class Query(ObjectType):
    
    plants = List(Plant)
    plants_by_species = List(Plant, species = String())
    plants_by_fruits = List(Plant, has_fruits = Boolean())
    
    # Retrieve all plants
    def resolve_plants(root, info):
        return plants
    
    # Search plants by species
    def resolve_plants_by_species(root, info, species):
        plants_species = list(plant for plant in plants if plant.species == species)
        return plants_species
    
    # Search plants with fruits
    def resolve_plants_by_fruits(root, info, has_fruits):
        plants_fruits = list(plant for plant in plants if plant.has_fruits == has_fruits)
        return plants_fruits
    
# Create a plant
class CreatePlant(Mutation):
    class Arguments:
        common_name = String()
        species = String()
        age = Int() 
        height = Int()
        has_fruits = Boolean()
    
    plant = Field(Plant)
    
    def mutate(root, info, common_name, species, age, height, has_fruits):
        new_plant = Plant(
            id = len(plants)+1,
            common_name = common_name,
            species = species,
            age = age, 
            height = height,
            has_fruits = has_fruits
        )
        plants.append(new_plant)
        
        return CreatePlant(plant = new_plant)

# Update plant information
class UpdatePlant(Mutation):
    class Arguments:
        id = Int()
        age = Int()
        height = Int()
    
    plant = Field(Plant)
    
    def mutate(root, info, id, age, height):
        for plant in plants:
            if plant.id == id:
                plant.age = age
                plant.height = height
                return UpdatePlant(plant = plant)
        return None   
    
# Delete a plant
class DeletePlant(Mutation):
    class Arguments:
        id = Int()
        
    plant = Field(Plant)
    
    def mutate(root, info, id):
        for i, plant in enumerate(plants):
            if plant.id == id:
                plants.pop(i)
                return DeletePlant(plant = plant)
        return None

class Mutations(ObjectType):
    create_plant = CreatePlant.Field()
    update_plant = UpdatePlant.Field()
    delete_plant = DeletePlant.Field()
    
plants = [
    Plant(
        id=1,
        common_name='Apple tree',
        species='Malus domestica',
        age=3,
        height=50,
        has_fruits=True
    ),
    Plant(
        id=2,
        common_name='Pine tree',
        species='Pinus',
        age=10,
        height=200,
        has_fruits=False
    )
]

schema = Schema(query=Query, mutation=Mutations)
    
class GraphQLRequestHandler(BaseHTTPRequestHandler):
    
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
        
    def do_GET(self):
        if self.path == "/graphql":            
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Path not found"})
    
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Path not found"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Starting web server at http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the web server")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
