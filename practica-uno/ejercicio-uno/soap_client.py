from zeep import Client

client = Client(
    "http://localhost:8000/"
)

result1 = client.service.Suma(15,11)
print(result1)
result2 = client.service.Resta(13,2)
print(result2)
result3 = client.service.Multiplicacion(5,6)
print(result3)
result4 = client.service.Division(10,2)
print(result4)
