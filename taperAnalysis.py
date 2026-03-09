import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# File definitions: (filename, legend label)
files = [
    ('WingTaper/TaperPlane0_2_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.2'),
    ('WingTaper/TaperPlane0_3_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.3'),
    ('WingTaper/TaperPlane0_4_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.4'),
    ('WingTaper/TaperPlane0_5_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.5'),
    ('WingTaper/TaperPlane0_6_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.6'),
    ('WingTaper/TaperPlane0_7_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.7'),
    ('WingTaper/TaperPlane0_8_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.8'),
    ('WingTaper/TaperPlane0_9_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 0.9'),
    ('WingTaper/TaperPlane1_0_T1-50_0 m_s-VLM2.txt', 'Taper Ratio = 1.0'),
    ('WingTaper/Y2P_T1-50_0 m_s-VLM2.txt',            'Y2P'),
]

# Column names from the xflr5 VLM2 output
col_names = ['alpha', 'Beta', 'CL', 'CDi', 'CDv', 'CD',
             'CY', 'Cl', 'Cm', 'Cn', 'Cni', 'QInf', 'XCP']

# Resolve paths relative to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

dataframes = {}
for fname, label in files:
    fpath = os.path.join(script_dir, fname)
    df = pd.read_csv(fpath, sep=r'\s+', skiprows=8, names=col_names)
    df = df.apply(pd.to_numeric, errors='coerce').dropna(subset=['alpha', 'CL', 'CD'])
    df['CL3_CD2'] = (df['CL'] ** 3) / (df['CD'] ** 2)
    dataframes[label] = df

# Distinct colours for up to 10 curves
colors = cm.tab10(np.linspace(0, 1, len(dataframes)))

# ── Figure: 2×2 comparison plots ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Wing Taper Ratio Aerodynamic Comparison', fontsize=18, fontweight='bold')

ax_cl_alpha  = axes[0, 0]   # CL vs alpha
ax_cd_alpha  = axes[0, 1]   # CD vs alpha
ax_ld_alpha  = axes[1, 0]   # CL/CD vs alpha
ax_end_alpha = axes[1, 1]   # CL³/CD² vs alpha

for (label, df), color in zip(dataframes.items(), colors):
    LD = df['CL'] / df['CD']
    mask_ld  = LD > 0
    mask_end = df['CL3_CD2'] > 0

    ax_cl_alpha.plot(df['alpha'], df['CL'],                       label=label, linewidth=2, color=color)
    ax_cd_alpha.plot(df['alpha'], df['CD'],                       label=label, linewidth=2, color=color)
    ax_ld_alpha.plot(df.loc[mask_ld,  'alpha'], LD[mask_ld],     label=label, linewidth=2, color=color)
    ax_end_alpha.plot(df.loc[mask_end, 'alpha'], df.loc[mask_end, 'CL3_CD2'],
                      label=label, linewidth=2, color=color)

# CL vs Alpha
ax_cl_alpha.set_xlabel('Angle of Attack (°)', fontsize=13)
ax_cl_alpha.set_ylabel('Lift Coefficient (CL)', fontsize=13)
ax_cl_alpha.set_title('CL vs Alpha', fontsize=14, fontweight='bold')
ax_cl_alpha.legend(fontsize=10)
ax_cl_alpha.grid(True, alpha=0.3)
ax_cl_alpha.tick_params(labelsize=11)

# CD vs Alpha
ax_cd_alpha.set_xlabel('Angle of Attack (°)', fontsize=13)
ax_cd_alpha.set_ylabel('Drag Coefficient (CD)', fontsize=13)
ax_cd_alpha.set_title('CD vs Alpha', fontsize=14, fontweight='bold')
ax_cd_alpha.legend(fontsize=10)
ax_cd_alpha.grid(True, alpha=0.3)
ax_cd_alpha.tick_params(labelsize=11)

# CL/CD vs Alpha
ax_ld_alpha.set_xlabel('Angle of Attack (°)', fontsize=13)
ax_ld_alpha.set_ylabel('L/D Ratio (CL/CD)', fontsize=13)
ax_ld_alpha.set_title('CL/CD vs Alpha', fontsize=14, fontweight='bold')
ax_ld_alpha.legend(fontsize=10)
ax_ld_alpha.grid(True, alpha=0.3)
ax_ld_alpha.tick_params(labelsize=11)

# CL³/CD² vs Alpha
ax_end_alpha.set_xlabel('Angle of Attack (°)', fontsize=13)
ax_end_alpha.set_ylabel('CL³/CD²', fontsize=13)
ax_end_alpha.set_title('CL³/CD² vs Alpha', fontsize=14, fontweight='bold')
ax_end_alpha.legend(fontsize=10)
ax_end_alpha.grid(True, alpha=0.3)
ax_end_alpha.tick_params(labelsize=11)

fig.tight_layout(rect=[0, 0, 1, 0.96])

# ── Print peak performance table ──────────────────────────────────────────────
print(f"\n{'Label':<22} {'Max L/D':>9} {'@ alpha':>9} {'Max CL³/CD²':>13} {'@ alpha':>9}")
print("-" * 65)
for label, df in dataframes.items():
    LD = df['CL'] / df['CD']
    pos = LD[LD > 0]
    max_ld   = pos.max()
    a_max_ld = df.loc[pos.idxmax(), 'alpha']

    pos3 = df['CL3_CD2'][df['CL3_CD2'] > 0]
    max_e   = pos3.max()
    a_max_e = df.loc[pos3.idxmax(), 'alpha']

    print(f"{label:<22} {max_ld:>9.2f} {a_max_ld:>8.2f}° {max_e:>13.2f} {a_max_e:>8.2f}°")

plt.show()
