#class-> class is a blueprint of an object
#object-> object is an instance of a class
#pass-> pass is a placeholder for future code. It is used when we want to create a class or a function but we don't want to write the code for it yet.
#attribute-> attribute is a variable that is associated with an object. It is used to store data about the object.
#class attribute-> class attribute is a variable that is associated with a class. It is shared by all instances of the class.
#object attribute-> object attribute is a variable that is associated with an object. It is unique to each instance of the class.
#method-> method is a function that is associated with an object. It is used to perform some action on the object.
#__init__-> __init__ is a special method that is called when an object is created. It is used to initialize the object.
#it is called contructor in other programming languages.
def demo(x,y):
    return x+y

a=demo(10,20)
print(a)
b=demo(10,30)
print(b)

print('some random line')


class Student:
    school_name='ABC School' #class attribute
    dress_code='Uniform' #class attribute

    def __init__(self,n,a,e):
        self.name=n #object attribute
        self.age=a #object attribute
        self.email=e #object attribute

    def introduce(self):
        intro= f'My name is {self.name} and I am {self.age} years old. My email is {self.email} and I study in {self.school_name}.'
        return intro

s1=Student('John',20,'john@example.com')
print(s1)
print(s1.introduce())
s2=Student('Jane',22,'jane@example.com')
print(s2)
print(s2.introduce())



