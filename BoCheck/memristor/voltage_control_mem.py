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

print(min(R))
print(max(R))

# Plot the input voltage (V) vs. current (I)
plt.plot(V, I)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (I)')
plt.title('Voltage vs. Current')
plt.grid(True)
plt.show()


mem.x = 0      # Starting from low resistance state (LRS)
target_x = 1   # Target state value (high resistance state HRS)
V = 1          # Constant voltage applied to induce switching
dt = 0.001     # Time step
time_elapsed = 0

# Array to track memristor state over time
x_values = []

# Start switching and track time
while mem.x < target_x:
    x_values.append(mem.x)
    # Update memristor state
    dx = mem.dx(V)
    mem.update_x(dt, dx)
    time_elapsed += dt

# Plot memristor state change over time
plt.plot(np.arange(dt, time_elapsed, dt), x_values)
plt.xlabel('Time (s)')
plt.ylabel('Memristor State (x)')
plt.title('Memristor State Transition Over Time')
plt.show()

print(f"Switching time: {time_elapsed:.4f} seconds") # 0.013s