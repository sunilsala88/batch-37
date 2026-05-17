
#1. Positional Arguments
def greet_user(name, age):
    print(f"Hello {name}, you are {age} years old.")

greet_user( 25,"Alice")

#  2. Default Arguments

def greet(name="User"):
    print("Hello", name)

greet()       # Uses default
greet("Niel") # Uses passed value


# 3. Keyword Arguments

def display_info(name, city):
    print(f"{name} lives in {city}.")

display_info('ravi','mumbai')
display_info(city="Mumbai", name="Ravi")



#fstring

name='sunil'
age=35
l1=[1,2,3,4,5]
print('hello my name is '+name+' and my age is '+str(age))
print(f"hello my name is {name} and my age is {l1}")