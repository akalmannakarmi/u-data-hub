import json


data={}
with open("file") as f:
	data=json.load(f)

data["ahsld"]="usgaiud"

dataStr=json.dumps(data)

with open("file",'w') as f:
	json.dump(data,f)