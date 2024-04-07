import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

nuevo_animal = {
        "animal_type": "Mamífero",
    "nombre": "Elefante africano",
    "especie": "Loxodonta africana",
    "genero": "Hembra",
    "edad": 15,
    "peso": 5000
}
respuesta = requests.post(url=url, json=nuevo_animal, headers=headers)
print(respuesta.text)

nuevo_animal = {
        "animal_type": "Ave",
    "nombre": "Halcón peregrino",
    "especie": "Falco peregrinus",
    "genero": "Macho",
    "edad": 8,
    "peso": 1.5
}
respuesta = requests.post(url=url, json=nuevo_animal, headers=headers)
print(respuesta.text)

nuevo_animal = {
         "animal_type": "Reptil",
    "nombre": "Cocodrilo del Nilo",
    "especie": "Crocodylus niloticus",
    "genero": "Macho",
    "edad": 20,
    "peso": 900
}
respuesta = requests.post(url=url, json=nuevo_animal, headers=headers)
print(respuesta.text)

nuevo_animal = {
         "animal_type": "Anfibio",
    "nombre": "Rana arborícola",
    "especie": "Hyla cinerea",
    "genero": "Hembra",
    "edad": 2,
    "peso": 0.05
}
respuesta = requests.post(url=url, json=nuevo_animal, headers=headers)
print(respuesta.text)

nuevo_animal = {
        "animal_type": "Pez",
    "nombre": "Atún rojo",
    "especie": "Thunnus thynnus",
    "genero": "Macho",
    "edad": 6,
    "peso": 400
}
respuesta = requests.post(url=url, json=nuevo_animal, headers=headers)
print(respuesta.text)

respuesta = requests.get(url=url)
print(respuesta.text)

especie = "Panthera leo"
respuesta_especie = requests.get(f"{url}/?especie={especie}")
print(respuesta_especie.text)

genero = "Hembra"
respuesta_genero = requests.get(f"{url}/?genero={genero}")
print(respuesta_genero.text)

id = 1
actualizacion_animal = {
    "edad": 6,
    "peso": 250
}
respuesta = requests.put(f"{url}/{id}", json=actualizacion_animal)
print(respuesta.text)

id = 2
respuesta_eliminar = requests.delete(f"{url}/{id}")
print(respuesta_eliminar.text)

respuesta = requests.get(url=url)
print(respuesta.text)
