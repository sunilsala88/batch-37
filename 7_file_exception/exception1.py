
# try:
#     n1=int(input('Enter the number 1: '))
#     n2=int(input('Enter the number 2(o is not allowed): '))
#     s=n1/n2
#     print(s)
# except:
#     print('Something went wrong')
#TypeError
#ZeroDivisionError
#ValueError

# try:
#     n1=int(input('Enter the number 1: '))
#     n2=int(input('Enter the number 2(o is not allowed): '))
#     s=n1/n2
#     print(s)
# except Exception as e:
#     print('Something went wrong',e)

try:
    n1=int(input('Enter the number 1: '))
    n2=int(input('Enter the number 2(o is not allowed): '))
    s=n1/n2
    print(s)
except ZeroDivisionError as e:
    print('Division by zero is not allowed',e)
except ValueError as e:
    print('Invalid input, please enter a number',e)

print('This is my 1st line and it is important')