import pandas as pd
import numpy as np
import os
from scipy.fftpack import fft
from scipy import stats

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
        data = df[axis].to_numpy()
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
    return features


def main():
    file_path = 'E:\\Tap\\04 10sec\\705processed'
    df = read_data(file_path)

    if df.empty:
        print("Dataframe is empty, skipping feature extraction.")
        return

    label = input("Please enter the label: ")
    sample_id = input("Please enter the sample ID: ")

    features = extract_features(df, label, sample_id)

    output_file = 'features_and_labels3.csv'
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write(','.join(features.keys()) + '\n')

    with open(output_file, 'a') as f:
        f.write(','.join(map(str, features.values())) + '\n')

    print(f"Features saved to {output_file}")


if __name__ == "__main__":
    main()
