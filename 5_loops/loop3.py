

# #type 1

# l1=[45,67,89,23,45]
# for i in l1:
#     print(i)


# #type 2 
# for i in range(10):
#     print('hello world',i)

# #type 3
# l1=[45,67,89,23,45]
# for i in range(len(l1)):
#     print(l1[i])

# #type 4
# stock_prices={'apple':33,'google':44,'microsoft':55,'facebook':66,'amazon':77}

# for i,j in stock_prices.items():
#     print(i,j)

# fib=[0,1]
# number=8
# for i in range(8):
#     prev=fib[-1]
#     prev_prev=fib[-2]
#     next=prev+prev_prev
#     fib.append(next)
# print(fib)

# s1='hello'#'olleh'

print(list(range(5)))
print(list(range(5,10)))
print(list(range(1,10,2)))
print(list(range(4,-1,-1)))

l1=[65,97,89,23,45]
l=[4,3,2,1,0]
print(list(range(4,-1,-1)))
new_list=[]
for i in range(len(l1)-1,-1,-1):
    new_list.append(l1[i])
print(new_list)
