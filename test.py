from test import admin,api,basic,user

passed=0
failed=0

print("Testing Admin Module...")
(p,f)=admin.test()
passed+=p
failed+=f

print("Testing API Module...")
(p,f)=api.test()
passed+=p
failed+=f

print("Testing Basic Module...")
(p,f)=basic.test()
passed+=p
failed+=f

print("Testing User Module...")
(p,f)=user.test()
passed+=p
failed+=f


print(f"Testing Result:{passed}/{passed+failed}")