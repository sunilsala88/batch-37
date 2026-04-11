
#tuple
t1=(33,44,55,66,77)
print(t1)
print(type(t1))

print(t1[0])
print(t1[-1])
print(t1[1:3])

print(t1.index(55))
#tuple is immutable
#we use ( ) for tuple

#set
s1={33,44,55,66,77,44}
print(s1)

s1.add(88)
print(s1)


s1.pop()
print(s1)



s2='ts.la-100'
print(s2.split('.'))

l1=['tsla-100','apple-200','google-300']
z='='.join(l1)
print(z)