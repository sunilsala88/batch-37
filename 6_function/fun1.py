


# total=0
# prices=[100,200,300,400,500]

# for price in prices:
#     total=total+price
# average=total/len(prices)
# print(average)


def average(list1:list)->float:
    total=0
    for i in list1:
        total=total+i
    avg=total/len(list1)
    return avg

prices=[100,200,300,400,500]
avg_price=average(prices)
print(avg_price)


def add_number(num1:int,num2:int)->int:
    sum=num1+num2
    return sum

result=add_number(10,20)
print(result)




def get_fibonacci(n:int)->list:
    fib=[0,1]
    last=1
    second_last=0
    for i in range(n-2):
        current=last+second_last
        fib.append(current)
        second_last=last
        last=current
        
    return (fib)


fib_numbers=get_fibonacci(20)
print(fib_numbers)

#function to get the largest number in the list
#create a rev function which takes a list as input and returns the reversed list as output

def get_largest(list1:list)->int:
    max=list1[0]
    for i in list1:
        if i>max:
            max=i
    return max

largest_number=get_largest([34,25,68,21,11])
print(largest_number)

def rev_list(list1:list)->list:
    rev_list=[]
    i=len(list1)-1
    while True:
        if i<0:
            break
        rev_list.append(list1[i])
        i=i-1
    return rev_list

reversed_list=rev_list([34,25,68,21,11])
print(reversed_list)


#take stock prices as input and return portfolio value as output
def get_portfolio(stock_prices:dict)->dict:
    
    portfolio={}
    while True:
        name=input('enter stock name(type q to quit):')
        
        if name=='q':
            break
        if name=='msft':
            print('msft is not available try some other stock')
            continue
        price=stock_prices.get(name)
        print(name,price)
        # if price is not None:
        if price :
            portfolio.update({name:price})
        else:
            print('stock not found')
    return portfolio


stock_prices={'amzn':500,'msft':200,'goog':1000,'tsla':300,'nifty':600}
portfolio=get_portfolio(stock_prices)
print(portfolio)