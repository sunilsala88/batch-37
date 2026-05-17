

#gloabl variable
total=10
a='hello world'
def average(list1:list)->float:

    #local variable
    print(a)
    total=0
    for i in list1:
        total=total+i
    avg=total/len(list1)
    return avg

prices=[100,200,300,400,500]
avg_price=average(prices)
print(avg_price)
print(total)
print(a)