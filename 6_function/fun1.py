


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