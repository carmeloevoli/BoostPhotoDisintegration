import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np
import os

from utils import savefig, set_axes, read_talys

def plot_talys(element_id=(56, 26), output_file='xsecs_pd_TALYS.pdf'):
    """ Plot the cross-sections for a given element (Z, A). """
    fig, ax = plt.subplots(figsize=(11.5, 8.5))

    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 100], ylim=[0.1, 50], yscale='log')
   
    E, sigma = read_talys('talys_g_O16_nonelastic.txt')
    ax.plot(E, sigma, color='tab:blue', label='O16')

    # Add legend
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

if __name__ == "__main__":
    plot_talys((16, 8), 'xsecs_pd_O16_TALYS.pdf')  # Plot for Fe-56 as the default element
