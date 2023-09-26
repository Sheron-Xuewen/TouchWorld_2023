import re
import pandas as pd
import numpy as np
from scipy import signal
from scipy.stats import zscore

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

# Function to write processed data to a new file
def write_data(file_path, df):
    with open(file_path, 'w') as file:
        for index, row in df.iterrows():
            file.write(f"X= {row['X']} Y= {row['Y']} Z= {row['Z']}\n")

file_path = 'E:\\Tap\\02 Data Extraction\\12'
read_data(file_path)

df = pd.DataFrame({
    'X': accel_x,
    'Y': accel_y,
    'Z': accel_z
})

z_scores = np.abs(zscore(df))
df = df[(z_scores < 3).all(axis=1)]

window = signal.windows.gaussian(51, std=7)
df['X'] = signal.convolve(df['X'], window, mode='same') / sum(window)
df['Y'] = signal.convolve(df['Y'], window, mode='same') / sum(window)
df['Z'] = signal.convolve(df['Z'], window, mode='same') / sum(window)

nyquist = 0.5 * 50  # Assuming a sampling frequency of 50 Hz
low = 0.5 / nyquist
high = 3.0 / nyquist
b, a = signal.butter(4, [low, high], btype='band')
df['X'] = signal.filtfilt(b, a, df['X'])
df['Y'] = signal.filtfilt(b, a, df['Y'])
df['Z'] = signal.filtfilt(b, a, df['Z'])

write_data('E:\\Tap\\02 Data Extraction\\processed\\12processed', df)
