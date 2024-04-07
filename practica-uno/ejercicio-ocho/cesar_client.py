import requests

url = "http://localhost:8000/messages"

new_message = {
    "content": "Hello world"
}
response = requests.post(url, json=new_message)
print(response.text)

new_message = {
    "content": "Goodbye world"
}
response = requests.post(url, json=new_message)
print(response.text)

response = requests.get(url)
print(response.text)

id = 2
response_id = requests.get(f"{url}/{id}")
print(response_id.text)

id = 2
update_message = {
    "content": "Let's play"
}
response = requests.put(f"{url}/{id}", json=update_message)
print(response.text)

id = 1
response = requests.delete(f"{url}/{id}")
print(response.text)

response = requests.get(url)
print(response.text)
