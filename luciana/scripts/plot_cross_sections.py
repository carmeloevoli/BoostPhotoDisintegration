from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
import ast
import numpy as np
import subprocess

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

FIGURS_DIR = '../figures'
EXFOR_DIR = '../../tables/EXFOR'

Al27_FILES = ['g_Al27_abs_L0122.007.txt', 'g_Al27_abs_L0083.006.txt', 'g_Al27_abs_M0825.010.txt', 'g_Al27_abs_M0188.016.txt'] # 'g_Al27_abs_M0825.011.txt'
O16_FILES = ['g_O16_abs_L0064.004.txt', 'g_O16_abs_L0083.004.txt', 'g_O16_abs_L0122.004.txt']

Al27_LEGENDS = ['Wyckoff et al. 1965', 'Ahrens et al. 1972', 'Ahrens et al. 1975', 'Ahrens et al. 1985']
O16_LEGENDS = ['Bezic et al. 1969', 'Ahrens et al. 1972', 'Wyckoff et al. 1975']

COLORS = ['b', 'g', 'r', 'orange']

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
def get_anchored_text(A, Z):

    if A == 16 and Z == 8:
        return r'$^{16}$O'
    elif A == 27 and Z == 13:
        return r'$^{27}$Al'
    else:
        raise ValueError(f"Nucleus with A = {A} and Z = {Z} not found.") 
    
# ----------------------------------------------------------------------------------------------------
def get_files_and_legends(A, Z):

    if A == 16 and Z == 8:
        return O16_FILES, O16_LEGENDS
    elif A == 27 and Z == 13:
        return Al27_FILES, Al27_LEGENDS
    else:
        raise ValueError(f"Files not available for nucleus with A = {A} and Z = {Z}")

# ----------------------------------------------------------------------------------------------------
def get_nucleus_label(A, Z):

    if A == 16 and Z == 8:
        return '16O'
    elif A == 27 and Z == 13:
        return '27Al'
    else:
        raise ValueError(f"Label not available for nucleus with A = {A} and Z = {Z}")

# ----------------------------------------------------------------------------------------------------
def plot_cross_section_measurements(A, Z):

    files, legends = get_files_and_legends(A, Z)
    
    for i, filename in enumerate(files):
        cross_section_data = np.loadtxt(f"{EXFOR_DIR}/{filename}")

        x_values = cross_section_data[:, 0]  
        y_values = cross_section_data[:, 1]  
        y_errors = cross_section_data[:, 2] 

        color = COLORS[i % len(COLORS)]
        label = legends[i % len(legends)]

        plt.errorbar(x_values, y_values, yerr = y_errors, fmt = 'o', color = color, capsize = 2, elinewidth = 1, markersize = 2, label = label, zorder = -1)

# ----------------------------------------------------------------------------------------------------
def plot_cross_section_TENDL2023(A, Z):

    eps, cross_section = execute_get_cross_section_TENDL2023(A, Z)
    mask = cross_section > 0
    eps = eps[mask]
    cross_section = cross_section[mask]
    plt.plot(eps, cross_section, color = 'k', ls = '-', label = r'TENDL-2023')

# ----------------------------------------------------------------------------------------------------
def plot_cross_section_v2r4(A, Z):

    eps, cross_section = execute_get_cross_section_v2r4(A, Z, 'N')[0], execute_get_cross_section_v2r4(A, Z, 'N')[1] + execute_get_cross_section_v2r4(A, Z, 'alpha')[1]
    mask = cross_section > 0
    eps = eps[mask]
    cross_section = cross_section[mask] 
    plt.plot(eps, cross_section, color = 'k', ls = '--', label = r'SimProp v2r4')

# ----------------------------------------------------------------------------------------------------
def plot_cross_sections(A, Z):

    plot_cross_section_v2r4(A, Z)
    plot_cross_section_TENDL2023(A, Z)
    plot_cross_section_measurements(A, Z)

    at = AnchoredText('{0}'.format(get_anchored_text(A, Z)), loc = 'upper left', frameon = False, prop = {'fontsize': 'x-large'})
    plt.gca().add_artist(at)   

    plt.xlim([0, 50])
    plt.ylim(bottom = 0)
    plt.xlabel(r'Photon energy$\: \rm [MeV]$')
    plt.ylabel(r'Inelastic cross section$\: \rm [mb]$')
    plt.legend()
    plt.savefig(f"{FIGURS_DIR}/cross-sections/cross_sections_{get_nucleus_label(A, Z)}.pdf", bbox_inches = 'tight')
    plt.savefig(f"{FIGURS_DIR}/cross-sections/cross_sections_{get_nucleus_label(A, Z)}.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_cross_sections(16, 8)
    plot_cross_sections(27, 13)

# ----------------------------------------------------------------------------------------------------
