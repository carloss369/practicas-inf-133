import requests

url = "http://localhost:8000/patients"
headers = {'Content-type': 'application/json'}

# Consulta: obtener pacientes actuales
get_response = requests.get(url)
print(get_response.text)

# Consulta: agregar un nuevo paciente
new_patient = {
    "id": 456789,
    "first_name": "Gloria",
    "last_name": "Ramirez",
    "age": 20,
    "gender": "Femenino",
    "diagnosis": "Diabetes",
    "physician": "Dr. Gabriela Flores",
}
response = requests.post(url, json=new_patient, headers=headers)
print(response.text)

# Consulta: obtener pacientes actuales después de agregar uno nuevo
response = requests.get(url)
print(response.text)

# Consulta: obtener información de un paciente por ID
id = 456789
response_id = requests.get(f"{url}/{id}")
print(response_id.text)

# Consulta: obtener pacientes con diagnóstico específico (Diabetes)
diagnosis = "Diabetes"
response_diagnosis = requests.get(f"{url}/?diagnosis={diagnosis}")
print(response_diagnosis.text)

# Consulta: obtener pacientes atendidos por un doctor específico
physician = "Dr. Pedro Perez"
response_physician = requests.get(f"{url}/?physician={physician}")
print(response_physician.text)

# Consulta: actualizar información de un paciente por ID
id = 456789
update_patient = {
    "age": 22,
    "physician": "Dr. Pedro Perez",
}
response_update = requests.put(f"{url}/{id}", json=update_patient)
print(response_update.text)

# Consulta: eliminar un paciente por ID
id = 8464559
response_delete = requests.delete(f"{url}/{id}")
print(response_delete.text)

# Consulta: obtener pacientes actuales después de eliminar uno
response_current = requests.get(url)
print(response_current.text)
