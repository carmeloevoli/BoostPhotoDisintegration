from matplotlib import pyplot as plt
from scipy.integrate import simps
import ast
import numpy as np 
import subprocess
import sys

c =  299792458       # m/s
hbar = 6.5821220e-16 # eV.s
kB = 8.6173303e-5    # eV/K
T0 = 2.7             # K 

mbarn = 1.e-31 # m^2
Mpc = 3.086e22 # m
MeV = 1.e6     # eV  

# ----------------------------------------------------------------------------------------------------
def execute_get_cross_section_v2r4(A, Z, ipart):

    output = subprocess.run(
        ['python3', 'get_cross_section_v2r4.py', str(A), str(Z), ipart],
        capture_output = True,
        text = True
    )
    
    if output.returncode != 0:
            raise RuntimeError(f'Error executing script: {output.stderr.strip()}')
    
    eps, cross_section = [ast.literal_eval(line) for line in output.stdout.strip().split('\n')]

    return np.array(eps), np.array(cross_section)

# ----------------------------------------------------------------------------------------------------
def execute_get_cross_section_TENDL2023(A, Z):

    output = subprocess.run(
        ['python3', 'get_cross_section_TENDL-2023.py', str(A), str(Z)],
        capture_output = True,
        text = True
    )
    
    if output.returncode != 0:
            raise RuntimeError(f'Error executing script: {output.stderr.strip()}')
    
    eps, cross_section = [ast.literal_eval(line) for line in output.stdout.strip().split('\n')]

    return np.array(eps), np.array(cross_section)

# ----------------------------------------------------------------------------------------------------
def I(eps, Gmm): # CMB

    return -(kB * T0) / (np.pi**2 * (hbar * c)**3) * np.log(1. - np.exp(-(eps)/(2 * Gmm * kB * T0)))

# ----------------------------------------------------------------------------------------------------
# def plot_losses_integral(): # Intermediate step to check results
     
#     eps = np.logspace(-5, 2, num = 100)

#     data_comparison = np.loadtxt('losses_integral_slides.dat')

#     plt.figure()
#     plt.plot(eps, eps * I(eps, 1./2.), color = 'red', label = 'Luciana')
#     plt.plot(data_comparison[:,0], data_comparison[:,1], color = 'k', ls = '--', label = 'Carmelo')
#     plt.xscale('log')
#     plt.yscale('log')
#     plt.ylim([0.1, 1.e13])
#     plt.xlabel(r'$\epsilon \: \rm [eV]$')
#     plt.ylabel(r'$\epsilon I(\epsilon) \: \rm [eV^{-1} m^{-3}]$')
#     plt.legend()
#     plt.show()

# ----------------------------------------------------------------------------------------------------
def interaction_length(A, Z, Gmm, xs_model):

    if xs_model == 'v2r4':
        eps = execute_get_cross_section_v2r4(A, Z, 'N')[0] * MeV
        cross_section = (execute_get_cross_section_v2r4(A, Z, 'N')[1] + execute_get_cross_section_v2r4(A, Z, 'alpha')[1]) * mbarn
        mask = cross_section > 0
        eps = eps[mask]
        cross_section = cross_section[mask]  
         
    elif xs_model == 'TENDL-2023':
        eps, cross_section = execute_get_cross_section_TENDL2023(A, Z)
        mask = cross_section > 0
        eps = eps[mask] * MeV 
        cross_section = cross_section[mask] * mbarn
    
    else: 
        raise ValueError(f"Unknown cross-section model '{xs_model}'. Please use 'v2r4' or 'TENDL-2023'.")

    integrand_interaction_rate = c / (2 * Gmm**2) * eps * cross_section * I(eps, Gmm)
    interaction_rate = simps(integrand_interaction_rate, eps)
    
    return c * A * interaction_rate**-1 / Mpc

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    A = int(sys.argv[1])
    Z = int(sys.argv[2])
    Gmm = float(sys.argv[3])
    xs_model = sys.argv[4] # v2r4 or TENDL-2023

    print(interaction_length(A, Z, Gmm, xs_model))

    # Intermediate steps to check results
    # plot_losses_integral()

# ----------------------------------------------------------------------------------------------------