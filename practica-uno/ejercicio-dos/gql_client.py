import json
import requests

url = 'http://localhost:8000/graphql'

# Create a plant
print("Create a plant")
create_mutation = """
mutation {
    createPlant(commonName: "Orange tree", species: "Citrus sinensis", age: 5, height: 80, hasFruits: true) {
        plant {
            id
            commonName
            species
            age
            height
            hasFruits
        }
    }
}
"""
response = requests.post(url, json={'query': create_mutation})
print(response.text)

# List all plants
print("List all plants")
list_query = """ 
{
    plants {
        id
        commonName
        species
        age
        height
        hasFruits
    }
}
"""
response = requests.get(url, json={'query': list_query})
print(response.text)

# Search plants by species
print("Search plants by species")
species_query = """ 
{
    plantsBySpecies(species:"Pinus") {
        id
        commonName
        species
        age
        height
        hasFruits
    }
}
"""
response = requests.get(url, json={'query': species_query})
print(response.text)

# Search plants with fruits
print("Search plants with fruits")
fruits_query = """ 
{
    plantsByFruits(hasFruits:true) {
        id
        commonName
        species
        age
        height
        hasFruits
    }
}
"""
response = requests.get(url, json={'query': fruits_query})
print(response.text)

# Update plant information
print("Update a plant")
update_mutation = """
mutation {
    updatePlant(id: 3, age: 6, height: 100) {
        plant {
            id
            commonName
            species
            age
            height
            hasFruits
        }
    }
}
"""
response = requests.post(url, json={'query': update_mutation})
print(response.text)

print("Updated list")
response = requests.get(url, json={'query': list_query})
print(response.text)

# Delete a plant
print("Delete a plant")
delete_mutation = """
mutation {
    deletePlant(id: 2) {
        plant {
            id
            commonName
            species
            age
            height
            hasFruits
        }
    }
}
"""
response = requests.post(url, json={'query': delete_mutation})
print(response.text)

print("Updated list")
response = requests.get(url, json={'query': list_query})
print(response.text)
