import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fmin
from scipy.interpolate import interp1d
from scipy import signal


f = open("psk.txt", "r")


def resp(t,dzeta,omega_n,k):
  lewy=0
  prawy=0
  if dzeta>0 and dzeta<1:
    omega_d=omega_n*math.sqrt(1-dzeta**2)
    lewy=( (omega_n*math.exp(-dzeta*omega_n*t))/(math.sqrt(1-dzeta**2)) )
    prawy=math.sin(omega_d*t)
  return lewy*prawy*k
def czytaj():
  t=[]
  y=[]
  for line in f:
    kolumny=line.split()
    t.append(float(kolumny[0]))
    y.append(float(kolumny[1]))
  return t,y
t,y=czytaj()

def linearyzuj(t,y):
  nowe_t=[]
  nowe_y=[]
  dt=t[1]-t[0]
  for idx,i in enumerate(t):
    nowe_t.append(i)
    nowe_t.append((dt/2)+i )
  f = interp1d(t, y, fill_value="extrapolate", kind='cubic')
  nowe_y=f(nowe_t)
  return nowe_t,nowe_y
nowet,nowey=linearyzuj(t,y)
def squares(param):
  sqr = 0
  for idx,i in enumerate(nowey):
      sqr += (float(i) - resp(nowet[idx], param[0], param[1],param[2] ))**2
  wynik=math.sqrt((1/len(nowey))*sqr)
  return wynik

def stworzTeorie(dopasowane):
  teorytyczne=[]
  for i in nowet:
    teorytyczne.append(resp(float(i),dopasowane[0],dopasowane[1],dopasowane[2]))
  return teorytyczne
def dopasuj():
  startowa_old=[ 0.01,0.001,0.1]
  fit=fmin(squares,startowa_old,maxiter=10000)
  return fit

fitted=dopasuj()
print(fitted)
wynikowe=stworzTeorie(fitted)

# plt.plot(t,y,t,wynikowe,nowet,nowey)
plt.plot(nowet,nowey,nowet,wynikowe)

plt.show()