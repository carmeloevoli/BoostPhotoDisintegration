import numpy as np 
import subprocess

mp = 1.e9 # 1 GeV 

nuclei = np.array([[14, 7], [16, 8], [28, 14], [56, 26], [195, 78]])
xs_models = ['v2r4', 'TENDL-2023']

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

    Gmm = np.logspace(10, 13, num = 50) / A
    interaction_length = np.zeros_like(Gmm)

    for i in range(len(interaction_length)):
        interaction_length[i] = execute_get_interaction_length(A, Z, Gmm[i], model)

    return Gmm * A * mp, interaction_length

# ----------------------------------------------------------------------------------------------------
def write_interaction_length_file(A, Z, model):

    E, interaction_length = get_interaction_length_array(A, Z, model)

    f = open('../runs/files/lambda/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, model), 'w')
    for iE in range(len(E)):
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        f.write(str('{:.15e}'.format(interaction_length[iE])) + '\n')
    f.close()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for nucleus in nuclei:
        A, Z = nucleus
        write_interaction_length_file(A, Z, xs_models[1])

# ----------------------------------------------------------------------------------------------------
