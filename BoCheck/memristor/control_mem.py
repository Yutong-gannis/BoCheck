from memristor import memristor
import matplotlib.pyplot as plt
import numpy as np


mem = memristor()

# Set initial value for memristor state
mem.x = 0

# Time parameters
dt = 0.001  # time step
t = np.arange(0, 1, dt)  # time array

# Input voltage waveform
V = np.sin(2 * np.pi * t)

# Arrays to store current, resistance, and memristor state
I = np.zeros(len(V))
R = np.zeros(len(V))
X = np.zeros(len(V))

# Iterate through each time step
for i in range(len(V)):
    # Record current memristor state
    X[i] = mem.x
    
    # Calculate resistance and current
    mem.r = mem.R()
    R[i] = mem.r
    I[i] = V[i] / mem.r
    
    # Update memristor state
    dx = mem.dx(V[i])
    x = mem.update_x(dt, dx)
    X[i] = x

# Plot the input voltage (V) vs. current (I)
plt.plot(V, I)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (I)')
plt.title('Voltage vs. Current')
plt.grid(True)
plt.show()
