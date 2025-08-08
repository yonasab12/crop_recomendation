import pandas as pd

def feature_engineer(df):
    df = df.copy()
    # EXACT calculations from notebook
    df['NPK'] = (df['N'] + df['P'] + df['K']) / 3
    df['THI'] = df['temperature'] * df['humidity'] / 100
    df['rainfall_level'] = pd.cut(
        df['rainfall'],
        bins=[0, 50, 100, 200, 300],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    df['ph_category'] = df['ph'].apply(
        lambda x: 'Acidic' if x < 5.5 else 'Neutral' if x <= 7.5 else 'Alkaline'
    )
    df['temp_rain_interaction'] = df['temperature'] * df['rainfall']
    df['ph_rain_interaction'] = df['ph'] * df['rainfall']
    
    # Maintain EXACT column order
    return df[[
        'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
        'NPK', 'THI', 'rainfall_level', 'ph_category',
        'temp_rain_interaction', 'ph_rain_interaction'
    ]]