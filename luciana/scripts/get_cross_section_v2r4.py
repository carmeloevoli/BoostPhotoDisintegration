import numpy as np 
import sys

eps_1 = 30    # MeV
eps_max = 150 # MeV

# ----------------------------------------------------------------------------------------------------
def cross_section_Model4(A, Z, ipart):

    params = np.loadtxt('../../tables/v2r4/xsect_Gauss2_TALYS-restored.txt', skiprows = 2)

    for irow in range(len(params)):
        if params[irow, 0] == A and params[irow, 1] == Z:
            break
    else:
        raise ValueError(f'No data found for A = {A} and Z = {Z}')

    if ipart == 'N':
        t, h1, x1, w1, c = params[irow, 2], params[irow, 3], params[irow, 4], params[irow, 5], params[irow, 6]
    elif ipart == 'alpha':
        t, h1, x1, w1, c = params[irow, 7], params[irow, 8], params[irow, 9], params[irow, 10], params[irow, 11]
    else:
        raise ValueError(f'Invalid particle type: {ipart}')
    
    eps = np.logspace(0, np.log10(eps_max), num = 100)
    cross_section = np.zeros_like(eps)

    mask1 = (eps > t) & (eps < eps_1)
    mask2 = (eps > eps_1) & (eps < eps_max)

    cross_section[mask1] = h1 * np.exp(-(eps[mask1] - x1) ** 2 / w1)
    cross_section[mask2] = c

    return eps, cross_section

# ----------------------------------------------------------------------------------------------------
def print_cross_section_Model4():

    A = int(sys.argv[1])
    Z = int(sys.argv[2])
    ipart = sys.argv[3]

    eps, cross_section = cross_section_Model4(A, Z, ipart)

    print(eps.tolist())  
    print(cross_section.tolist())

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    print_cross_section_Model4()

# ----------------------------------------------------------------------------------------------------