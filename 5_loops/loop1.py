prices=[33,44,55,66,77]


total=0
for p in prices:
    # print(p)
    total=total+p

print(total)

print('average price is', total/len(prices))