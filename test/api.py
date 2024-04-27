from data import dbAPI as db

id = 517895693865
key = ""

def req():
	from data import dbBasic
	from data import dbAdmin
	from data import dbUser
	global id,key

	key = dbBasic.addUser(id,"UserTag")
	dbAdmin.addCategory("Test")
	dbAdmin.addField("Test","Field",1,1)
	dbUser.saveInfo(id,"Test",{"Field":"Value"},{"Field":1})


def test():
	global id,key
	passed=0
	failed=0

	try:
		req()
	except Exception as e:
		print("API Module failed to Load Requirements",e)

	# Change API Key
	try:
		key = db.changeKey(id)
		passed+=1
	except Exception as e:
		print("Failed to Change Key",e)
		failed+=1

	# Validate API Key
	try:
		result = db.validAuth(key)
		if not result:
			raise BaseException("Invalid Auth Key")
		passed+=1
	except Exception as e:
		print("Failed to Change Key",e)
		failed+=1
	
	# Get stats
	try:
		db.getStats(key,["Field",])
		passed+=1
	except Exception as e:
		print("Failed to Get Stats",e)
		failed+=1
	
	# Get User Info
	try:
		db.getUserInfo(id,key,["Field",])
		passed+=1
	except Exception as e:
		print("Failed to Get User Info",e)
		failed+=1
	
	print(f"API Module Testing:{passed}/{passed+failed}")
	return (passed,failed)