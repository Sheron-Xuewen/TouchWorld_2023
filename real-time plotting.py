import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re
import threading

accel_x = []
accel_y = []
accel_z = []

fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
fig.suptitle('Acceleration Data')

# Function to update the plot
def update(frame):
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()

    axs[0].plot(accel_x, label='X', color='r')
    axs[1].plot(accel_y, label='Y', color='g')
    axs[2].plot(accel_z, label='Z', color='b')

    for ax in axs:
        ax.legend(loc='upper right')
        ax.grid(True)

# Open serial port
try:
    ser = serial.Serial('COM3', 9600)
    print("Serial port opened successfully")
except serial.serialutil.SerialException as e:
    print(f"Failed to open serial port: {e}")
    exit(1)

# Function to read serial data
def read_serial():
    while True:
        if ser.in_waiting:
            try:
                line = ser.readline().decode('utf-8').strip()
                match = re.search(r'X=\s*(-?\d+\.\d+).+Y=\s*(-?\d+\.\d+).+Z=\s*(-?\d+\.\d+)', line)
                if match:
                    x, y, z = map(float, match.groups())
                    accel_x.append(x)
                    accel_y.append(y)
                    accel_z.append(z)
                else:
                    print(f"Skipping line: {line.strip()}")
            except (serial.serialutil.SerialException, UnicodeDecodeError) as e:
                print(f"Error reading line: {e}")
                ser.close()
                print("Serial port closed due to error")
                break

# Start reading data from the serial port in a new thread
thread = threading.Thread(target=read_serial)
thread.start()

# Run the animation
ani = FuncAnimation(fig, update, interval=200, save_count=100)

# Show the plot
plt.show()
