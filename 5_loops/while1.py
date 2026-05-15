

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

# fib=[0,1]
# count=10
# while True:
#     if len(fib)==count:
#         break
#     prev=fib[-1]
#     prev_prev=fib[-2]
#     current=prev+prev_prev
#     fib.append(current)
# print(fib)


# list1=[34,25,68,21,11]
# #find the largest number in the list
# largest=list1[0]

# for i in list1:
#     if i>largest:
#         largest=i
# print(largest)


#get fib numbers using for loop
#get lartgest number in the list using while loop


fib=[0,1]
count=10

for i in range(count-2):
    prev=fib[-1]
    prev_prev=fib[-2]
    current=prev+prev_prev
    fib.append(current)

print(fib)
print(list(range(8)))


list1=[34,25,68,21,11]
h=list1[0]
i=0
while True:
    if i==len(list1):
        break
    if list1[i]>h:
        h=list1[i]

    i=i+1
print(h)