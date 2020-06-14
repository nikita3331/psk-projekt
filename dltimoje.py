import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fmin
from scipy.interpolate import interp1d
from scipy import signal


f = open("psk.txt", "r")


def resp(omega_n,dzeta,k):
  funkcja=signal.dlti([omega_n*omega_n*k], [1,2*omega_n*dzeta, omega_n*omega_n], dt=0.005)
  t, y = signal.dimpulse(funkcja, n=61)
  y=np.squeeze(y)
  return y 
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
    if idx<30:
        nowe_t.append(i)
        nowe_t.append((dt/2)+i )
  f = interp1d(t, y, fill_value="extrapolate", kind='cubic')
  nowe_y=f(nowe_t)
  return nowe_t,nowe_y
nowet,nowey=linearyzuj(t,y)
def squares(param):
  sqr = 0
  trans=resp(param[0], param[1], param[2])
  for idx,i in enumerate(nowey):
      sqr += (float(i) -trans[idx] )**2
  wynik=math.sqrt(sqr*(1/len(nowey)))
  return sqr

def stworzTeorie(dopasowane):
  teorytyczne=resp(dopasowane[0],dopasowane[1],dopasowane[2])
  return teorytyczne
def dopasuj():
  startowa_old=[ 0.01,0.001,6]
  fit=fmin(squares,startowa_old,maxiter=10000)
  return fit

fitted=dopasuj()
wynikowe=stworzTeorie(fitted)

# plt.plot(t,y,t,wynikowe,nowet,nowey)
plt.plot(nowet,nowey,nowet,wynikowe)

plt.show()