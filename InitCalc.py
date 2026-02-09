import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

rho = 1.1117
mu = 1.8e-5
mPay = 85
ar = 10
CLC = 0.5

#Wempty/Wto = 0.5 and Wfuel/Wto = 0.3
#Wto = Wpay + Wempty + Wfuel
#So Wto = Wpay + 0.5*Wto + 0.3*Wto
#Wto = Wpay/0.2
mTo = mPay/0.2
mEmpty = 0.5*mTo
mFuel = 0.3*mTo
print(f"Takeoff Mass: {mTo:.1f} kg")
#Ar = b^2/S
#S = 1/Ar * b^2
#L = Cl *0.5 * rho * V^2 * S
#L = mTo * g
#mTo * g = Cl *0.5 * rho * V^2 * 1/(Ar * b^2)
#Solve for b
#V is a range of possilbe take off speeds
Vcr = 180/3.6
V = np.linspace(50/3.6, Vcr, 100)
S = (mTo*9.81)/(CLC * 0.5 * rho * V**2)
b = np.sqrt(S*ar)
Cmgc = np.sqrt(S/ar)
Re = (rho * V * Cmgc)/mu
print(f"Wing Span at Cruise: {b[-1]:.2f} m")
print(f"Wing Area at Cruise: {S[-1]:.2f} m^2")
print(f"Reynolds Number: {Re[0]:.0f}")

CLCw = CLC /0.95
Clci = CLCw / 0.9
print(f"Clci: {Clci:.3f}")
def plotResults():
    #plot V vs b
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12))
    ax1.plot(V, b)
    ax1.set_xlabel('Takeoff Speed (m/s)')
    ax1.set_ylabel('Wingspan (m)')
    ax1.set_title('Wingspan vs Takeoff Speed')
    ax1.axvline(x=Vcr, color='r', linestyle='--', label='Cruise Speed')
    ax1.legend()
    ax1.grid()

    #plot V vs S
    ax2.plot(V, S)
    ax2.set_xlabel('Takeoff Speed (m/s)')
    ax2.set_ylabel('Wing Area (m^2)')
    ax2.set_title('Wing Area vs Takeoff Speed')
    ax2.axvline(x=Vcr, color='r', linestyle='--', label='Cruise Speed')
    ax2.legend()
    ax2.grid()

    #plot V vs Cmgc
    ax3.plot(V, Cmgc)
    ax3.set_xlabel('Takeoff Speed (m/s)')
    ax3.set_ylabel('Mean Geometric Chord (m)')
    ax3.set_title('Mean Geometric Chord vs Takeoff Speed')
    ax3.axvline(x=Vcr, color='r', linestyle='--', label='Cruise Speed')
    ax3.legend()
    ax3.grid()
    
    #plot V vs Re
    ax4.plot(V, Re)
    ax4.set_xlabel('Takeoff Speed (m/s)')
    ax4.set_ylabel('Reynolds Number')
    ax4.set_title('Reynolds Number vs Takeoff Speed')
    ax4.axvline(x=Vcr, color='r', linestyle='--',
                label='Cruise Speed')
    ax4.legend()
    ax4.grid()
    
    plt.tight_layout()
    plt.show()
plotResults()
