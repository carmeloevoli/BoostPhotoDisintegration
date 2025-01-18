import numpy as np 

mp = 1.e9 # 1 GeV 

# nuclei = np.array([[14, 7], [16, 8], [28, 14], [56, 26], [195, 78]])
nuclei = np.array([[16, 8], [28, 14], [56, 26]])

# ----------------------------------------------------------------------------------------------------
def write_interaction_length_difference_file(A, Z):

    data_v2r4 = np.loadtxt('../results/interaction-length/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, 'v2r4'))
    data_TENDL2023 = np.loadtxt('../results/interaction-length/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, 'TENDL-2023'))

    E = data_v2r4[:,0]
    lambda_v2r4 = data_v2r4[:,1]
    lambda_TENDL2023 = data_TENDL2023[:,1]

    f = open('../results/interaction-length/interactionLengthDifferences_A{0:03}Z{1:03}.dat'.format(A, Z), 'w')
    for iE in range(len(E)):
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        f.write(str('{:.15e}'.format(abs(lambda_v2r4[iE] - lambda_TENDL2023[iE]))) + '\n')
    f.close()

# ----------------------------------------------------------------------------------------------------
def write_interaction_length_difference_percentage_file(A, Z):

    data_v2r4 = np.loadtxt('../results/interaction-length/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, 'v2r4'))
    data_TENDL2023 = np.loadtxt('../results/interaction-length/interactionLength_A{0:03}Z{1:03}_{2}.dat'.format(A, Z, 'TENDL-2023'))

    E = data_v2r4[:,0]
    lambda_v2r4 = data_v2r4[:,1]
    lambda_TENDL2023 = data_TENDL2023[:,1]

    f = open('../results/interaction-length/interactionLengthDifferencePercentages_A{0:03}Z{1:03}.dat'.format(A, Z), 'w')
    
    for iE in range(len(E)):
        
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        
        relative_difference = abs(lambda_v2r4[iE] - lambda_TENDL2023[iE]) / lambda_TENDL2023[iE]
    
        if relative_difference == float('inf'):
            f.write('NaN' + '\n') 
        else:
            f.write(str('{:.15e}'.format(relative_difference * 1.e2)) + '\n')

    f.close()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for nucleus in nuclei:
        A = nucleus[0]
        Z = nucleus[1]
        write_interaction_length_difference_percentage_file(A, Z)
        # write_interaction_length_difference_file(A, Z)

# ----------------------------------------------------------------------------------------------------


