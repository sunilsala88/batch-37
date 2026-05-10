

# number= 1
# while True:
#     if number ==10:
#         break
#     print(number)
#     number=number+1

#n=20
# [5,10,15...50...95 100]


multipler=[]
count=20
number=5

#loop should stop when we have 10 numbers in the multipler list
while True:
    if len(multipler)==count:
        break

    multipler.append(number)
    number=number+5    

print(multipler)

#list of 10 fib numbers
#[0,1,1,2,3,5,8,13,21,34]