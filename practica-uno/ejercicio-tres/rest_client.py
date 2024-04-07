import requests

url = "http://localhost:8000/pacientes"

get_response = requests.get(url)
print(get_response.text)

nuevo_paciente = {
    "ci": 123456,
    "nombre": "Tatiana",
    "apellido": "Quispe",
    "edad": 25,
    "genero": "Femenino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Perez",
}
response = requests.post(url, json=nuevo_paciente)
print(response.text)

response = requests.get(url)
print(response.text)

ci = 123456
response_ci = requests.get(f"{url}/{ci}")
print(response_ci.text)

diagnostico = "Diabetes"
response2 = requests.get(f"{url}/?diagnostico={diagnostico}")
print(response2.text)

doctor = "Pedro Perez"
response2 = requests.get(f"{url}/?doctor={doctor}")
print(response2.text)

ci = 123456
actualizacion_paciente = {
    "edad": 24,
    "doctor": "Pedro Perez",
}
response = requests.put(f"{url}/{ci}", json=actualizacion_paciente)
print(response.text)

ci = 123456
response = requests.delete(f"{url}/{ci}")
print(response.text)
