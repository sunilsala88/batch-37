#class-> class is a blueprint of an object
#object-> object is an instance of a class
#pass-> pass is a placeholder for future code. It is used when we want to create a class or a function but we don't want to write the code for it yet.
#attribute-> attribute is a variable that is associated with an object. It is used to store data about the object.
#class attribute-> class attribute is a variable that is associated with a class. It is shared by all instances of the class.
#object attribute-> object attribute is a variable that is associated with an object. It is unique to each instance of the class.
#method-> method is a function that is associated with an object. It is used to perform some action on the object.
#__init__-> __init__ is a special method that is called when an object is created. It is used to initialize the object.
#it is called contructor in other programming languages.
#what is self-> self is a reference to the current instance of the class. It is used to access the attributes and methods of the class in python.


# def demo(x,y):
#     return x+y

# a=demo(10,20)
# print(a)
# b=demo(10,30)
# print(b)

# print('some random line')


# class Student:
#     school_name='ABC School' #class attribute
#     dress_code='Uniform' #class attribute

#     def __init__(self,n,a,e):
#         self.name=n #object attribute
#         self.age=a #object attribute
#         self.email=e #object attribute

#     def introduce(self):
#         intro= f'My name is {self.name} and I am {self.age} years old. My email is {self.email} and I study in {self.school_name}.'
#         return intro

# s1=Student('John',20,'john@example.com')
# print(s1)
# print(s1.introduce())
# s2=Student('Jane',22,'jane@example.com')
# print(s2)
# print(s2.introduce())



#trading class
class Trading:
    broker_name='ibkr'
    stock_prices={'AAPL':150,'GOOGL':2800,'AMZN':3400,'MSFT':300,'TSLA':700}
    def __init__(self,name,id,balance):
        self.name=name
        self.id=id
        self.balance=balance
        self.portfolio={}
    
    def display_portfolio(self):
        # print(f"trader name: {self.name}")
        # print(f"trader id: {self.id}")
        # print(f"balance: {self.balance}")
        print("portfolio:")
        for stock,price in self.portfolio.items():
            print(f"{stock}: {price} ")
        print('-----------------------------')
    
    def buy_stock(self,stock):
        price=self.stock_prices.get(stock)
        if price and self.balance>=price:
            self.balance-=price
            self.portfolio.update({stock:price})
        else:
            print("insufficient balance or invalid stock")
    
    def sell_stock(self,stock):
        price=self.stock_prices.get(stock)
        if price and stock in self.portfolio:
            self.balance+=price
            self.portfolio.pop(stock)
        else:
            print("stock not in portfolio or invalid stock")

t1=Trading('tom',12345,10000)
t1.buy_stock('AAPL')
Trading.buy_stock(t1,'GOOGL')
t1.display_portfolio()

