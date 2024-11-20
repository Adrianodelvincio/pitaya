from matplotlib import pyplot as plt
import numpy as np
import sys

filename = str(sys.argv[1])
print(f"reading file {filename}")
V = np.loadtxt(str(filename), unpack = True)

plt.figure(1)

start = int(sys.argv[2])
stop  = int(sys.argv[3])

V = V[start:stop]

plt.errorbar(np.linspace(start, stop + 1, len(V)), V, marker = "x", color = 'red', linestyle = '')
name = f"{filename.split('/',1)[-1]}"
name = name.split('.',1)[0] + ".png"
print(f"saving {name}")
plt.savefig(name)
