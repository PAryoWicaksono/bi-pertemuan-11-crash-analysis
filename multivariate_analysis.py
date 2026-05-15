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
# 4. VALIDASI KOLOM
# =========================================
required_cols = [
   'contributory_cause',
   'weather_condition',
   'lighting_condition',
   'trafficway_type',
   'injuries_fatal',
   'injuries_incapacitating',
   'injuries_non_incapacitating',
   'injuries_reported_not_evident'
]


for col in required_cols:
   if col not in df.columns:
       raise ValueError(f"Kolom '{col}' tidak ditemukan")


# =========================================
# 5. HANDLE MISSING VALUES
# =========================================
df[['injuries_fatal',
   'injuries_incapacitating',
   'injuries_non_incapacitating',
   'injuries_reported_not_evident']] = df[[
       'injuries_fatal',
       'injuries_incapacitating',
       'injuries_non_incapacitating',
       'injuries_reported_not_evident'
   ]].fillna(0)


df['contributory_cause'] = df['contributory_cause'].fillna('unknown')
df['weather_condition'] = df['weather_condition'].fillna('unknown')
df['lighting_condition'] = df['lighting_condition'].fillna('unknown')
df['trafficway_type'] = df['trafficway_type'].fillna('unknown')


# =========================================
# 6. BUAT injuries_total
# =========================================
df['injuries_total'] = (
   df['injuries_fatal'] +
   df['injuries_incapacitating'] +
   df['injuries_non_incapacitating'] +
   df['injuries_reported_not_evident']
)


# =========================================
# 7. BUAT SEVERITY
# =========================================
def severity_label(x):
   if x == 0:
       return "No Injury"
   elif x <= 2:
       return "Low"
   elif x <= 5:
       return "Medium"
   else:
       return "High"


df['severity'] = df['injuries_total'].apply(severity_label)


# =========================================
# 8. FILTER DATA (PENTING AGAR TIDAK PADAT)
# =========================================


# Top cause
top_causes = df['contributory_cause'].value_counts().head(7).index


# Top weather
top_weather = df['weather_condition'].value_counts().head(5).index


# Top lighting
top_lighting = df['lighting_condition'].value_counts().head(5).index


# Traffic_type
top_traffictype = df['trafficway_type'].value_counts().head(5).index


df_filtered = df[
   (df['contributory_cause'].isin(top_causes)) &
   (df['weather_condition'].isin(top_weather)) &
   (df['lighting_condition'].isin(top_lighting))&
   (df['trafficway_type'].isin(top_traffictype))
]


# Sampling untuk performa
if len(df_filtered) > 8000:
   df_filtered = df_filtered.sample(5000, random_state=42)


# =========================================
# 9. PARALLEL CATEGORIES PLOT
# =========================================
fig = px.parallel_categories(
   df_filtered,
   dimensions=[
       'contributory_cause',
       'weather_condition',
       'lighting_condition',
       'trafficway_type',
       'severity'
   ],
   color=df_filtered['injuries_total'],
   title="Multivariate Analysis: Cause >> Weather >> Lighting >> Severity"
)


fig.update_layout(title_x=0.5)


fig.show()
