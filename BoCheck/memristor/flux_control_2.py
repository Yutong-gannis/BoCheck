import numpy as np
import matplotlib.pyplot as plt
from memristor import Flux_Controlled_Memristor


mem = Flux_Controlled_Memristor()

mem.x = 0

dt = 0.001
t = np.arange(0, 2, dt)

frequencies = [1, 3, 5]
colors = ['r', 'g', 'b']

plt.figure(figsize=(6, 4))

for f, color in zip(frequencies, colors):
    V = np.sin(2 * np.pi * f * t)
    I = np.zeros(len(V))
    for i in range(len(V)):
        mem.r = mem.R()
        I[i] = V[i] / mem.r
        
        d_phi = mem.d_phi(V[i])
        phi = mem.update_phi(dt, d_phi)
    
    plt.plot(V, I, label=f'{f} Hz', color=color)

plt.xlabel('Voltage/V')
plt.ylabel('Current/A')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("VA_at_different_frequency.png")

amplitudes = [1, 3, 8]
colors = ['purple', 'orange', 'blue']

plt.figure(figsize=(6, 4))

for amp, color in zip(amplitudes, colors):
    V = amp * np.sin(2 * np.pi * t)
    I = np.zeros(len(V))
    
    for i in range(len(V)):
        mem.r = mem.R()
        I[i] = V[i] / mem.r
        
        d_phi = mem.d_phi(V[i])
        phi = mem.update_phi(dt, d_phi)
    
    plt.plot(V, I, label=f'{amp} V', color=color)

plt.xlabel('Voltage/V')
plt.ylabel('Current/A')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("VA_at_different_amplitude.png")
