import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dydx(y1, y2, x1, x2):
    return (y2-y1)/(x2-x1)

ref = pd.read_csv('morecsv\\Alt_Iyy_OG_Cg.csv', skiprows=5)
closer = pd.read_csv('morecsv\\Alt_Iyy_0.209_Cg.csv', skiprows=5)


w = 425*9.81
dfs = {"ref": ref}

for df_name, df in dfs.items():
    df['rad'] = np.radians(df['alpha'])
    dCddA = dydx(df[' CD'].iloc[0], df[' CD'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    dCldA = dydx(df[' CL'].iloc[0], df[' CL'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    dCmdA = dydx(df[' Cm'].iloc[0], df[' Cm'].iloc[-1], df['rad'].iloc[0], df['rad'].iloc[-1])
    df['CL/CD'] = df[' CL'] / df[' CD']
    df['CL3/CD2'] = df[' CL']**3 / df[' CD']**2
    plots = ['CL/CD', ' CL', ' Cm', 'CL3/CD2']
    df['l'] = df[' CL'] *0.5*1.1*(50**2) * 6
    diff =abs(w - df['l'])
    min = diff.argmin()
    print(f"Cl/Cd cruise: {df[' CL'].iloc[min]:2f}, Cd cruise: {df[' CD'].iloc[min]:2f}, alpha cruise: {df['alpha'].iloc[min]:2f}")
    for plot in plots:
        print(f"{df_name} {plot} max: {df[plot].max()}")
        plt.figure()
        plt.plot(df['alpha'], df[plot], label=plot)
        plt.xlabel('Angle of Attack (degrees)')
        plt.ylabel(plot)
        plt.legend()
        plt.title(f"{plot} vs Alpha")
        plt.grid()
        #renmove slashes from string if there are any
        plot = plot.replace('/', '_')
        plt.savefig(f"{df_name}_{plot}.png")
    
    #print(f"{df_name}: Cd_a = {dCddA:2f}, Cl_a = {dCldA:2f}, Cm_a = {dCmdA:2f}")
    #idx = abs(df['alpha']).idxmin() 
    #print(f"{df_name}: Cd_0 = {df[' CD'].iloc[idx]:2f}, Cl_0 = {df[' CL'].iloc[idx]:2f}, Cm_0 = {df[' Cm'].iloc[idx]:2f}")
    