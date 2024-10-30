from matplotlib import pyplot as plt
import numpy as np 
import subprocess

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

mp = 1.e9 # 1 GeV 

xs_modelList = ['v2r4', 'TENDL-2023']
# nucleiList = np.array([[56, 26]])
nucleiList = np.array([[14, 7], [28, 14], [56, 26]])

# ----------------------------------------------------------------------------------------------------
def execute_get_interaction_length(A, Z, Gmm, model):

    output = subprocess.run(
        ['python3', 'get_interaction_length.py', str(A), str(Z), str(Gmm), model],
        capture_output = True,
        text = True
    )
    
    if output.returncode != 0:
        raise RuntimeError(f'Error executing script: {output.stderr.strip()}')
    
    interaction_length = float(output.stdout.strip())
    return interaction_length

# ----------------------------------------------------------------------------------------------------
def get_interaction_length_array(A, Z, model):

    Gmm = np.logspace(10, 12, num = 50) / A
    interaction_length = np.zeros_like(Gmm)

    for i in range(len(interaction_length)):
        interaction_length[i] = execute_get_interaction_length(A, Z, Gmm[i], model)

    return Gmm * A * mp, interaction_length

# ----------------------------------------------------------------------------------------------------
def plot_interaction_length():

    plt.figure()

    for xs_model in xs_modelList:
        for nuclei in nucleiList:
            A, Z = nuclei
            E, interaction_length = get_interaction_length_array(A, Z, xs_model)
            plt.plot(np.log10(E), interaction_length)

    # plt.xscale('log')    
    plt.yscale('log')
    plt.ylim(top = 1.e4)
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    # plt.xlabel(r'Nucleus Lorentz factor, $\Gamma$')
    plt.ylabel(r'Interaction length$\: \rm [Mpc]$')
    plt.legend()
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_interaction_length()

# ----------------------------------------------------------------------------------------------------
