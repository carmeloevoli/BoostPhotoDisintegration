import wget
from subprocess import Popen, PIPE

def url_exists(url):
    command = ["wget", "-S", "--spider", url]
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stderr = str(stderr)
    exists = stderr.find("Remote file does not exist")
    if int(exists) > -1:
        return False
    else:
        return True

def stringIt(Z):
    if Z == 1:
        return 'H'
    elif Z == 2:
        return 'He'
    elif Z == 3:
        return 'Li'
    elif Z == 4:
        return 'Be'
    elif Z == 5:
        return 'B'
    elif Z == 6:
        return 'C'
    elif Z == 7:
        return 'N'
    elif Z == 8:
        return 'O'
    elif Z == 9:
        return 'F'
    elif Z == 10:
        return 'Ne'
    elif Z == 11:
        return 'Na'
    elif Z == 12:
        return 'Mg'
    elif Z == 13:
        return 'Al'
    elif Z == 14:
        return 'Si'
    elif Z == 15:
        return 'P'
    elif Z == 16:
        return 'S'
    elif Z == 17:
        return 'Cl'
    elif Z == 18:
        return 'Ar'
    elif Z == 19:
        return 'K'
    elif Z == 20:
        return 'Ca'
    elif Z == 21:
        return 'Sc'
    elif Z == 22:
        return 'Ti'
    elif Z == 23:
        return 'V'
    elif Z == 24:
        return 'Cr'
    elif Z == 25:
        return 'Mn'
    elif Z == 26:
        return 'Fe'
    elif Z == 27:
        return 'Co'
    elif Z == 28:
        return 'Ni'
    elif Z == 29:
        return 'Cu'
    elif Z == 30:
        return 'Zn'
    else:
        return 'none'

TREPO='https://tendl.web.psi.ch/tendl_2023/gamma_file'
OUTDIR='TENDL2023'

def get_non_table(Z, A):
    element = stringIt(Z)
    url = TREPO + '/' + element + '/' + element + str(A).zfill(3) + '/tables/xs/nonelastic.tot'
    myfname = OUTDIR + '/talys_g_' + element + str(A) + '_non.txt'
    if (url_exists(url)):
        filename = wget.download(url, out=myfname)
        
def get_tables(Z, A):
    get_non_table(Z, A)

if __name__== "__main__":
    get_tables(26, 56) # get Fe
