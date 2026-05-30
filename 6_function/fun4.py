


def add(x:int,y:int) -> int:
    result=x+y
    return result


def multiply(x:int,y:int) -> int:
    result=x*y
    return result


def operation(a:int,b:int,c:int) -> int:
    result1=add(a,c) #2,4->6
    result2=multiply(result1,b)#6,3->18
    return result2+result1#->18+6->24

answer=operation(2,3,4)
print(answer)
