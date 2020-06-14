import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fmin
f = open("psk.txt", "r")

def resp_old(t,alfa,beta,k,omega_d):
  pierwszy=math.exp(-alfa*t)
  drugi=math.sin(beta*t)
  trzeci=(k/omega_d)
  return pierwszy*drugi*trzeci
def resp(t,dzeta,omega_n,omega_d):
  pierszy=(math.exp(-dzeta*omega_n*t))/(math.sqrt(1-dzeta**2))
  full=1-pierszy*math.sin(omega_d*t+np.arctan((math.sqrt(1-dzeta**2))/(dzeta)) )
  return full
def czytaj():
  t=[]
  y=[]
  for line in f:
    kolumny=line.split()
    t.append(float(kolumny[0]))
    y.append(float(kolumny[1]))
  return t,y
t,y=czytaj()
def squares_old(param):
    sqr = 0
    for idx,i in enumerate(y):
        sqr += (float(i) - resp_old(float(t[idx]), param[0], param[1],param[2] , param[3]))**2
    return sqr
def squares(param):
  sqr = 0
  for idx,i in enumerate(y):
      sqr += (float(i) - resp(float(t[idx]), param[0], param[1],param[2] ))**2
  return sqr
def stworzTeorie_old(dopasowane):
  teorytyczne=[]
  for i in t:
    teorytyczne.append(resp_old(float(i),dopasowane[0],dopasowane[1],dopasowane[2],dopasowane[3]))
  return teorytyczne
def stworzTeorie(dopasowane):
  teorytyczne=[]
  for i in t:
    teorytyczne.append(resp(float(i),dopasowane[0],dopasowane[1],dopasowane[2]))
  return teorytyczne
def dopasuj():
  startowa_old=[ 29.0925701,-1.10348782,-1.71743327*10**(-5) , 1.67782980*10**(-7)]
  fit=fmin(squares_old,startowa_old,maxiter=10000)
  return fit

fitted=dopasuj()
wynikowe=stworzTeorie_old(fitted)

plt.plot(t,y,t,wynikowe)
plt.show()