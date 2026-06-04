import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# File definitions: (filename, legend label)
files = [
    ('WingTaper/TaperPlane0_2_T1-50_0 m_s-VLM2.txt', 'Taper = 0.2'),
    ('WingTaper/TaperPlane0_3_T1-50_0 m_s-VLM2.txt', 'Taper = 0.3'),
    ('WingTaper/TaperPlane0_4_T1-50_0 m_s-VLM2.txt', 'Taper = 0.4'),
    ('WingTaper/TaperPlane0_5_T1-50_0 m_s-VLM2.txt', 'Taper = 0.5'),
    ('WingTaper/TaperPlane0_6_T1-50_0 m_s-VLM2.txt', 'Taper = 0.6'),
    ('WingTaper/TaperPlane0_7_T1-50_0 m_s-VLM2.txt', 'Taper = 0.7'),
    ('WingTaper/TaperPlane0_8_T1-50_0 m_s-VLM2.txt', 'Taper = 0.8'),
    ('WingTaper/TaperPlane0_9_T1-50_0 m_s-VLM2.txt', 'Taper = 0.9'),
    ('WingTaper/TaperPlane1_0_T1-50_0 m_s-VLM2.txt', 'Taper = 1.0'),
    ('WingTaper/Y2P_T1-50_0 m_s-VLM2.txt',             'Y2P'),
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
fig.suptitle('Wing Taper Aerodynamic Comparison', fontsize=18, fontweight='bold')

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
print(f"\n{'Label':<22} {'CLmax':>8} {'@ alpha':>9} {'Max L/D':>9} {'@ alpha':>9} {'Max CL³/CD²':>13} {'@ alpha':>9}")
print("-" * 86)
summary_rows = []
for label, df in dataframes.items():
    Taper = np.nan
    if label.startswith('Taper ='):
        try:
            Taper = float(label.split('=')[1].strip())
        except (ValueError, IndexError):
            Taper = np.nan

    max_cl = df['CL'].max()
    a_max_cl = df.loc[df['CL'].idxmax(), 'alpha']

    LD = df['CL'] / df['CD']
    pos = LD[LD > 0]
    max_ld   = pos.max()
    a_max_ld = df.loc[pos.idxmax(), 'alpha']

    pos3 = df['CL3_CD2'][df['CL3_CD2'] > 0]
    max_e   = pos3.max()
    a_max_e = df.loc[pos3.idxmax(), 'alpha']

    summary_rows.append({
        'label': label,
        'Taper': Taper,
        'clmax': max_cl,
        'alpha_clmax': a_max_cl,
        'max_ld': max_ld,
        'alpha_max_ld': a_max_ld,
        'max_cl3_cd2': max_e,
        'alpha_max_cl3_cd2': a_max_e,
    })

    print(f"{label:<22} {max_cl:>8.3f} {a_max_cl:>8.2f}° {max_ld:>9.2f} {a_max_ld:>8.2f}° {max_e:>13.2f} {a_max_e:>8.2f}°")

# ── Figure: Summary points vs Taper angle ─────────────────────────────────────
summary_df = pd.DataFrame(summary_rows)
Taper_df = summary_df.dropna(subset=['Taper']).sort_values('Taper')

if not Taper_df.empty:
    fig_Taper, axes_Taper = plt.subplots(2, 3, figsize=(18, 10))
    fig_Taper.suptitle('Peak Metrics vs Wing Taper', fontsize=18, fontweight='bold')

    ax1, ax2, ax3, ax4, ax5, ax6 = axes_Taper.ravel()

    ax1.plot(Taper_df['Taper'], Taper_df['clmax'], marker='o', linewidth=2)
    ax1.set_title('CLmax vs Taper', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Taper (°)')
    ax1.set_ylabel('CLmax')
    ax1.grid(True, alpha=0.3)

    ax2.plot(Taper_df['Taper'], Taper_df['alpha_clmax'], marker='o', linewidth=2)
    ax2.set_title('Alpha @ CLmax vs Taper', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Taper (°)')
    ax2.set_ylabel('Alpha @ CLmax (°)')
    ax2.grid(True, alpha=0.3)

    ax3.plot(Taper_df['Taper'], Taper_df['max_ld'], marker='o', linewidth=2)
    ax3.set_title('Max L/D vs Taper', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Taper (°)')
    ax3.set_ylabel('Max L/D')
    ax3.grid(True, alpha=0.3)

    ax4.plot(Taper_df['Taper'], Taper_df['alpha_max_ld'], marker='o', linewidth=2)
    ax4.set_title('Alpha @ Max L/D vs Taper', fontsize=13, fontweight='bold')
    ax4.set_xlabel('Taper (°)')
    ax4.set_ylabel('Alpha @ Max L/D (°)')
    ax4.grid(True, alpha=0.3)

    ax5.plot(Taper_df['Taper'], Taper_df['max_cl3_cd2'], marker='o', linewidth=2)
    ax5.set_title('Max CL³/CD² vs Taper', fontsize=13, fontweight='bold')
    ax5.set_xlabel('Taper (°)')
    ax5.set_ylabel('Max CL³/CD²')
    ax5.grid(True, alpha=0.3)

    ax6.plot(Taper_df['Taper'], Taper_df['alpha_max_cl3_cd2'], marker='o', linewidth=2)
    ax6.set_title('Alpha @ Max CL³/CD² vs Taper', fontsize=13, fontweight='bold')
    ax6.set_xlabel('Taper (°)')
    ax6.set_ylabel('Alpha @ Max CL³/CD² (°)')
    ax6.grid(True, alpha=0.3)

    fig_Taper.tight_layout(rect=[0, 0, 1, 0.96])

non_Taper = summary_df[summary_df['Taper'].isna()]['label'].tolist()
if non_Taper:
    print(f"\nNote: Excluded non-numeric Taper cases from Taper plots: {', '.join(non_Taper)}")

plt.show()
