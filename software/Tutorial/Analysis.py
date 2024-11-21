from scipy.interpolate import CubicSpline
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.optimize import brentq

datafile = str(sys.argv[1])
y = np.loadtxt(datafile, unpack = True)

y = y[(8192 - 20):(8320)]
t = np.arange(0, len(y), 1)*8

spline = CubicSpline(t, y)

# Creazione di un array di valori di t per valutare la spline (più denso per una curva liscia)
t_fine = np.linspace(650, 1000, 351)

# Calcolo dei valori di y per la spline sui nuovi t
y_fine = spline(t_fine)
y_max = np.max(y_fine)
yargmax = np.argmax(y_fine)

# Calcolare i valori al 10% e 90% del massimo
y_10 = 0.10 * y_max
y_90 = 0.90 * y_max

# Funzione per trovare i punti in cui la spline è uguale a un valore specifico
def find_t_for_y(spline, ytarget, t, yargmax):
    d = np.abs(ytarget - spline(t[0:yargmax]))
    result = t[np.argmin(d)]
    print(result)
    return result

# Troviamo i valori di t per 10% e 90%
t_10 = find_t_for_y(spline, y_10,t_fine,yargmax)
t_90 = find_t_for_y(spline, y_90,t_fine,yargmax)

# Calcolare la larghezza
width = t_90 - t_10

# Visualizzazione dei risultati
print(f"find t at 10% max: {t_10}  nS")
print(f"find t al 90% max: {t_90}  nS")
print(f"width:             {width} nS")

plt.figure(1)
plt.title(datafile, fontsize = 15)
plt.xlim(650,1000)
plt.errorbar(t,y, linestyle = '', marker = 'x', color = 'red')
plt.axvline(t_10, linestyle = '--', color = "grey")
plt.axvline(t_90, linestyle = '--', color = "grey")
plt.plot(t_fine, y_fine, marker = '', linestyle = '-', color = 'black')
text = f"width: {width} nS"
plt.text(t_fine[yargmax] + 20, y_max, text, fontsize=12, color='black', ha='left', va='center')
plt.savefig(f"analysis_fig/{datafile.removesuffix('.txt').split('/',1)[1]}.png")