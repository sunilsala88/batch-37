
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



#4. Variable-Length Arguments (*args and **kwargs)

# ➤ *args → Multiple positional arguments

def add_numbers(*args):
    print(args)
    return sum(args)

print(add_numbers(1, 2, 3, 4,5))


def print_details(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_details(name="Anil", age=30, country="India", email="some@gmail.com")


#lamda
def square(x):
    return x**2
s=square(5)
print(s)

square = lambda x: x**2
print(square(5))