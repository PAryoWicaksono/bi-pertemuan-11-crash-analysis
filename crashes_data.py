import pandas as pd

file_path = 'crashes_data.csv'


# Membaca file CSV
df = pd.read_csv(file_path)

print("Daftar Kolom di Dataset Student Health:")
print(df.shape)
print(df.head())
print(df.alignment.nunique())
