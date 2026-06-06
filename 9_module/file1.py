
a=100

def abc():
    print("abc function")


class Circle:
    pi=3.14
    def __init__(self,radius):
        self.radius=radius
    
    def area(self):
        area=self.pi*(self.radius**2)
        return area

    def circumference(self):
        circumference=2*self.pi*self.radius
        return circumference
