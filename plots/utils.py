import numpy as np
import matplotlib.pyplot as plt
import os

def savefig(fig: plt.Figure, filename: str, dpi: int = 300, bbox_inches: str = 'tight', pad_inches: float = 0.1, transparent: bool = False) -> None:
    """
    Save the given matplotlib figure to a file with enhanced options for better quality.
    
    Parameters:
    - fig: The matplotlib Figure object to save.
    - filename: The file name or path where the figure will be saved.
    - dpi: The resolution in dots per inch (default is 300 for high-quality).
    - bbox_inches: Adjusts bounding box ('tight' will minimize excess whitespace).
    - pad_inches: Amount of padding around the figure when bbox_inches is 'tight' (default is 0.1).
    - transparent: Whether to save the plot with a transparent background (default is False).
    """
    
    try:
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches, transparent=transparent, format='pdf')
        print(f'Plot successfully saved to {filename} with dpi={dpi}, bbox_inches={bbox_inches}, pad_inches={pad_inches}, transparent={transparent}')
    except Exception as e:
        print(f"Error saving plot to {filename}: {e}")

def set_axes(ax: plt.Axes, xlabel: str, ylabel: str, xscale: str = 'linear', yscale: str = 'linear', xlim: tuple = None, ylim: tuple = None) -> None:
    """
    Set the properties for the axes of a plot.
    
    Parameters:
    - ax: Matplotlib Axes object.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - xscale: Scale of the x-axis ('linear' or 'log').
    - yscale: Scale of the y-axis ('linear' or 'log').
    - xlim: Limits for the x-axis (min, max).
    - ylim: Limits for the y-axis (min, max).
    """
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # Validate and set axis scale
    if xscale in ['linear', 'log']:
        ax.set_xscale(xscale)
    else:
        print(f"Invalid xscale '{xscale}', defaulting to 'linear'.")
        ax.set_xscale('linear')
        
    if yscale in ['linear', 'log']:
        ax.set_yscale(yscale)
    else:
        print(f"Invalid yscale '{yscale}', defaulting to 'linear'.")
        ax.set_yscale('linear')

    # Set axis limits if provided
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

def _normalize_data(x: np.ndarray, y: np.ndarray, y_err: np.ndarray, norm: float) -> tuple:
    """Normalize data values by given slope and normalization factor."""
    x_norm = x / norm
    y_norm = norm * y
    y_err_norm = np.zeros_like(y_norm)
    for i in range(len(x)):
        if y_err[i] > 0.:
            y_err_norm[i] = norm * y_err[i]
        else:
            y_err_norm[i] = 0.
    return x_norm, y_norm, y_err_norm

def plot_data(ax: plt.Axes, filename: str, color: str, label: str, norm: float = 1, fmt: str = 'o', zorder: int = 1) -> None:
    """
    Load data from file, normalize, and plot with error bars.
    
    Parameters:
    - ax: Matplotlib Axes object to plot on.
    - filename: The path to the data file.
    - norm: Normalization factor for the data.
    - fmt: Format string for the plot markers.
    - color: Color of the plot markers and lines.
    - label: Label for the plot legend.
    - zorder: Z-order for layering the plot.
    """
    try:
        x, y, y_err = np.loadtxt(f'../tables/EXFOR/{filename}', usecols=(0, 1, 2), unpack=True)
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return
        
    # Normalize data
    x_norm, y_norm, y_err_norm = _normalize_data(x, y, y_err, norm)
    
    # Plot the data with error bars
    ax.errorbar(x_norm, y_norm, yerr=[y_err_norm, y_err_norm], fmt=fmt, markeredgecolor=color, color=color, 
                label=label, capsize=3.3, markersize=4.5, elinewidth=1.4, capthick=1.4, zorder=zorder)

def read_talys(filename):
    repo = '../tables/TENDL2023/'
    E, sigma = np.loadtxt(repo + filename, usecols=(0,1), unpack=True)
    return E, sigma # MeV, mbarn

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

    return E, s # MeV, barn