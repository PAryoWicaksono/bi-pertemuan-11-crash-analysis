# =========================================
# 1. IMPORT LIBRARY
# =========================================
import pandas as pd
import matplotlib.pyplot as plt

# =========================================
# 2. LOAD DATA
# =========================================
file_path = "crashes_data.csv"
df = pd.read_csv(file_path)

# =========================================
# 3. NORMALISASI NAMA KOLOM
# =========================================
df.columns = df.columns.str.lower().str.strip()

# =========================================
# 4. VALIDASI KOLOM YANG DIBUTUHKAN
# =========================================
required_cols = [
    "injuries_fatal",
    "injuries_incapacitating",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident"
]

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Kolom '{col}' tidak ditemukan dalam dataset.")

# =========================================
# 5. HANDLE MISSING VALUES
# =========================================
df[required_cols] = df[required_cols].fillna(0)

# Pastikan semua kolom cedera bertipe angka
for col in required_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =========================================
# 6. MEMBUAT ATRIBUT CLASS: impact_risk
# =========================================
def get_impact_risk(row):
    if row["injuries_fatal"] > 0 or row["injuries_incapacitating"] > 0:
        return "Serious/Fatal"
    elif row["injuries_non_incapacitating"] > 0 or row["injuries_reported_not_evident"] > 0:
        return "Minor Injury"
    else:
        return "No Injury"

df["impact_risk"] = df.apply(get_impact_risk, axis=1)

# =========================================
# 7. CEK HASIL CLASS
# =========================================
print("Distribusi impact_risk:")
print(df["impact_risk"].value_counts())

print("\nContoh data:")
print(df[required_cols + ["impact_risk"]].head(10))

# =========================================
# 8. SIMPAN DATA BARU
# =========================================
df.to_csv("crashes_data_dengan_impact_risk.csv", index=False)

print("\nFile berhasil dibuat: crashes_data_dengan_impact_risk.csv")

# =========================================
# 9. MEMBUAT GRAFIK DISTRIBUSI impact_risk
# =========================================

# Hitung jumlah masing-masing class
impact_counts = df["impact_risk"].value_counts()

# Atur urutan class agar rapi
class_order = ["No Injury", "Minor Injury", "Serious/Fatal"]
impact_counts = impact_counts.reindex(class_order)

# Hitung persentase
impact_percent = (impact_counts / impact_counts.sum() * 100).round(2)

# Buat grafik
plt.figure(figsize=(8, 5))
plt.bar(impact_counts.index, impact_counts.values)

plt.title("Distribusi Impact Risk")
plt.xlabel("Kategori Impact Risk")
plt.ylabel("Jumlah Kasus")

# Tambahkan label jumlah dan persentase di atas bar
for i, value in enumerate(impact_counts.values):
    plt.text(
        i,
        value,
        f"{value:,}\n({impact_percent.iloc[i]}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Simpan grafik sebagai PNG
plt.savefig("grafik_distribusi_impact_risk.png", dpi=300)

print("Grafik berhasil dibuat: grafik_distribusi_impact_risk.png")

# Tampilkan grafik
plt.show()