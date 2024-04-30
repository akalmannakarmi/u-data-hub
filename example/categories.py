import requests

apiKey="755c00bb81b46b63906d8480c9803c01"
url="http://127.0.0.1:5000/api/getCategories"

response = requests.post(url,{"apiKey":apiKey})

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error:{response.status_code}")