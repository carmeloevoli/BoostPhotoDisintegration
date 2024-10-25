import os
import wget
import subprocess
from subprocess import Popen, PIPE

from utils import stringIt, url_exists

TREPO = 'https://tendl.web.psi.ch/tendl_2023/gamma_file'
OUTDIR = 'TENDL2023'

def get_table(Z, A, type='nonelastic'):
    """Download the non-elastic total table for element Z and mass number A if the URL exists."""
    element = stringIt(Z)
    if element == 'none':
        print(f"Invalid atomic number: {Z}")
        return
    
    url = f"{TREPO}/{element}/{element}{str(A).zfill(3)}/tables/xs/{type}.tot"
    myfname = os.path.join(OUTDIR, f'talys_g_{element}{A}_{type}.txt')

    # Create the output directory if it does not exist
    try:
        os.makedirs(OUTDIR, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory '{OUTDIR}': {e}")
        return

    # Check if file exists locally before downloading
    if os.path.exists(myfname):
        print(f"File already exists: {myfname}")
        return

    # Download if URL exists
    try:
        if url_exists(url):
            print(f"Downloading {url}...")
            wget.download(url, out=myfname)
            print(f"\nSaved to {myfname}")
        else:
            print(f"URL not found: {url}")
    except Exception as e:
        print(f"Error occurred during download or file saving: {e}")

def get_tables(pid):
    """Download all necessary tables for element Z and mass number A."""
    try:
        Z, A = pid
        if Z not in ELEMENTS:
            raise ValueError(f"Invalid atomic number: {Z}. Supported range is 1 to 30.")
        if A <= 0:
            raise ValueError(f"Invalid mass number: {A}. Must be a positive integer.")
        get_table(Z, A)
        get_table(Z, A, 'pprod')
        get_table(Z, A, 'nprod')
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        pids = ((6, 12), (8, 16), (12, 24), (13, 27), (26, 54), (26, 56))
        for pid in pids:
            get_tables(pid)
    except Exception as e:
        print(f"Error in the main routine: {e}")
