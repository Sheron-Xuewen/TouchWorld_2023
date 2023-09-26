import matplotlib.pyplot as plt
import re

accel_x = []
accel_y = []
accel_z = []

# Open the data file
try:
    with open('E:\\Tap\\02 Data Extraction\\Raw Data\\31') as file:
        print("File opened successfully.")

        for line in file:
            match = re.search(r'X=\s*(-?\d+\.\d+)\s+Y=\s*(-?\d+\.\d+)\s+Z=\s*(-?\d+\.\d+)', line)

            if match:
                x, y, z = map(float, match.groups())
                accel_x.append(x)
                accel_y.append(y)
                accel_z.append(z)
            else:
                print(f"Skipping line: {line.strip()}")

except FileNotFoundError:
    print("File not found. Please make sure the data file is in the same directory as this script.")

# Create the plot
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
fig.suptitle('Acceleration Data')

# Plot X, Y, and Z acceleration values
axs[0].plot(accel_x, label='X', color='r')
axs[1].plot(accel_y, label='Y', color='g')
axs[2].plot(accel_z, label='Z', color='b')

# Add labels to the plot
for ax in axs:
    ax.legend(loc='upper right')
    ax.grid(True)

# Show the plot
plt.show()
