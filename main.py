import db as D
import os

from colorama import Fore
from platform import python_version
from db import cFormatter
from checker import Checker


...



if __name__ == "__main__":
    pyver = python_version()
    sysname = os.name

    if sysname.upper() != "NT":
        print(cFormatter("Este programa esta probado en dispositivos Windows. Puede experimentar problemas si ejecuta el programa en otro sistema operativo", color= Fore.YELLOW))
        exit()
    if pyver < "3.10":
        print(cFormatter(f"Esta aplicacion requiere Python 3.10.2 o superior. {cFormatter(f'Version actual: {pyver}', color= Fore.MAGENTA)}", color=Fore.RED))
        exit()