import os
import wget

from utils import ELEMENTS, stringIt, url_exists

TREPO = 'https://tendl.web.psi.ch/tendl_2023/gamma_file'
OUTDIR = 'TENDL2023'

def count_nucleons(i_n, i_p, i_d, i_t, i_h, i_a):
    """Calculate the total nucleons based on particle counts."""
    return (i_n + i_p) + 2 * i_d + 3 * (i_t + i_h) + 4 * i_a 

def nucleon_combinations(A):
    """Generate valid nucleon combinations up to a maximum nucleon count A."""
    for i_n in range(5):
        for i_p in range(5):
            for i_d in range(5):
                for i_t in range(5):
                    for i_h in range(5):
                        for i_a in range(5):
                            if count_nucleons(i_n, i_p, i_d, i_t, i_h, i_a) <= A:
                                yield i_n, i_p, i_d, i_t, i_h, i_a

def download_file(url, filepath):
    """Download file if it exists at the URL, otherwise log error."""
    if os.path.exists(filepath):
        print(f"File already exists: {filepath}")
        return False
    try:
        if url_exists(url):
            print(f"Downloading {url}...")
            wget.download(url, out=filepath)
            print(f"\nSaved to {filepath}")
            return True
        else:
            print(f"URL not found: {url}")
            return False
    except Exception as e:
        print(f"Error downloading file from {url}: {e}")
        return False

def get_tables(Z, A):
    """Download all tables for a given nucleus defined by atomic number Z and mass number A."""
    element = stringIt(Z)
    if element == 'none':
        print(f"Invalid atomic number: {Z}")
        return

    # Define output directory for this element and ensure it exists
    outdir = os.path.join(OUTDIR, f"{element}{str(A).zfill(3)}")
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory '{outdir}': {e}")
        return

    # Track successful downloads
    download_count = 0

    for i_n, i_p, i_d, i_t, i_h, i_a in nucleon_combinations(A):
        nucleon_type = f"{i_n}{i_p}{i_d}{i_t}{i_h}{i_a}"
        url = f"{TREPO}/{element}/{element}{str(A).zfill(3)}/tables/xs/xs{nucleon_type}.tot"
        myfname = os.path.join(outdir, f"talys_g_{element}{A}_{nucleon_type}.txt")

        if download_file(url, myfname):
            download_count += 1

    print(f"Total files downloaded for {element}-{A}: {download_count}")

def get_nucleus(pid):
    """Validate input and trigger the download process for the specified nucleus."""
    try:
        Z, A = pid
        if Z not in ELEMENTS:
            raise ValueError(f"Invalid atomic number: {Z}. Supported range is 1 to 30.")
        if A <= 0:
            raise ValueError(f"Invalid mass number: {A}. Must be a positive integer.")
        get_tables(Z, A)
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        pid = (8, 16)  # Example for Oxygen-16
        get_nucleus(pid)
    except Exception as e:
        print(f"Error in the main routine: {e}")
