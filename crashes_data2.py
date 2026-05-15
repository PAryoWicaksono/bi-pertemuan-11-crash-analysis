import pandas as pd
import matplotlib.pyplot as plt
file_path = 'crashes_data.csv'


# Membaca file CSV
df = pd.read_csv(file_path)
df.columns = df.columns.str.lower().str.strip()

# Lighting
plt.figure(figsize=(6,6))
df['lighting_condition'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Lighting Condition")
plt.ylabel("")
plt.show()