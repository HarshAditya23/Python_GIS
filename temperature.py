import pandas as pd


def transform(region, n_bands):
    df = pd.DataFrame(region)
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df = df[['longitude', 'latitude', 'time', *n_bands]].dropna()
    for band in n_bands:
        df[band] = pd.to_numeric(df[band], errors='coerce')
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')
    df = df[['time', 'datetime',  *n_bands]]
    return df


def temperture_conversion(t_modis):
    t_celsius = 0.02 * t_modis - 273.15
    return t_celsius


def utfvi_calculation(cal_fx):
    for i in cal_fx:
        cal_fx = (cal_fx - cal_fx.mean()) / cal_fx.mean()
