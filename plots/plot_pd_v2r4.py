import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
import os

from utils import savefig, set_axes

def read_v2r4(id, doAlpha=False):
    """ Read the cross-section data and return energy (E) and cross-section (s) arrays. """
    dir_path = '../tables/v2r4/'
    file_name = 'xsect_Gauss2_TALYS-restored.txt'
    file_path = os.path.join(dir_path, file_name)

    try:
        # Select columns based on whether we are using alpha or not
        cols = (0, 1, 7, 8, 9, 10, 11) if doAlpha else (0, 1, 2, 3, 4, 5, 6)
        A, Z, tN, h1N, x1N, w1N, cN = np.loadtxt(file_path, skiprows=2, unpack=True, usecols=cols)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, None

    # Initialize energy array and cross-section array
    epsilon1 = 30.0 # MeV
    E = np.linspace(0, 100, 1000) # MeV
    s = np.zeros_like(E)

    # Vectorize cross-section calculation for efficiency
    mask = (A == id[0]) & (Z == id[1])
    if not np.any(mask):
        print(f"Error: No data found for id {id}.")
        return E, s

    for i in np.where(mask)[0]:
        s[E > epsilon1] = cN[i]  # Constant for energies > epsilon1
        mask_below_epsilon1 = (E > tN[i]) & (E <= epsilon1)
        s[mask_below_epsilon1] = h1N[i] * np.exp(-(E[mask_below_epsilon1] - x1N[i]) ** 2.0 / w1N[i])

    return E, s

def plot_v2r4(element_id=(56, 26), output_file='xsecs_pd_v2r4.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[0, 100], ylim=[0.01, 300], yscale='log')

    # Read and plot data for neutrons
    E, s_N = read_v2r4(element_id, False)
    ax.plot(E, s_N, color='tab:red', ls='--', label='N')

    # Read and plot data for alphas
    E, s_a = read_v2r4(element_id, True)
    ax.plot(E, s_a, color='tab:red', ls=':', label=r'$\alpha$')

    # Plot the sum of both
    ax.plot(E, s_N + s_a, color='tab:red', ls='-')

    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

if __name__ == "__main__":
    plot_v2r4((56, 26), 'xsecs_pd_Fe56_v2r4.pdf')  # Plot for Fe-56 as the default element
