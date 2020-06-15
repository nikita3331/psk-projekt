import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fmin
from scipy.interpolate import interp1d
from scipy import signal
import pprint
#http://home.agh.edu.pl/~pautom/pliki/wyklady/przykladowe/06.pdf

f = open("psk.txt", "r")

ilosc=30
def resp(omega_n,dzeta,k):
  y=[0]*40
  if dzeta>0:
    funkcja=signal.dlti([omega_n*omega_n*k], [1,2*omega_n*dzeta, omega_n*omega_n], dt=0.005)
    t, y = signal.dimpulse(funkcja, n=40)
    y=np.squeeze(y)
    
  return y 
def czytaj():
  t=[]
  y=[]
  inde=0
  for line in f:
    if inde<20:
      kolumny=line.split()
      t.append(float(kolumny[0]))
      y.append(float(kolumny[1]))
    inde+=1
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
  trans=resp(param[0], param[1], param[2])
  for idx,i in enumerate(nowey):
      sqr += (float(i) -trans[idx] )**2
  wynik=math.sqrt(sqr*(1/len(nowey)))
  return wynik

def stworzTeorie(dopasowane):
  teorytyczne=resp(dopasowane[0],dopasowane[1],dopasowane[2])
  return teorytyczne
def dopasuj():
  startowa_old=[ 0.1,0.1,6]
  fit=fmin(squares,startowa_old,maxiter=10000)
  return fit
def wyswietlCzestotliwosci(funk):
  w, mag, phase = funk.bode()
  plt.figure()
  plt.title('Amplitudowy')
  plt.semilogx(w, mag)    # Bode magnitude plot
  plt.ylabel('Amplituda')
  plt.xlabel('w rad/s')
  plt.legend()
  plt.figure()
  plt.semilogx(w, phase)  # Bode phase plot
  plt.title('Fazowy')
  plt.ylabel('Faza')
  plt.xlabel('w rad/s')
  plt.legend()
  plt.show()
def wyswietlModelDane():
  plt.plot(nowet,nowey,label='Dane')
  przesuniete_t=[]
  for i in nowet:
    przesuniete_t.append(i-0.005)
  plt.plot(przesuniete_t,wynikowe,label='Model')
  plt.title('Liczba próbek pomiarowych=20')
  plt.ylabel('G(t) [V/V]')
  plt.xlabel('t [s]')
  plt.legend()
  plt.show()
def wyswietlSkokowa(funk):
  t_n,y_n=signal.dstep(funk, n=40)
  y_n=np.squeeze(y_n)
  plt.plot(t_n,y_n)
  plt.show()
  pprint.pprint(funk._as_ss())
  pprint.pprint(funk._as_zpk())
fitted=dopasuj()
wynikowe=stworzTeorie(fitted)
print('omega_n = ',fitted[0],'dzeta = ',fitted[1],'k = ',fitted[2])
# wyswietlModelDane()
funkcja=signal.dlti([fitted[0]*fitted[0]*fitted[2]], [1,2*fitted[0]*fitted[1], fitted[0]*fitted[0]], dt=0.005)
#wyswietlSkokowa(funkcja)

w, H = signal.dfreqresp(funkcja)
plt.figure()
plt.title('Charakterystyka Nyquista')
plt.plot(H.real, H.imag, "b")
plt.plot(H.real, -H.imag, "r")
plt.show()