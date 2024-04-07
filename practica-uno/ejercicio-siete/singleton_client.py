import requests
import json

url = "http://localhost:8000/partidas"

player_eleccion = [
    {"elemento": "piedra"},
    {"elemento": "piedra"},
    {"elemento": "papel"},
    {"elemento": "tijera"},]

for eleccion in player_eleccion:
    response = requests.post(url, json=eleccion)
    print("Respuesta del servidor:")
    print(response.text)
response = requests.get(url)
print(response.text)

resultado = "gano"
response = requests.get(f"{url}?resultado={resultado}")
print(response.text)

resultado = "perdio"
response = requests.get(f"{url}?resultado={resultado}")
print(response.text)

resultado = "empato"
response = requests.get(f"{url}?resultado={resultado}")
print(response.text)