import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data - Pastikan file CSV ada di folder yang sama
df = pd.read_csv('student_health_new.csv')

# Cek 5 data teratas untuk memastikan data terbaca
print("--- 5 Data Teratas ---")
print(df.head())

# Visualisasi Pie Chart Distribusi Risiko
plt.figure(figsize=(8, 6))
df['risk_level'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#66b3ff','#ff9999','#99ff99'])
plt.title('Distribusi Tingkat Risiko Kesehatan Mental')
plt.show()