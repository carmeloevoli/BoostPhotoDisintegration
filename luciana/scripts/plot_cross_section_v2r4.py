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

nucleiList = np.array([[14, 7], [28, 14], [56, 26]])

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
def plot_cross_section_v2r4(A, Z):

    eps_N, cross_section_N = execute_get_cross_section_v2r4(A, Z, 'N')
    cross_section_alpha = execute_get_cross_section_v2r4(A, Z, 'alpha')[1]

    mask_common = (cross_section_N > 0) & (cross_section_alpha > 0)
    
    eps_common = eps_N[mask_common]
    cross_section_N = cross_section_N[mask_common]
    cross_section_alpha = cross_section_alpha[mask_common]
    
    cross_section_total = cross_section_N + cross_section_alpha

    color = select_color(A, Z)

    plt.figure()
    plt.plot(eps_common, cross_section_total, color = color, ls = '-', label = r'$N + \alpha$')
    plt.plot(eps_common, cross_section_N, color = color, ls = '--', label = r'$N$')
    plt.plot(eps_common, cross_section_alpha, color = color, ls = ':', label = r'$\alpha$')
    
    at = AnchoredText('{0}'.format(select_anchored_text(A, Z)), loc = 'upper right', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)	
    
    plt.yscale('log')
    plt.xlabel(r"Photon energy$'\: \rm [MeV]$")
    plt.ylabel(r'Nonelastic cross section$\: \rm [mb]$')
    plt.legend(title = 'Channel')
    plt.savefig('../figures/cross-sections/cross_section_v2r4_A{0:03}Z{1:03}.pdf'.format(int(A), int(Z)), bbox_inches = 'tight')
    plt.savefig('../figures/cross-sections/cross_section_v2r4_A{0:03}Z{1:03}.png'.format(int(A), int(Z)), bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_all_cross_sections_v2r4():

    params = np.loadtxt('../../tables/v2r4/xsect_Gauss2_TALYS-restored.txt', skiprows=2)
    params = params[:-3]

    plt.figure()

    unique_A_values = np.unique(params[:, 0])
    colormap = cm.get_cmap('viridis', len(unique_A_values))

    for irow in range(len(params)):
    
        A = int(params[irow, 0])
        Z = int(params[irow, 1])
        
        eps, cross_section_N = execute_get_cross_section_v2r4(A, Z, 'N')
        cross_section_alpha = execute_get_cross_section_v2r4(A, Z, 'alpha')[1]
        cross_section = cross_section_N + cross_section_alpha
        mask = cross_section > 0
        eps = eps[mask]
        cross_section = cross_section[mask]  

        color = colormap(np.where(unique_A_values == A)[0][0] / len(unique_A_values))
        plt.plot(eps, cross_section, color = color)
    
    plt.ylim(bottom = 1.e-1)
    plt.yscale('log')
    plt.xlabel(r"Photon energy$'\: \rm [MeV]$")
    plt.ylabel(r'Nonelastic cross section$\: \rm [mb]$')

    sm = plt.cm.ScalarMappable(cmap = colormap, norm = plt.Normalize(vmin = unique_A_values.min(), vmax = unique_A_values.max()))
    plt.colorbar(sm, ax = plt.gca(), label = r'Mass number, $A$')

    plt.savefig('../figures/cross-sections/all_cross_sections_v2r4.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/cross-sections/all_cross_sections_v2r4.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    inucleus = 2
    plot_cross_section_v2r4(nucleiList[inucleus][0], nucleiList[inucleus][1])

    # plot_all_cross_sections_v2r4()

# ----------------------------------------------------------------------------------------------------
