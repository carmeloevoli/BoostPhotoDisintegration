from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
import ast
import matplotlib.cm as cm
import numpy as np 
import subprocess

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

nuclei = np.array([[16, 8], [28, 14], [56, 26], [195, 78]])
nucleiList = np.array([[14, 7], [28, 14], [56, 26]])

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
def select_color(A, Z):

    colorList = ['#d6301f', '#2c8bbd', '#87419c']
     
    for i in range(len(colorList)):
        if A == nucleiList[i][0] and Z == nucleiList[i][1]:
            break 

    return colorList[i]

# ----------------------------------------------------------------------------------------------------
def select_anchored_text(A, Z):
     
    nuclei = [r'$^{14}$N', r'$^{28}$Si', r'$^{56}$Fe']

    for i in range(len(nuclei)):
        if A == nucleiList[i][0] and Z == nucleiList[i][1]:
            break 

    return nuclei[i]

# ----------------------------------------------------------------------------------------------------
def get_legend(A, Z):

    elements = {
        1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 
        11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 
        20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 
        29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 
        38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 
        47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 
        56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 
        65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta', 
        74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb'
    }    
    
    return r'$^{{{}}}${}'.format(A, elements.get(Z))

# ----------------------------------------------------------------------------------------------------
def get_color(A, Z):

    color = cm.plasma(np.linspace(0, 1, 10))
                     
    if A == 16 and Z == 8:
        return color[2]
    elif A == 28 and Z == 14:
        return color[4]
    elif A == 56 and Z == 26:
        return color[6]
    elif A == 195 and Z == 78:
        return color[8]

# ----------------------------------------------------------------------------------------------------
def plot_cross_section_v2r4_vs_TENDL2023(A, Z):

    eps_TENDL2023, cross_section_TENDL2023 = execute_get_cross_section_TENDL2023(A, Z)
    mask_TENDL2023 = cross_section_TENDL2023 > 0
    eps_TENDL2023 = eps_TENDL2023[mask_TENDL2023]
    cross_section_TENDL2023 = cross_section_TENDL2023[mask_TENDL2023]

    eps_v2r4 = execute_get_cross_section_v2r4(A, Z, 'N')[0]
    cross_section_v2r4 = execute_get_cross_section_v2r4(A, Z, 'N')[1] + execute_get_cross_section_v2r4(A, Z, 'alpha')[1]
    mask_v2r4 = cross_section_v2r4 > 0
    eps_v2r4 = eps_v2r4[mask_v2r4]
    cross_section_v2r4 = cross_section_v2r4[mask_v2r4] 

    color = select_color(A, Z)

    plt.figure()
    plt.plot(eps_TENDL2023, cross_section_TENDL2023, color = color, ls = '-', label = 'TENDL-2023')
    plt.plot(eps_v2r4, cross_section_v2r4, color = 'k', ls = '--', label = 'Model 4 from SimProp v2r4')
    
    at = AnchoredText('{0}'.format(select_anchored_text(A, Z)), loc = 'upper right', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)	
    
    plt.ylim(bottom = 1.e-1) 
    plt.yscale('log')
    plt.xlabel(r"Photon energy$'\: \rm [MeV]$")
    plt.ylabel(r'Nonelastic cross section$\: \rm [mb]$')
    plt.legend(loc = 'lower right')
    plt.savefig('../figures/cross-sections/cross_section_v2r4_vs_TENDL2023_A{0:03}Z{1:03}.pdf'.format(int(A), int(Z)), bbox_inches = 'tight')
    plt.savefig('../figures/cross-sections/cross_section_v2r4_vs_TENDL2023_A{0:03}Z{1:03}.png'.format(int(A), int(Z)), bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_cross_section_TENDL2023():
     
    plt.figure()

    for nucleus in nuclei:

        A = nucleus[0]
        Z = nucleus[1]
         
        eps_TENDL2023, cross_section_TENDL2023 = execute_get_cross_section_TENDL2023(A, Z)
        mask_TENDL2023 = cross_section_TENDL2023 > 0
        eps_TENDL2023 = eps_TENDL2023[mask_TENDL2023]
        cross_section_TENDL2023 = cross_section_TENDL2023[mask_TENDL2023]

        plt.plot(eps_TENDL2023, cross_section_TENDL2023, color = get_color(A, Z), label = '{}'.format(get_legend(A, Z)))
    
    plt.ylim(bottom = 1.e-1) 
    plt.yscale('log')
    plt.xlabel(r"Photon energy$'\: \rm [MeV]$")
    plt.ylabel(r'Nonelastic cross section$\: \rm [mb]$')
    plt.legend(title = r'Nucleus')
    plt.savefig('../figures/cross-sections/cross_sections_TENDL2023.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/cross-sections/cross_sections_TENDL2023.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_all_cross_sections_TENDL2023():
    
    nucleiList = [[7, 3], [9, 4], [11, 5], [12, 6], [14, 7], [16, 8], [19, 9], [20, 10],
                  [23, 11], [24, 12], [27, 13], [28, 14], [31, 15], [32, 16], [35, 17], [40, 18], 
                  [39, 19], [40, 20], [45, 21], [48, 22], [51, 23], [52, 24], [55, 25], [56, 26]]
    
    A_values = [nucleus[0] for nucleus in nucleiList]
    A_min, A_max = min(A_values), max(A_values)

    fig, ax = plt.subplots()

    for inuclei in range(len(nucleiList)):
        A = int(nucleiList[inuclei][0])
        Z = int(nucleiList[inuclei][1])
        
        color_value = (A - A_min) / (A_max - A_min)
        color = cm.viridis(color_value)
        
        eps, cross_section = execute_get_cross_section_TENDL2023(A, Z)        
        mask = cross_section > 0
        eps = eps[mask]
        cross_section = cross_section[mask]

        ax.plot(eps, cross_section, color = color)

    ax.set_ylim(bottom = 1.e-1)
    ax.set_yscale('log')
    ax.set_xlabel(r"Photon energy$\: \rm [MeV]$")
    ax.set_ylabel(r'Nonelastic cross section$\: \rm [mb]$')
    
    sm = cm.ScalarMappable(cmap = 'viridis', norm = plt.Normalize(A_min, A_max))
    sm.set_array([])
    fig.colorbar(sm, ax = ax, label = r'Mass number, $A$')

    plt.savefig('../figures/cross-sections/all_cross_sections_TENDL2023.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/cross-sections/all_cross_sections_TENDL2023.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # inucleus = 2
    # plot_cross_section_v2r4_vs_TENDL2023(nucleiList[inucleus][0], nucleiList[inucleus][1])

    # plot_all_cross_sections_TENDL2023()

    plot_cross_section_TENDL2023()

# ----------------------------------------------------------------------------------------------------
