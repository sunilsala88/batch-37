
#never name your file same as built in module name
#pypi.org
import file1

import random
import time
import math
import os
import sys
print(file1.a)
file1.abc()

import numpy

c1=file1.Circle(5)
print(c1.area())
print(c1.circumference())

print(random.random())
time.sleep(1)
print(random.randint(1,10))
print(math.sqrt(16))
print(os.getcwd())
sys.exit()

#pip install numpy
#pip uninstall numpy
#upgrade library
#pip install --upgrade numpy
#downgrade library
#pip install numpy==1.21.0
#list of installed libraries
#pip list/pip freeze