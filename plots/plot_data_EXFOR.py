import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np

from utils import savefig, set_axes, plot_data, read_talys, read_v2r4

def plot_exfor_Fe54(output_file='xsecs_exfor_Fe54.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 50], ylim=[0, 180], yscale='linear')

    plot_data(ax=ax, filename='g_Fe54_abs_M0507.004.txt', color='r', label='Norbury+1978')

    E, sigma = read_talys('talys_g_Fe54_nonelastic.txt')
    ax.plot(E, sigma, color='b', zorder=9, label='TALYS2023', lw=3.5)

    E, sigma_n = read_v2r4((54, 26), False)
    E, sigma_a = read_v2r4((54, 26), True)
    ax.plot(E, sigma_n + sigma_a, color='g', zorder=9, label='v2r4', linestyle='--', lw=3.5)

    ax.text(8, 150, 'Fe54', fontsize=30)

    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_exfor_Al27(output_file='xsecs_exfor_Al27.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 50], ylim=[0, 50], yscale='linear')

    #plot_data(ax=ax, filename='g_Al27_abs_L0083.006', color='tab:gray', label='x', zorder=1)
    plot_data(ax=ax, filename='g_Al27_abs_L0083.006.txt', color='tab:orange', label='Ahrens+1972', zorder=2)
    plot_data(ax=ax, filename='g_Al27_abs_L0122.007.txt', color='tab:purple', label='Wyckoff+1965', zorder=3)
    plot_data(ax=ax, filename='g_Al27_abs_M0188.016.txt', color='tab:pink', label='Ahrens1985', zorder=4)
    plot_data(ax=ax, filename='g_Al27_abs_M0825.011.txt', color='tab:olive', label='Ahrens+1975', zorder=5)

    E, sigma = read_talys('talys_g_Al27_nonelastic.txt')
    ax.plot(E, sigma, color='b', zorder=9, label='TALYS2023', lw=3.5)

    E, sigma_n = read_v2r4((27, 13), False)
    E, sigma_a = read_v2r4((27, 13), True)
    ax.plot(E, sigma_n + sigma_a, color='g', zorder=9, label='v2r4', linestyle='--', lw=3.5)

    ax.text(8, 44, 'Al27', fontsize=30)

    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_exfor_Mg24(output_file='xsecs_exfor_Mg24.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 50], ylim=[0, 50], yscale='linear')

    plot_data(ax=ax, filename='g_Mg24_abs_M0656.003.txt', color='tab:orange', label='Varlamov+2003', zorder=2)
    plot_data(ax=ax, filename='g_Mg24_abs_M0727.003.txt', color='tab:purple', label='Dolbilkin+1966', zorder=3)
    
    E, sigma = read_talys('talys_g_Mg24_nonelastic.txt')
    ax.plot(E, sigma, color='b', zorder=9, label='TALYS2023', lw=3.5)

    E, sigma_n = read_v2r4((24, 12), False)
    E, sigma_a = read_v2r4((24, 12), True)
    ax.plot(E, sigma_n + sigma_a, color='g', zorder=9, label='v2r4', linestyle='--', lw=3.5)

    ax.text(8, 44, 'Mg24', fontsize=30)

    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_exfor_O16(output_file='xsecs_exfor_O16.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 50], ylim=[0, 50], yscale='linear')

    plot_data(ax=ax, filename='g_O16_abs_L0064.004.txt', color='tab:gray', label='Bezic+1969', zorder=1)
    plot_data(ax=ax, filename='g_O16_abs_L0083.004.txt', color='tab:orange', label='Ahrens+1972', zorder=2)
    plot_data(ax=ax, filename='g_O16_abs_L0122.004.txt', color='tab:purple', label='Wyckoff+1975', zorder=3)

    E, sigma = read_talys('talys_g_O16_nonelastic.txt')
    ax.plot(E, sigma, color='b', zorder=9, label='TALYS2023', lw=3.5)

    E, sigma_n = read_v2r4((16, 8), False)
    E, sigma_a = read_v2r4((16, 8), True)
    ax.plot(E, sigma_n + sigma_a, color='g', zorder=9, label='v2r4', linestyle='--', lw=3.5)

    ax.text(8, 44, 'O16', fontsize=30)
   
    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

if __name__ == "__main__":
    plot_exfor_Fe54()   
    plot_exfor_Al27()   
    plot_exfor_Mg24()   
    plot_exfor_O16()   