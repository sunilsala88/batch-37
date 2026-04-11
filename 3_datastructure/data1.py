n1=90
f1=4.4
s1='66'
b1=True
print(type(n1))
print(type(f1))
print(type(s1)) 
print(type(b1))
#list
#dictionay
#tuple
#set

l1=[33,44,55,66,77]
print(l1)
print(type(l1))

print(l1[0])
print(l1[-1])
print(l1[1:3])

#add element in list
l1.append(88)
print(l1)

l1.insert(2,99)
print(l1)

#remove element from list
l1.remove(33)
print(l1)

l1.pop(2)
print(l1)

del l1[-1]
print(l1)

#update element in list
l1[1]=100
print(l1)

#index
print(l1.index(66))