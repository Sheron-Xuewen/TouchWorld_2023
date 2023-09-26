import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('features_and_labels2trees.csv')

# Check for missing or inconsistent data
print("Checking for missing values...")
missing_values = df.isnull().sum()
print(missing_values)

# Extract features (X) and labels (y)
X = df.drop(['label', 'sample_id'], axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

X_train.to_csv('X_train.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("Data cleaning and splitting completed. Check your directory for the new CSV files.")
