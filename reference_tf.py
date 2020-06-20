import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt

def get_tf(student_number):
  numb = str(student_number)
  dt=0.01
  G = sig.dlti([1, -int(numb[2]), int(numb[1])],[int(numb[0]), -int(numb[3])/8, int(numb[4])/8, -int(numb[5])/16], dt=dt)
  return G

G = get_tf(172017) # tu oczywiście proszę podać swój numer indeksu
print(G)
N=100
w = G.impulse(n=N)
#w = G.step(n=N)
data = np.reshape(np.array(w[1][0]),(N,))

plt.plot(data,'x-')
plt.show()