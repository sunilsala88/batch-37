#class-> class is a blueprint of an object
#object-> object is an instance of a class
#pass-> pass is a placeholder for future code. It is used when we want to create a class or a function but we don't want to write the code for it yet.


def demo(x,y):
    return x+y

a=demo(10,20)
print(a)
b=demo(10,30)
print(b)

print('some random line')


class Student:
    pass

s1=Student()
print(s1)
s2=Student()
print(s2)