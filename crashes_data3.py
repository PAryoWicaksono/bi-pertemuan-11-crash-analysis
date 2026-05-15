import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
file_path = 'crashes_data.csv'


# Membaca file CSV
df = pd.read_csv(file_path)
df.columns = df.columns.str.lower().str.strip()
cols = [
   'injuries_fatal',
   'injuries_incapacitating',
   'injuries_non_incapacitating',
   'injuries_reported_not_evident'
]
available_cols = [c for c in cols if c in df.columns]
df[available_cols] = df[available_cols].fillna(0)
df['injuries_total'] = df[available_cols].sum(axis=1)
df_day = df[df['lighting_condition'] == 'daylight']
df_dark = df[df['lighting_condition'] == 'darkness']
fig = go.Figure()

fig.add_trace(go.Histogram(
   x=df_day['injuries_total'],
   name='Daylight',
   opacity=0.6
))

fig.add_trace(go.Histogram(
   x=df_dark['injuries_total'],
   name='Darkness',
   opacity=0.6
))
# Overlay mode
fig.update_layout(
   barmode='overlay',
   title='Distribusi Total Injuries (Daylight vs Darkness)',
   xaxis_title='Total Injuries',
   yaxis_title='Frequency'
)

fig.show()

