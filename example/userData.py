import requests

apiKey="3b42dbeaa5d9fd14dffc29208c6e1e06"
url="http://127.0.0.1:5000/api/getUserData"
fields=[1,2,3,4]
userId=[2]

response = requests.post(url,{"apiKey":apiKey,"userId":userId,"fields":fields})

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error:{response.status_code}")