from memristor import Flux_Controlled_Memristor
import matplotlib.pyplot as plt
import numpy as np


mem = Flux_Controlled_Memristor()

# Set initial value for memristor state
mem.phi = 0

# Time parameters
dt = 0.001  # time step
t = np.arange(0, 2, dt)  # time array

# Input voltage waveform
V = np.sin(np.pi * t)

# Arrays to store current, resistance, and memristor state
I = np.zeros(len(V))
R = np.zeros(len(V))
PHI = np.zeros(len(V))

# Iterate through each time step
for i in range(len(V)):
    # Record current memristor state
    PHI[i] = mem.phi
    
    # Calculate resistance and current
    mem.r = mem.R()
    R[i] = mem.r
    I[i] = V[i] / mem.r
    
    # Update memristor state
    d_phi = mem.d_phi(V[i])
    phi = mem.update_phi(dt, d_phi)
    PHI[i] = phi

print(min(R))
print(max(R))

# Plot the input voltage (V) vs. current (I)
plt.plot(V, I, c='k')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (I)')
plt.title('Voltage vs. Current')
plt.grid(True)
plt.show()

mem.r = 100      # Starting from low resistance state (LRS)
target_r = 2400   # Target state value (high resistance state HRS)
V = 1          # Constant voltage applied to induce switching
dt = 0.001     # Time step
time_elapsed = 0

# Array to track memristor state over time
r_values = []

# Start switching and track time
while mem.r < target_r:
    # Update memristor state
    d_phi = mem.d_phi(V)
    mem.update_phi(dt, d_phi)
    mem.r = mem.R()
    r_values.append(mem.r)
    time_elapsed += dt

# Plot memristor state change over time
plt.plot(np.arange(dt, time_elapsed, dt), r_values)
plt.xlabel('Time (s)')
plt.ylabel('Memristor State (x)')
plt.title('Memristor State Transition Over Time')
plt.show()

print(f"Switching time: {time_elapsed:.4f} seconds") # 0.5520s