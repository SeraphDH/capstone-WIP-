import requests

response = requests.get("http://127.0.0.1:5000/name_gen/elf")
print(response.content)

response = requests.get("http://127.0.0.1:5000/name_gen/blob")
print(response)