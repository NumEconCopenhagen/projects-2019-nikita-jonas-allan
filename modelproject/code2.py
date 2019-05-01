import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import time
from scipy import linalg
from scipy import optimize
import sympy as sm



def objective(x) :
    x1 = x[0]
    x2 = x[1]
    x3 = 