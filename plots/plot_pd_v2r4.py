import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
import os

from utils import savefig, set_axes, read_v2r4

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
