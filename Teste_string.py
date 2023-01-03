import py_dss_interface
import random
import math  # cos() for Rastrigin
import copy  # array-copying convenience
import sys  # max float

for j in range(5):
    node = 6
    node = str(node)
    gerador = str(j)

    my_string = "new generator.gen bus1=node  Kw=2342 Kvar= 0.00 model=7"
    index = my_string.find(" bus")
    my_string = my_string[:index] + gerador + my_string[index:]
    index = my_string.find("  Kw")
    final_string = my_string[:index] + node + my_string[index:]
    print(final_string)