stock_prices={'apple':33,'google':44,'microsoft':55,'facebook':66,'amazon':77}
for i in stock_prices:
    print(i,stock_prices[i])


print(list(stock_prices.keys()))
print(list(stock_prices.values()))
print(list(stock_prices.items()))

for i,j in stock_prices.items():
    print(i,j)

list1=[4,6,9,1,5]
m=list1[0]
for i in list1:
    if i>m:
        m=i

print(m)


v=[200,300,400,500,600]
p=[20,30,40,50,60]