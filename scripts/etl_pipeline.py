import pandas as pd
import numpy as np
import os

def run_etl(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # Clean Data
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.drop(columns=[c for c in ['brent_crude_usd_barrel', 'jet_fuel_usd_barrel_surcharge_policy'] if c in df.columns], inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    if 'surcharge_band' in df.columns: 
        df['surcharge_band'] = df['surcharge_band'].fillna('No Surcharge')
