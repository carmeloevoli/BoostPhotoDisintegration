from matplotlib import lines
from matplotlib import pyplot as plt
from matplotlib.pylab import cm
import numpy as np 

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

km = 1.e3      # m
Mpc = 3.086e22 # m

c = 299792458      # m/s
mp = 1.e9          # 1 GeV 
H0 = 70 * km / Mpc # 1/s

nuclei = np.array([[16, 8], [28, 14], [56, 26]])
nucleus_Pt = [195, 78]
xs_models = ['v2r4', 'TENDL-2023']

# Investigate why negative values of interaction length are appearing for the case of 28Si using TENDL-2023
# Add a second y-axis with a comparison of distances to known astrophysical objects

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
def get_color_inverted_colors(A, Z):

    if A == 16 and Z == 8:
        return '#FFD700'
    elif A == 28 and Z == 14:
        return '#FFA500'
    elif A == 56 and Z == 26:
        return '#40E0D0'
    elif A == 195 and Z == 78:
        return '#D3D3D3'

# ----------------------------------------------------------------------------------------------------
def plot_interaction_length():

    plt.figure()
    plt.axhline(c/H0/Mpc, color = 'gray', ls = ':') # Adiabatic losses

    for xs_model in xs_models:

        for nucleus in nuclei:

            A, Z = nucleus
            data = np.loadtxt('../runs/files/lambda/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, xs_model))
            E = data[:,0]
            interaction_length = data[:,1]

            if xs_model == 'v2r4':
                plt.plot(np.log10(E), interaction_length, color = get_color(A, Z), ls = '--')

            elif xs_model == 'TENDL-2023':
                if A == 28 and Z == 14:
                    mask = interaction_length >= 0 
                    E = E[mask]
                    interaction_length = interaction_length[mask]
                plt.plot(np.log10(E), interaction_length, color = get_color(A, Z), ls = '-', label = '{}'.format(get_legend(A, Z)))               

    data = np.loadtxt('../runs/files/lambda/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(nucleus_Pt[0], nucleus_Pt[1], xs_models[1]))
    E = data[:,0]
    interaction_length = data[:,1]
    plt.plot(np.log10(E), interaction_length, color = get_color(nucleus_Pt[0], nucleus_Pt[1]), ls = '-', label = '{}'.format(get_legend(nucleus_Pt[0], nucleus_Pt[1])))
    print()

    TENDL2023 = lines.Line2D([], [], color = 'black', ls = '-', label = 'TENDL-2023')
    v2r4 = lines.Line2D([], [], color = 'black', ls = '--', label = 'SimProp v2r4')
    lgnd = plt.legend(title = 'Cross section', handles = [TENDL2023, v2r4], frameon = True, loc = 'lower left')	
    plt.gca().add_artist(lgnd)

    plt.yscale('log')
    plt.ylim(top = 1.e4)
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    plt.ylabel(r'Interaction length$\: \rm [Mpc]$')
    plt.legend(title = 'Nucleus', loc = 'lower left', bbox_to_anchor = (0., 0.234))
    plt.grid()
    plt.savefig('../runs/figures/interactionLength.pdf', bbox_inches = 'tight')
    plt.savefig('../runs/figures/interactionLength.png', bbox_inches = 'tight', dpi = 600)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_interaction_length_inverted_colors(): # Write the code

    plt.figure()
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_interaction_length()

# ----------------------------------------------------------------------------------------------------
