from data import dbUser as db

id = 9858635638

def req():
	from data import dbBasic
	from data import dbAdmin
	global id,key

	dbBasic.addUser(id,"TestUser")
	dbAdmin.addCategory("Test1")
	dbAdmin.addField("Test1","Field1",1,1)


def test():
	global id,key
	passed=0
	failed=0

	try:
		req()
	except Exception as e:
		print("User Module failed to Load Requirements",e)

	# Find Users
	try:
		db.findUsers("User")
		passed+=1
	except Exception as e:
		print("Failed to Find Users",e)
		failed+=1

	# Get User Data
	try:
		db.getUserData(id,id)
		passed+=1
	except Exception as e:
		print("Failed to Get User Data",e)
		failed+=1
	
	# Get My Data
	try:
		db.getMyData(id)
		passed+=1
	except Exception as e:
		print("Failed to Get My data",e)
		failed+=1
	
	# Get Save Info
	try:
		db.saveInfo(id,"Test1",{"Field1":"Value"},{"Field1":1})
		passed+=1
	except Exception as e:
		print("Failed to Save Info",e)
		failed+=1
	
	# Get Remove Info
	try:
		db.removeInfo(id,"Test1",["Field1",])
		passed+=1
	except Exception as e:
		print("Failed to Remove Info",e)
		failed+=1


	print(f"User Module Testing:{passed}/{passed+failed}")
	return (passed,failed)