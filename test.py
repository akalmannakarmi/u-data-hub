class A:
    a = 1
    def add():
        A.a+=1

class B(A):
    def sub():
        A.a-=1


B.sub()
print(A.a)