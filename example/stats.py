import requests

apiKey="d2e2755722ffd69091d42650766b63af"
url="http://127.0.0.1:5000/api/getStats"
fields=[1,2]

response = requests.post(url,{"apiKey":apiKey,"fields":fields})

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error:{response.status_code}")