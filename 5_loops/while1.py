

# number= 1
# while True:
#     if number ==10:
#         break
#     print(number)
#     number=number+1

#n=20
# [5,10,15...50...95 100]


# multipler=[]
# count=20
# number=5

# #loop should stop when we have 10 numbers in the multipler list
# while True:
#     if len(multipler)==count:
#         break

#     multipler.append(number)
#     number=number+5    

# print(multipler)

#list of 10 fib numbers
#[0,1,1,2,3,5,8,13,21,34]

fib=[0,1]
count=10
while True:
    if len(fib)==count:
        break
    prev=fib[-1]
    prev_prev=fib[-2]
    current=prev+prev_prev
    fib.append(current)
print(fib)


lisst1=[34,25,68,21,11,45,32]
#find the largest number in the list