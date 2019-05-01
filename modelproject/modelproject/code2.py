import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize



def objective(x) :
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    return x1+x2+x3


x1=[2,2,2]
print(objective(x1))

def constraint1(x):
    return x[0]*x[1]*x[2]-25
def constraint2(x):
    sum_consume= 40
    for i in range(3) :
        sum_consume= sum_consume-x[i]**2
    return sum_consume

b=(1.0, 1.0)
bds=(b,b,b)
con1={'type':'ineq', 'fun':constraint1}
con2={'type':'eq', 'fun':constraint2}
cons=[con1, con2]

sol=minimize(objective, x1, method='SLSQP', \
    bounds=bds, constraints=cons)

print(sol)

print(sol.x[1])
