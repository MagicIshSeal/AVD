import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the three airfoil polar files
files = [
    'CLARK Y AIRFOIL_T1_Re2.392_M0.00_N9.0.txt',
    'EPPLER 748 AIRFOIL_T1_Re2.392_M0.00_N9.0.txt',
    'NASA NLF1 416 AIRFOIL_T1_Re2.392_M0.00_N9.0.txt'
]

# Read data from each file
dataframes = {}
for file in files:
    # Read the file, skipping first 11 lines (headers and separator)
    df = pd.read_csv(file, sep=r'\s+', skiprows=11, 
                     names=['alpha', 'CL', 'CD', 'CDp', 'Cm', 'Top_Xtr', 'Bot_Xtr', 
                            'Cpmin', 'Chinge', 'XCp', 'col11', 'col12'])
    # Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    # Extract airfoil name from filename
    airfoil_name = file.split('_T1')[0]
    dataframes[airfoil_name] = df
    print(f"\n{airfoil_name}:")
    print(df.head())

# Create plots comparing the three airfoils
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: CL vs alpha
for name, df in dataframes.items():
    ax1.plot(df['alpha'], df['CL'], label=name)
ax1.set_xlabel('Angle of Attack (degrees)')
ax1.set_ylabel('Lift Coefficient (CL)')
ax1.set_title('CL vs Alpha')
ax1.legend()
ax1.grid(True)

# Plot 2: CL vs CD (Drag Polar)
for name, df in dataframes.items():
    ax2.plot(df['CD'], df['CL'], label=name)
ax2.set_xlabel('Drag Coefficient (CD)')
ax2.set_ylabel('Lift Coefficient (CL)')
ax2.set_title('Drag Polar (CL vs CD)')
ax2.legend()
ax2.grid(True)

# Plot 3: L/D vs alpha
for name, df in dataframes.items():
    LD = df['CL'] / df['CD']
    ax3.plot(df['alpha'], LD, label=name)
ax3.set_xlabel('Angle of Attack (degrees)')
ax3.set_ylabel('L/D Ratio')
ax3.set_title('L/D vs Alpha')
ax3.legend()
ax3.grid(True)

# Plot 4: Cm vs alpha
for name, df in dataframes.items():
    ax4.plot(df['alpha'], df['Cm'], label=name)
ax4.set_xlabel('Angle of Attack (degrees)')
ax4.set_ylabel('Moment Coefficient (Cm)')
ax4.set_title('Cm vs Alpha')
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.show()

# Print some statistics
print("\n" + "="*60)
print("AIRFOIL COMPARISON STATISTICS")
print("="*60)
for name, df in dataframes.items():
    LD = df['CL'] / df['CD']
    max_LD = LD.max()
    max_LD_alpha = df.loc[LD.idxmax(), 'alpha']
    max_CL = df['CL'].max()
    max_CL_alpha = df.loc[df['CL'].idxmax(), 'alpha']
    
    print(f"\n{name}:")
    print(f"  Max L/D: {max_LD:.2f} at alpha = {max_LD_alpha:.2f}°")
    print(f"  Max CL: {max_CL:.4f} at alpha = {max_CL_alpha:.2f}°")