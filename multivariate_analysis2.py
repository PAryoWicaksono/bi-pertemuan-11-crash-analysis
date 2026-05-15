# =========================================
# 1. IMPORT LIBRARY
# =========================================
import pandas as pd
import plotly.express as px

# =========================================
# 2. LOAD DATA
# =========================================
file_path = 'crashes_data.csv'
df = pd.read_csv(file_path)

# =========================================
# 3. NORMALISASI KOLOM
# =========================================
df.columns = df.columns.str.lower().str.strip()

# =========================================
# 4. HITUNG TOTAL CEDERA & SEVERITY
# =========================================
injury_cols = [
    'injuries_fatal', 'injuries_incapacitating', 
    'injuries_non_incapacitating', 'injuries_reported_not_evident'
]
df[injury_cols] = df[injury_cols].fillna(0)

# Total semua cedera (Ini yang akan jadi parameter angka 0-7)
df['injuries_total'] = df[injury_cols].sum(axis=1)

# Membuat Label Severity untuk kolom dimensi terakhir
def get_severity(x):
    if x == 0: return "No Injury"
    elif x <= 2: return "Low"
    elif x <= 5: return "Medium"
    else: return "High"

df['severity'] = df['injuries_total'].apply(get_severity)

# =========================================
# 5. HANDLE MISSING VALUES (VARIABEL PROYEK)
# =========================================
target_cols = ['alignment', 'lighting_condition', 'contributory_cause', 'first_crash_type']
for col in target_cols:
    df[col] = df[col].fillna('UNKNOWN')

# =========================================
# 6. FILTER DATA (TOP CATEGORIES)
# =========================================
top_alignment = df['alignment'].value_counts().head(4).index
top_lighting = df['lighting_condition'].value_counts().head(4).index
top_cause = df['contributory_cause'].value_counts().head(6).index
top_crash = df['first_crash_type'].value_counts().head(6).index

df_filtered = df[
    (df['alignment'].isin(top_alignment)) &
    (df['lighting_condition'].isin(top_lighting)) &
    (df['contributory_cause'].isin(top_cause)) &
    (df['first_crash_type'].isin(top_crash))
].copy()

# Sampling agar performa browser tetap lancar
if len(df_filtered) > 5000:
    df_filtered = df_filtered.sample(5000, random_state=42)

# =========================================
# 7. PARALLEL CATEGORIES PLOT (DENGAN SKALA PARAMETER)
# =========================================
fig = px.parallel_categories(
    df_filtered,
    dimensions=[
        'alignment', 
        'lighting_condition', 
        'contributory_cause', 
        'first_crash_type',
        'severity'
    ],
    color='injuries_total', # Menggunakan angka total cedera sebagai warna
    color_continuous_scale=[
        [0, 'green'],   # Rendah = Hijau
        [0.5, 'yellow'],# Menengah = Kuning
        [1.0, 'red']    # Tinggi = Merah
    ],
    title="Analisis Pola Bahaya: Hubungan Kondisi Lingkungan dan Penyebab terhadap Dampak Kecelakaan",
    labels={
        'alignment': 'Bentuk Jalan',
        'lighting_condition': 'Cahaya',
        'contributory_cause': 'Penyebab',
        'first_crash_type': 'Tipe Tabrakan',
        'severity': 'Severity (Class)',
        'injuries_total': 'Total Cedera'
    }
)

# Menampilkan skala parameter (Color Bar) di sebelah kanan sesuai contoh
fig.update_layout(
    coloraxis_showscale=True, 
    title_x=0.5,
    coloraxis_colorbar=dict(title="injuries_total")
)

fig.show()