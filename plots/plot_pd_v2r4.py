import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np

# def read_pd_data(filename, projectile):
#     E_ = np.logspace(0, 2, 1000)
#     s_ = np.zeros(1000)
#     for line in open(filename):
#         line = line.rstrip()
#         if line[0] != '#':
#             fields = line.split(',')
#             A = str(fields[0]).strip()
#             Z = str(fields[1]).strip()
#             if (projectile[0] == int(A) and projectile[1] == int(Z)):
#                 sstr = fields[2:1002]
#                 for i in range(1000):
#                     s_[i] = float(sstr[i])
#     return E_, s_

def read_v2r4(id, doAlpha = False):
    dir = '../tables/v2r4/'
    url = dir + 'xsect_Gauss2_TALYS-restored.txt'
    
    cols = (0,1,7,8,9,10,11) if doAlpha else (0,1,2,3,4,5,6)
    A, Z, tN, h1N, x1N, w1N, cN = np.loadtxt(url, skiprows=2, unpack=True, usecols=cols)
        
    size = len(A)
    epsilon1 = 30.
    E = np.logspace(0, 2, 100)
    s = np.zeros(100)
    for i in range(size):
        if A[i] == id[0] and Z[i] == id[1]:
            print (id)
            for j in range(100):
                if E[j] > epsilon1:
                    s[j] = cN[i]
                elif E[j] > tN[i]:
                    s[j] = h1N[i] * np.exp(-(E[j] - x1N[i])**2.0 / w1N[i])
    return E, s

def plot_v2r4():
    def set_axes(ax):
        ax.set_ylabel(r'$\sigma$ [mb]')
        ax.set_ylim([0.001,300])
        ax.set_yscale('log')
        ax.set_xlabel(r'$\epsilon^\prime$ [MeV]')
        ax.set_xlim([0,200])
        #ax.set_xscale('log')
        ax.set_ylim([0.1,300.])
        ax.set_xlim([0.,100.])
        ax.set_ylabel('$\sigma$($\gamma$,X)')

    fig = plt.figure(figsize=(10.5, 8))
    ax = fig.add_subplot(111)
    set_axes(ax)

    E, s_N = read_v2r4([56,26], False)
    ax.plot(E, s_N, color='tab:red', ls='--')

    E, s_a = read_v2r4([56,26], True)
    ax.plot(E, s_a, color='tab:red', ls=':')

    ax.plot(E, s_N + s_a, color='tab:red', ls='-')

    ax.legend()
    
    plt.savefig('xsecs_pd_Fe56_v2r4.pdf')

if __name__== "__main__":
    plot_v2r4()
