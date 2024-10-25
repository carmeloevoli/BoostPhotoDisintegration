import subprocess
from subprocess import Popen, PIPE

# Mapping Z to element symbol
ELEMENTS = {
    1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
    11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca',
    21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn'
}

def url_exists(url):
    """Check if a URL exists using wget's spider command, with error handling."""
    try:
        command = ["wget", "-S", "--spider", url]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        _, stderr = process.communicate()
        return "Remote file does not exist" not in stderr.decode()
    except FileNotFoundError:
        print("Error: 'wget' command not found. Please ensure wget is installed and available in the PATH.")
        return False
    except subprocess.SubprocessError as e:
        print(f"Subprocess error occurred while checking URL: {e}")
        return False

def stringIt(Z):
    """Map atomic number to element symbol. Return 'none' if Z is not found."""
    return ELEMENTS.get(Z, 'none')