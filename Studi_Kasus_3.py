import pandas as pd
import numpy as np

data_aset = {
    'Asset_ID': ['AST-001', 'AST-002', 'AST-003', 'AST-004', 'AST-005'],
    'Jenis_Aset': ['Pipa Air', 'Tiang Listrik', 'Penerangan Jalan', 'Pipa Air', 'Saluran Drainase'],
    'Lat': [-3.7928, -3.7950, -3.8001, -3.7890, -3.7915],
    'Lon': [102.2608, 102.2650, 102.2700, 102.2580, 102.2620],
    'Kondisi_Fisik': ['Rusak Ringan', 'Baik', 'Rusak Berat', 'Baik', 'Rusak Berat']
}

df_aset = pd.DataFrame(data_aset)

ZONA_RISIKO_LAT = -3.7920
ZONA_RISIKO_LON = 102.2610

def hitung_jarak_spasial(lat1, lon1, lat2, lon2):
    jarak = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111  
    return round(jarak, 2) 

print("--- PROSES ANALISIS SPASIAL ASET INFRASTRUKTUR ---")

df_aset['Jarak_Ke_Zona_Risiko_KM'] = df_aset.apply(
    lambda row: hitung_jarak_spasial(row['Lat'], row['Lon'], ZONA_RISIKO_LAT, ZONA_RISIKO_LON), 
    axis=1
)

def tentukan_prioritas(row):
    if row['Kondisi_Fisik'] == 'Rusak Berat' and row['Jarak_Ke_Zona_Risiko_KM'] < 1.5:
        return 'PRIORITAS UTAMA (URGENT)'
    elif row['Kondisi_Fisik'] == 'Rusak Berat' or row['Jarak_Ke_Zona_Risiko_KM'] < 1.0:
        return 'PRIORITAS SEDANG'
    else:
        return 'RUTIN / MONITORING'

df_aset['Status_Pemeliharaan'] = df_aset.apply(tentukan_prioritas, axis=1)

print(df_aset[['Asset_ID', 'Jenis_Aset', 'Kondisi_Fisik', 'Jarak_Ke_Zona_Risiko_KM', 'Status_Pemeliharaan']])