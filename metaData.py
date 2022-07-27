from platform import python_version, system

__all__ = [
    'updateVersion',
    'pyver'
    'opsys'
]

__version__ = "0.0.1"
__author__ = "Backest"
__email__ = "alvarodrumer54@gmail.com"

pyver = python_version()
opsys = system()  #* Can be None if opsys not Found  

def updateVersion(nver: str):
    global __version__
    if nver < __version__:
        print(f"Version must be greater than {__version__}!! (last version updated)")
        return 
    else:
        __version__ = nver
        print(f"Successfully updated to version: {__version__}")
        return 
