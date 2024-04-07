import requests

url = "http://localhost:8000/animals"

get_response = requests.get(url)
print(get_response.text)

new_animal = {
    "name": "Sharky",
    "species": "Fish",
    "gender": "Male",
    "age": 4,
    "weight": 30.2
}
response = requests.post(url, json=new_animal)
print(response.text)

print("--- Current Animals ---")
response = requests.get(url)
print(response.text)

species = "Fish"
response_species = requests.get(f"{url}/?species={species}")
print(response_species.text)

gender = "Female"
response_gender = requests.get(f"{url}/?gender={gender}")
print(response_gender.text)

id = 1
update_animal = {
    "name": "Maximus",
    "age": 5
}
response = requests.put(f"{url}/{id}", json=update_animal)
print(response.text)

id = 2
response_delete = requests.delete(f"{url}/{id}")
print(response_delete.text)
