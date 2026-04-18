#iteration,looping
prices=[33,44,55,66,77,66]

#type 1 loop
total=0
for p in prices:
    # print(p)
    total=total+p

print(total)

print('average price is', total/len(prices))

new_list=[]

for p in prices:
    new_list.append(p**2)

print(new_list)

#type 2 loop
print('hello world')

print(list(range(100)))

for i in range(10):
    print('hello world',i)


#type 3 loop
new_list=[]
for i in range(len(prices)):
    new_list.append(prices[i]**2)
print(new_list)