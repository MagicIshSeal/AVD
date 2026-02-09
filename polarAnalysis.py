import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from InitCalc import Clci, mTo, S, rho

# Use cruise values (last element of arrays from InitCalc)
S_cruise = S[-1] if isinstance(S, np.ndarray) else S

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
    # Add CL^3/CD^2 column
    df['CL3_CD2'] = (df['CL']**3) / (df['CD']**2)
    # Extract airfoil name from filename
    airfoil_name = file.split('_T1')[0]
    dataframes[airfoil_name] = df
    print(f"\n{airfoil_name}:")
    print(df.head())


def plot_airfoil_comparisons(dataframes, Clci):
    """
    Create comprehensive comparison plots for airfoil performance data.
    Split into two windows for better visibility.
    """
    # Define colors for consistency
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
    
    # Find alpha values where CL = Clci for each airfoil
    clci_intercepts = {}
    for (name, df), color in zip(dataframes.items(), colors):
        alpha_at_clci = np.interp(Clci, df['CL'], df['alpha'])
        LD = df['CL'] / df['CD']
        LD_at_clci = np.interp(alpha_at_clci, df['alpha'], LD)
        clci_intercepts[name] = {
            'alpha': alpha_at_clci,
            'LD': LD_at_clci,
            'color': color
        }
    
    # ===== FIGURE 1: Aerodynamic Characteristics (2x2) =====
    fig1 = plt.figure(figsize=(16, 12))
    fig1.suptitle('Airfoil Aerodynamic Characteristics', fontsize=18, fontweight='bold', y=0.98)
    gs1 = fig1.add_gridspec(2, 2, hspace=0.25, wspace=0.25, left=0.08, right=0.95, top=0.93, bottom=0.06)
    
    ax1 = fig1.add_subplot(gs1[0, 0])
    ax2 = fig1.add_subplot(gs1[0, 1])
    ax3 = fig1.add_subplot(gs1[1, 0])
    ax4 = fig1.add_subplot(gs1[1, 1])
    
    # Plot 1: CL vs Alpha
    for (name, df), color in zip(dataframes.items(), colors):
        ax1.plot(df['alpha'], df['CL'], label=name, linewidth=2.5, color=color)
    ax1.axhline(y=Clci, color='red', linestyle='--', linewidth=2.5, label=f'Clci = {Clci:.3f}')
    ax1.set_xlabel('Angle of Attack (°)', fontsize=13)
    ax1.set_ylabel('Lift Coefficient (CL)', fontsize=13)
    ax1.set_title('CL vs Alpha', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(labelsize=11)
    
    # Plot 2: Drag Polar (CL vs CD)
    for (name, df), color in zip(dataframes.items(), colors):
        ax2.plot(df['CD'], df['CL'], label=name, linewidth=2.5, color=color)
    ax2.axhline(y=Clci, color='red', linestyle='--', linewidth=2.5, label=f'Clci = {Clci:.3f}')
    ax2.set_xlabel('Drag Coefficient (CD)', fontsize=13)
    ax2.set_ylabel('Lift Coefficient (CL)', fontsize=13)
    ax2.set_title('Drag Polar (CL vs CD)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(labelsize=11)
    
    # Plot 3: L/D vs Alpha with Clci intercept lines
    for (name, df), color in zip(dataframes.items(), colors):
        LD = df['CL'] / df['CD']
        ax3.plot(df['alpha'], LD, label=name, linewidth=2.5, color=color)
    
    for name, data in clci_intercepts.items():
        ax3.axvline(x=data['alpha'], color=data['color'], linestyle=':', linewidth=2.5, alpha=0.7,
                    label=f"{name.split()[0]} @ Clci: α={data['alpha']:.1f}°, L/D={data['LD']:.1f}")
    
    ax3.set_xlabel('Angle of Attack (°)', fontsize=13)
    ax3.set_ylabel('L/D Ratio', fontsize=13)
    ax3.set_title('L/D vs Alpha', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=9.5, ncol=2)
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(labelsize=11)
    
    # Plot 4: Moment Coefficient vs Alpha
    for (name, df), color in zip(dataframes.items(), colors):
        ax4.plot(df['alpha'], df['Cm'], label=name, linewidth=2.5, color=color)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax4.set_xlabel('Angle of Attack (°)', fontsize=13)
    ax4.set_ylabel('Moment Coefficient (Cm)', fontsize=13)
    ax4.set_title('Cm vs Alpha', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(labelsize=11)
    
    # ===== FIGURE 2: Performance Metrics (1x2) =====
    fig2 = plt.figure(figsize=(16, 6))
    fig2.suptitle('Airfoil Performance Metrics', fontsize=18, fontweight='bold', y=0.98)
    gs2 = fig2.add_gridspec(1, 2, hspace=0.25, wspace=0.25, left=0.08, right=0.95, top=0.88, bottom=0.12)
    
    ax5 = fig2.add_subplot(gs2[0, 0])
    ax6 = fig2.add_subplot(gs2[0, 1])
    
    # Plot 5: CL³/CD² vs Alpha
    for (name, df), color in zip(dataframes.items(), colors):
        # Filter for positive CL³/CD² values only
        mask = df['CL3_CD2'] > 0
        ax5.plot(df.loc[mask, 'alpha'], df.loc[mask, 'CL3_CD2'], label=name, linewidth=2.5, color=color)
    ax5.set_xlabel('Angle of Attack (°)', fontsize=13)
    ax5.set_ylabel('CL³/CD² (Endurance Parameter)', fontsize=13)
    ax5.set_title('CL³/CD² vs Alpha', fontsize=14, fontweight='bold')
    ax5.legend(fontsize=11)
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(labelsize=11)
    
    # Plot 6: L/D Ratio comparison (alternative view)
    for (name, df), color in zip(dataframes.items(), colors):
        LD = df['CL'] / df['CD']
        mask = LD > 0  # Only show positive L/D
        ax6.plot(df.loc[mask, 'CL'], LD[mask], label=name, linewidth=2.5, color=color)
    ax6.set_xlabel('Lift Coefficient (CL)', fontsize=13)
    ax6.set_ylabel('L/D Ratio', fontsize=13)
    ax6.set_title('L/D vs CL', fontsize=14, fontweight='bold')
    ax6.legend(fontsize=11)
    ax6.grid(True, alpha=0.3)
    ax6.tick_params(labelsize=11)
    
    plt.show()
    
    return clci_intercepts


def print_statistics(dataframes, clci_intercepts, Clci):
    """
    Print comprehensive statistics for all airfoils.
    """
    print("\n" + "="*70)
    print("AIRFOIL COMPARISON STATISTICS")
    print("="*70)
    
    for name, df in dataframes.items():
        LD = df['CL'] / df['CD']
        max_LD = LD.max()
        max_LD_alpha = df.loc[LD.idxmax(), 'alpha']
        max_CL = df['CL'].max()
        max_CL_alpha = df.loc[df['CL'].idxmax(), 'alpha']
        max_CL3_CD2 = df['CL3_CD2'].max()
        max_CL3_CD2_alpha = df.loc[df['CL3_CD2'].idxmax(), 'alpha']

        
        # Calculate RCmax using max CL3_CD2
        S_cruise_val = S[-1] if isinstance(S, np.ndarray) else S
        RC_max = np.sqrt(((mTo*9.81)/S_cruise_val) * (2/rho) * (1/max_CL3_CD2))
        
        print(f"\n{name}:")
        print(f"  Max L/D: {max_LD:.2f} at alpha = {max_LD_alpha:.2f}°")
        print(f"  Max CL: {max_CL:.4f} at alpha = {max_CL_alpha:.2f}°")
        print(f"  Max CL³/CD²: {max_CL3_CD2:.2f} at alpha = {max_CL3_CD2_alpha:.2f}°")
        print(f"  RCmax (at max CL³/CD²): {RC_max:.3f} m/s")
        print(f"  At Clci ({Clci:.3f}): alpha = {clci_intercepts[name]['alpha']:.2f}°, L/D = {clci_intercepts[name]['LD']:.2f}")


# Generate plots and statistics
clci_intercepts = plot_airfoil_comparisons(dataframes, Clci)
print_statistics(dataframes, clci_intercepts, Clci)