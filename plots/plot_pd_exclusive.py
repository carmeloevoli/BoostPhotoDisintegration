import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('simprop.mplstyle')
import numpy as np

from utils import savefig, set_axes, file_exists, read_talys, read_v2r4

XREPO = '../tables/TENDL2023/'
OUTDIR = 'TENDL2023'

def count_nucleons(i_n, i_p, i_d, i_t, i_h, i_a):
    """Calculate the total nucleons based on particle counts."""
    return (i_n + i_p) + 2 * i_d + 3 * (i_t + i_h) + 4 * i_a 

def plot_pd_exclusive_xsecs(output_file='xsecs_pd_exclusive.pdf'):
    # Remember: (in, ip, id, it, ih, iα)
    def sum_cross_sections(A):
        filename = f'O016/talys_g_O16_000000.txt'
        E_tot, sigma_g = read_talys(filename)
        sigma_tot = np.zeros_like(E_tot)
        for i_n in range(5):
            for i_p in range(5):
                for i_d in range(5):
                    for i_t in range(5):
                        for i_h in range(5):
                            for i_a in range(5):
                                filename = f'O016/talys_g_O16_{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}.txt'
                                if sum([i_n, i_p, i_d, i_t, i_h, i_a]) == A and file_exists(XREPO + filename):
                                    print(filename)
                                    E, sigma = read_talys(filename)
                                    E_tot = E
                                    sigma_tot += sigma
        return E_tot, sigma_tot
    
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'fractional cross-section',
             xlim=[5, 150], ylim=[0.01, 1.5], yscale='log')

    E, sigma_abs = read_talys('talys_g_O16_nonelastic.txt')

    E, sigma_1 = sum_cross_sections(1)
    ax.plot(E, sigma_1 / sigma_abs, label='1', color='tab:blue')

    E, sigma_2 = sum_cross_sections(2)
    ax.plot(E, sigma_2 / sigma_abs, label='2', color='tab:orange')
  
    E, sigma_3 = sum_cross_sections(3)
    ax.plot(E, sigma_3 / sigma_abs, label='3', color='tab:green')

    E, sigma_4 = sum_cross_sections(4)
    ax.plot(E, sigma_4 / sigma_abs, label='4', color='tab:red')

    E, sigma_5 = sum_cross_sections(5)
    ax.plot(E, sigma_5 / sigma_abs, label='5', color='tab:purple')

    E, sigma_6 = sum_cross_sections(6)
    ax.plot(E, sigma_6 / sigma_abs, label='6', color='tab:brown')

    E, sigma_7 = sum_cross_sections(7)
    ax.plot(E, sigma_7 / sigma_abs, label='7', color='tab:pink')

    # total
    sigma_tot = sigma_1 + sigma_2 + sigma_3 + sigma_4 + sigma_5 + sigma_6 + sigma_7
    ax.plot(E, sigma_tot / sigma_abs, color='tab:gray', linestyle=':', label='tot')

    ax.legend(fontsize=15)

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_pd_prod_xsecs(output_file='xsecs_pd_prod.pdf'):
    # Remember: (in, ip, id, it, ih, iα)
    def sum_cross_sections():
        filename = f'O016/talys_g_O16_000000.txt'
        E_tot, sigma_g = read_talys(filename)
        sigma_tot = np.zeros_like(E_tot)
        for i_n in range(1,5):
            for i_p in range(5):
                for i_d in range(5):
                    for i_t in range(5):
                        for i_h in range(5):
                            for i_a in range(5):
                                filename = f'O016/talys_g_O16_{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}.txt'
                                if file_exists(XREPO + filename):
                                    print(filename)
                                    E, sigma = read_talys(filename)
                                    E_tot = E
                                    sigma_tot += float(i_n) * sigma
        return E_tot, sigma_tot
    
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 100], ylim=[0.1, 10], yscale='log')

    E, sigma_prod_n = read_talys('talys_g_O16_nprod.txt')
    ax.plot(E, sigma_prod_n, label='n prod', color='tab:gray')

    E, sigma_tot = sum_cross_sections()
    ax.plot(E, sigma_tot, label='sum', color='tab:red', ls=':')

    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_pd_pa_xsecs(output_file='xsecs_pd_pa.pdf'):
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$\sigma$($\gamma$,X) [mb]',
             xlim=[5, 100], ylim=[0.03, 50], yscale='log')

    E, sigma_abs = read_talys('talys_g_O16_nonelastic.txt')
    ax.plot(E, sigma_abs, label='abs', lw=2, color='tab:gray')

    E, sigma_n = read_talys('O016/talys_g_O16_100000.txt')
    E, sigma_p = read_talys('O016/talys_g_O16_010000.txt')
    ax.plot(E, sigma_p + sigma_n, label='p + n', color='tab:orange', ls='--')

    E, sigma_h = read_talys('O016/talys_g_O16_000010.txt')
    E, sigma_a = read_talys('O016/talys_g_O16_000001.txt')
    ax.plot(E, sigma_h + sigma_a, label='h + a', color='tab:blue', ls=':')
    
    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_pd_sirente_xsecs(output_file='xsecs_pd_sirente.pdf'):
     # Remember: (in, ip, id, it, ih, iα)
    def sum_cross_sections(idStr):
        filename = f'{idStr}/talys_g_{idStr}_000000.txt'
        E_tot, sigma_g = read_talys(filename)
        sigma_N = np.zeros_like(E_tot)
        sigma_a = np.zeros_like(E_tot)
        for i_n in range(5):
            for i_p in range(5):
                for i_d in range(5):
                    for i_t in range(5):
                        for i_h in range(5):
                            for i_a in range(5):
                                filename = f'{idStr}/talys_g_{idStr}_{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}.txt'
                                if file_exists(XREPO + filename):
                                    print(filename)
                                    E, sigma = read_talys(filename)
                                    E_tot = E
                                    sigma_N += (float(i_n) + float(i_p) + 2. * float(i_d) + 3. * float(i_t)) * sigma
                                    sigma_a += (float(i_h) + float(i_a)) * sigma
        return E_tot, sigma_N, sigma_a
    
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'$P_{1\alpha}/P_{1N}$',
             xlim=[10, 90], ylim=[0.003, 3], yscale='log', xscale='log')

    E, sigma_N, sigma_a = sum_cross_sections('O16')
    ax.plot(E, sigma_a / sigma_N, label='TALYS-2023', color='tab:orange', ls='--')

    E, sigma_N, sigma_a = sum_cross_sections('Si28')
    ax.plot(E, sigma_a / sigma_N, color='tab:red', ls='--')

    E, sigma_N, sigma_a = sum_cross_sections('Fe56')
    ax.plot(E, sigma_a / sigma_N, color='tab:purple', ls='--')

    E, sigma_N = read_v2r4((16, 8), False)
    E, sigma_a = read_v2r4((16, 8), True)
    ax.plot(E, sigma_a / sigma_N, label='v2r4', color='tab:orange', ls=':')

    E, sigma_N = read_v2r4((28, 14), False)
    E, sigma_a = read_v2r4((28, 14), True)
    ax.plot(E, sigma_a / sigma_N, color='tab:red', ls=':')

    E, sigma_N = read_v2r4((56, 26), False)
    E, sigma_a = read_v2r4((56, 26), True)
    ax.plot(E, sigma_a / sigma_N, color='tab:purple', ls=':')

    ax.text(70, 0.16, 'O16', color='tab:orange')
    ax.text(70, 0.08, 'Si28', color='tab:red')
    ax.text(70, 0.03, 'Fe56', color='tab:purple')

    ax.legend(fontsize=26)

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

def plot_pd_lnA_xsecs(output_file='xsecs_pd_lnA.pdf'):
    # Remember: (in, ip, id, it, ih, iα)
    def approx_lnA_cross_sections():
        filename = f'O16/talys_g_O16_000000.txt'
        E_tot, sigma_g = read_talys(filename)
        sigma_N = np.zeros_like(E_tot)
        sigma_a = np.zeros_like(E_tot)
        for i_n in range(5):
            for i_p in range(5):
                for i_d in range(5):
                    for i_t in range(5):
                        for i_h in range(5):
                            for i_a in range(5):
                                filename = f'O16/talys_g_O16_{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}.txt'
                                if file_exists(XREPO + filename):
                                    print(filename)
                                    E, sigma = read_talys(filename)
                                    E_tot = E
                                    sigma_N += (float(i_n) + float(i_p) + 2. * float(i_d) + 3. * float(i_t)) * sigma
                                    sigma_a += (float(i_h) + float(i_a)) * sigma
        return E_tot, sigma_N, sigma_a
    
        # Remember: (in, ip, id, it, ih, iα)
    def true_lnA_cross_sections():
        filename = f'O16/talys_g_O16_000000.txt'
        E_tot, sigma_g = read_talys(filename)
        lnA_sigma = np.zeros_like(E_tot)
        sigma_sum = np.zeros_like(E_tot)
        for i_n in range(5):
            for i_p in range(5):
                for i_d in range(5):
                    for i_t in range(5):
                        for i_h in range(5):
                            for i_a in range(5):
                                filename = f'O16/talys_g_O16_{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}.txt'
                                if file_exists(XREPO + filename):
                                    print(filename)
                                    E, sigma = read_talys(filename)
                                    E_tot = E
                                    residual_A = 16. - (float(i_n) + float(i_p) + 2. * float(i_d) + 3. * float(i_t) + 3. * float(i_h) + 4. * float(i_a))
                                    assert(residual_A > 0)
                                    lnA_sigma += np.log(residual_A) * sigma
                                    sigma_sum += sigma
        return E_tot, lnA_sigma, sigma_sum
    
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel=r'$\epsilon^\prime$ [MeV]', ylabel=r'ln A',
             xlim=[10, 120], ylim=[2, 3], xscale='log', yscale='linear')

    ax.text(42., 2.90, 'O16', fontsize=27)

    E, wlnA, sigma_tot = true_lnA_cross_sections() 
    ax.plot(E, wlnA / sigma_tot, label='all channels')

    E, sigma_N, sigma_a = approx_lnA_cross_sections()
    wlnA = np.log(16. - 1.) * sigma_N + np.log(16. - 4.) * sigma_a
    sigma_sum = sigma_N + sigma_a
    ax.plot(E, wlnA / sigma_sum, label='1-particle approx.', ls='--')

    ax.hlines(np.log(16), 0, 300, ls=':', color='tab:gray')
    ax.text(88., np.log(16) + 0.02, 'A = 16', fontsize=18, color='tab:gray')
    ax.hlines(np.log(12), 0, 300, ls=':', color='tab:gray')
    ax.text(88., np.log(12) + 0.02, 'A = 12', fontsize=18, color='tab:gray')
    ax.hlines(np.log(8), 0, 300, ls=':', color='tab:gray')
    ax.text(88., np.log(8) + 0.02, 'A = 8', fontsize=18, color='tab:gray')

    GammaNucleon = 1e19 / 1e9
    epsCmb = 1e-3 * 1e-6 # MeV

    epsilonPrime = 2. * GammaNucleon * epsCmb
    ax.vlines(epsilonPrime, 1, 4, color='tab:red', lw=2, ls='--')
    ax.text(21., 2.20, r'$\Gamma \gtrsim 10^{10}$ on CMB', fontsize=18, color='tab:red')
    ax.text(21., 2.28, r'$\Gamma \gtrsim 10^{9}$ on IR', fontsize=18, color='tab:red')

    ax.legend()

    # Save figure using a utility function (ensure error handling in savefig)
    try:
        savefig(fig, output_file)
        print(f"Figure saved as {output_file}")
    except Exception as e:
        print(f"Error saving figure {output_file}: {e}")

if __name__ == "__main__":
    # plot_pd_exclusive_xsecs('xsecs_pd_exclusive_O16_TALYS.pdf') 
    # plot_pd_prod_xsecs('xsecs_pd_prod_O16_TALYS.pdf')
    # plot_pd_pa_xsecs('xsecs_pd_pa_O16_TALYS.pdf')
    # plot_pd_sirente_xsecs('xsecs_pd_sirente_O16_TALYS.pdf')
    plot_pd_lnA_xsecs('xsecs_pd_lnA_O16.pdf')