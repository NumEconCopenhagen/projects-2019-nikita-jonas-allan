import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def objective(x) :
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    return x1+x2+x3


x1=[2,2,2]
print(objective(x1))
