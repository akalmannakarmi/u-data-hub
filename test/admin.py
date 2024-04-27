from data import dbAdmin as db


def test():
	passed=0
	failed=0

	# Add Category
	try:
		db.addCategory("Test")
		passed+=1
	except Exception as e:
		print("Add Category Failed")
		failed+=1
	
	# Edit Category
	try:
		db.editCategory("Test1","Test")
		passed+=1
	except Exception as e:
		print("Edit Category Failed")
		failed+=1
	
	# Add Field
	try:
		db.addField("Test1","Field",1,1)
		passed+=1
	except Exception as e:
		print("Add Field Failed")
		failed+=1
	
	# Edit Field
	try:
		db.editField(1,"Field1",3,0)
		passed+=1
	except Exception as e:
		print("Edit Field Failed")
		failed+=1
	
	# Remove Field
	try:
		db.removeField(1)
		passed+=1
	except Exception as e:
		print("Remove Field Failed")
		failed+=1
	
	# Remove Category
	try:
		db.removeCategory("Test1")
		passed+=1
	except Exception as e:
		print("Remove Category Failed")
		failed+=1
	
	print(f"Admin Module Testing:{passed}/{passed+failed}")
	return (passed,failed)