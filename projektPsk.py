import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fmin
os.chdir('c:/Users/Nikita/Desktop/')
f = open("psk.txt", "r")

def resp(t,alfa,beta,k,omega_d):
  pierwszy=math.exp(-alfa*t)
  drugi=math.sin(beta*t)
  trzeci=(k/omega_d)
  return pierwszy*drugi*trzeci
def czytaj():
  t=[]
  y=[]
  for line in f:
    kolumny=line.split()
    t.append(float(kolumny[0]))
    y.append(float(kolumny[1]))
  return t,y
t,y=czytaj()
def squares(param):
    sqr = 0
    for idx,i in enumerate(y):
        sqr += (float(i) - resp(float(t[idx]), param[0], param[1],param[2] , param[3]))**2
    return sqr
def stworzTeorie(dopasowane):
  teorytyczne=[]
  for i in t:
    teorytyczne.append(resp(float(i),dopasowane[0],dopasowane[1],dopasowane[2],dopasowane[3]))
  return teorytyczne
def dopasuj():
  #alfa,t,beta,k,omega_d
  fit=0
  startowa=[ 29.0925701,-1.10348782,-1.71743327*10**(-5) , 1.67782980*10**(-7)]
  for i in range(0,10):
    fit=fmin(squares,startowa ,maxiter=10000)
    startowa=fit
  return fit

fitted=dopasuj()
wynikowe=stworzTeorie(fitted)

plt.plot(t,y,t,wynikowe)
plt.show()