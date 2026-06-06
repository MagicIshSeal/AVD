import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dydx(y1, y2, x1, x2):
    return (y2-y1)/(x2-x1)

ref = pd.read_csv('morecsv/reference.csv', skiprows=5)
closer = pd.read_csv('morecsv/longer_tail_chord.csv', skiprows=5)

cm = pd.read_csv('Tain/Cm_a_2.csv')

print(cm.head())
cm.drop(' Alpha.1')
cm.plot()
print(cm.head())
plt.show()

dfs = {"ref": ref, "Bigger Chord": closer}

for df_name, df in dfs.items():
    df['rad'] = np.radians(df['alpha'])
    dCddA = dydx(df[' CD'].iloc[0], df[' CD'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    dCldA = dydx(df[' CL'].iloc[0], df[' CL'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    dCmdA = dydx(df[' Cm'].iloc[0], df[' Cm'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    print(f"{df_name}: Cd_a = {dCddA:2f}, Cl_a = {dCldA:2f}, Cm_a = {dCmdA:2f}")
    idx = abs(df['alpha']).idxmin() 
    print(f"{df_name}: Cd_0 = {df[' CD'].iloc[idx]:2f}, Cl_0 = {df[' CL'].iloc[idx]:2f}, Cm_0 = {df[' Cm'].iloc[idx]:2f}")