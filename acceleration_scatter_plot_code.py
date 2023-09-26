
import matplotlib.pyplot as plt
import re
import pandas as pd

accel_x = []
accel_y = []
accel_z = []

# Function to read data
def read_data(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'X=\s*(-?\d+\.\d+)\s+Y=\s*(-?\d+\.\d+)\s+Z=\s*(-?\d+\.\d+)', line)
            if match:
                accel_x.append(float(match.group(1)))
                accel_y.append(float(match.group(2)))
                accel_z.append(float(match.group(3)))

# Read the data
read_data('E:\\Tap\\02 Data Extraction\\32')

# Create a DataFrame
df = pd.DataFrame({
    'X': accel_x,
    'Y': accel_y,
    'Z': accel_z
})

# Check if the DataFrame is empty
if df.empty:
    print("The DataFrame is empty. No data to plot.")
else:
    # Plotting the scatter plot
    plt.figure(figsize=(10, 10))
    plt.scatter(df['X'], df['Y'], c=df['Z'], cmap='viridis', s=50)
    plt.colorbar().set_label('Z Acceleration')
    plt.xlabel('X Acceleration')
    plt.ylabel('Y Acceleration')
    plt.title('Scatter Plot of Accelerometer Data')
    plt.grid(True)
    plt.show()
