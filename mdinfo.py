
__version__ = "0.0.1"
__author__ = "Backest"
__email__ = "alvarodrumer54@gmail.com"

def _updateVersion(nver: str):
    global __version__
    if nver < __version__:
        print(f"Version must be greater than {__version__}!! (last version updated)")
        return 
    else:
        __version__ = nver
        print(f"Successfully updated to version: {__version__}")
        return 
