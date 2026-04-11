
stock_price={'tsla':100,'apple':200,'google':300,'meta':400}
#key:int,float,string,bool
#value:any data type

#access
print(stock_price['tsla'])
print(stock_price.get('apple'))

#add
stock_price['amazon']=500
stock_price.update({'microsoft':600})
print(stock_price)


#update
stock_price['tsla']=150 
stock_price.update({'google':400})
print(stock_price)

#delete
del stock_price['meta']
stock_price.pop('google')
print(stock_price)

