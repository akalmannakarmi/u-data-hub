import json


data={}
with open("file") as f:
	data=json.load(f)

data["ahsld"]="usgaiud"

with open("file",'w') as f:
	json.dump(data,f,indent=4)