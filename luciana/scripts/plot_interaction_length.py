from matplotlib import pyplot as plt
import numpy as np 
import subprocess

nucleiList = np.array([[56, 26]])
# nucleiList = np.array([[14, 7], [28, 14], [56, 26]])

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

mp = 1.e9 # 1 GeV 

# ----------------------------------------------------------------------------------------------------
def execute_get_interaction_length(A, Z, Gmm):

    output = subprocess.run(
        ['python3', 'get_interaction_length.py', str(A), str(Z), str(Gmm)],
        capture_output = True,
        text = True
    )
    
    if output.returncode != 0:
        raise RuntimeError(f'Error executing script: {output.stderr.strip()}')
    
    interaction_length = float(output.stdout.strip())
    return interaction_length

# ----------------------------------------------------------------------------------------------------
def get_interaction_length_array(A, Z):

    Gmm = np.logspace(5, 15, num = 50) / A
    interaction_length = np.zeros_like(Gmm)

    for i in range(len(interaction_length)):
        interaction_length[i] = execute_get_interaction_length(A, Z, Gmm[i])

    return Gmm * A * mp, interaction_length

# ----------------------------------------------------------------------------------------------------
def plot_interaction_length():

    plt.figure()

    for nuclei in nucleiList:
        A, Z = nuclei
        E, interaction_length = get_interaction_length_array(A, Z)
        plt.plot(np.log10(E), interaction_length, label = f'A = {A}, Z = {Z}')
    
    plt.yscale('log')
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    plt.ylabel(r'Interaction length$\: \rm [Mpc]$')
    plt.legend()
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_interaction_length()

# ----------------------------------------------------------------------------------------------------
