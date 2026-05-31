


d1=open('/Users/algo trading 2026/batch 37/7_file_exception/demo1.txt','r')
d=d1.read()
print(d)
d1.close()

with open('/Users/algo trading 2026/batch 37/7_file_exception/demo1.txt','r') as d1:
    d=d1.read()
    print(d)