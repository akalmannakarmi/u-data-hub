from data import dbBasic as db


def test():
	passed=0
	failed=0

	# Add User
	try:
		db.addUser(89986946,"TestUserTag")
		passed+=1
	except Exception as e:
		print("Add User Failed",e)
		failed+=1
	
	print(f"Basic Module Testing:{passed}/{passed+failed}")
	return (passed,failed)