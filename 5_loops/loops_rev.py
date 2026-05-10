

#type 1
l1=[45,67,89,23,45]
for i in l1:
    print(i)

#type 2
for i in range(10):
    print('hello world',i)

#type 3
l2=[45,67,89,23,45]
for i in range(5):
    print(l2[i])

#type 4
stock_prices={'apple':33,'google':44,'microsoft':55,'facebook':66,'amazon':77}
print(list(stock_prices.items()))
for i,j in stock_prices.items():
    print(i,j)