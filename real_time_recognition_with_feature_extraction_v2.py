import serial
import time
import pandas as pd
import numpy as np
import re
from scipy import signal
from scipy.stats import zscore
from joblib import load
from tkinter import messagebox
import tkinter as tk

print("Python script started")

try:
    ser = serial.Serial('COM3', 9600)  # Adjust 'COM3' based on your Arduino's port
    print("Serial port opened successfully")
    
    # Clear the serial buffer
    while ser.in_waiting:
        ser.readline()
    print("Serial buffer cleared")
    
except serial.serialutil.SerialException as e:
    print(f"Failed to open serial port: {e}")
    exit(1)

filename = "temp_data.txt"  # Temporary file to store raw data

try:
    with open(filename, "w") as f:
        for i in range(100):  # Adjust the range based on the number of data points you want to collect
            data = ser.readline().decode("utf-8").strip()
            f.write(data + "\n")
    print(f"Data saved to {filename}")
    
except Exception as e:
    print(f"Failed to save data: {e}")
    exit(1)

accel_x = []
accel_y = []
accel_z = []

def read_data(filename):
    with open(filename, 'r') as f:
        for line in f:
            components = line.strip().split()
            x = float(components[0])
            y = float(components[1])
            z = float(components[2])
            accel_x.append(x)
            accel_y.append(y)
            accel_z.append(z)

read_data(filename)

accel_x = np.array(accel_x)
accel_y = np.array(accel_y)
accel_z = np.array(accel_z)


def extract_features(accel_x, accel_y, accel_z):
def read_data(file_path):
    x_values = []
    y_values = []
    z_values = []

    with open(file_path, 'r') as f:
        for line in f:
            try:
                components = line.strip().split()
                x = float(components[1])
                y = float(components[3])
                z = float(components[5])
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)
            except Exception as e:
                print(f"Skipping invalid line: {line.strip()} ({str(e)})")

    return pd.DataFrame({
        'X': x_values,
        'Y': y_values,
        'Z': z_values
    })

def extract_features(df, label, sample_id):
    features = {}
    for axis in ['X', 'Y', 'Z']:
        data = df[axis].to_numpy()  # Convert to numpy array
        if len(data) == 0:
            print(f"Skipping empty data for axis {axis}")
            continue

        # Time domain features
        features[f"{axis}_max"] = np.max(data)
        features[f"{axis}_min"] = np.min(data)
        features[f"{axis}_median"] = np.median(data)
        features[f"{axis}_q1"] = np.percentile(data, 25)
        features[f"{axis}_q3"] = np.percentile(data, 75)
        features[f"{axis}_rms"] = np.sqrt(np.mean(np.square(data)))
        features[f"{axis}_zero_cross_rate"] = len(np.where(np.diff(np.sign(data)))[0])

        # Frequency domain features
        fft_vals = np.fft.fft(data)
        fft_centroid = np.sum(fft_vals * np.arange(len(fft_vals))) / np.sum(fft_vals)
        fft_std = np.sqrt(np.sum(np.square(fft_vals - fft_centroid)) / len(fft_vals))
        features[f"{axis}_fft_centroid"] = np.abs(fft_centroid)
        features[f"{axis}_fft_std"] = np.abs(fft_std)

        # Statistical features
        features[f"{axis}_mean"] = np.mean(data)
        features[f"{axis}_std"] = np.std(data)
        features[f"{axis}_skew"] = stats.skew(data)
        features[f"{axis}_kurtosis"] = stats.kurtosis(data)

    features['label'] = label
    features['sample_id'] = sample_id
    
    return features  # Assuming 'features' is the variable that holds the final feature vector

features = extract_features(accel_x, accel_y, accel_z)

threshold = 0.2  # Predefined threshold for Y_std
if features['Y_std'] > threshold:
    model = load("random_forest_group1.joblib")
else:
    model = load("random_forest_group2.joblib")

prediction = model.predict(features.reshape(1, -1))[0]

root = tk.Tk()
root.withdraw()  # Hide the main window
messagebox.showinfo("Prediction Result", f"The object is predicted to be of class {prediction}")
