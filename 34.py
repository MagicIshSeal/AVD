import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dydx(y1, y2, x1, x2):
    return (y2-y1)/(x2-x1)

cd = pd.read_csv('.\\csv\\Cd.csv')
cl = pd.read_csv('.\\csv\\Cl.csv')
cm = pd.read_csv('.\\csv\\Cm.csv')

dfs = {"cd": cd, "cl": cl, "cm": cm}

for df_name, df in dfs.items():
    df['rad'] = np.radians(df['Alpha'])
    df_alpha = dydx(df['T1-50.0 m/s-VLM1+Drag'].iloc[0], df['T1-50.0 m/s-VLM1+Drag'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    print(f"{df_name}_0: {df['T1-50.0 m/s-VLM1+Drag'].iloc[0]}")
    print(f"{df_name}_alpha: {df_alpha}\n")
    df.plot(x='rad', y='T1-50.0 m/s-VLM1+Drag', label=df_name)
    plt.show()