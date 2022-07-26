"""Some utility functions that make source code more cleaner and easier to read."""

import logging
import os.path
import time as t
import mmap

from chardet import detect
from pathlib import Path
from colorama import Fore, Back, Style
from random import choice
from werkzeug.security import check_password_hash


def Logger(level, text: str, logger_preffix: str = None) -> str:
    """Funcion para formatear mensajes de terminal rapidamente.\n
    'i' -> info\n
    'w' -> warn\n
    'c' -> critical\n
    'e' -> error\n
    """
    log = logging.getLogger("Checker") if not logger_preffix else logging.getLogger(logger_preffix)

    if level == "i":
        return log.info(text)
    elif level == "w":
        return log.warning(text)
    elif level == "c":
        return log.critical(text)
    elif level == "e":
        return log.error(text)
    else:
        return "Ha ocurrido un error. Establezca ['i', 'w', 'c' o 'e'] como valores para el parametro ['level']"


def cFormatter(
    string: str, 
    color: Fore, 
    style: Style = None, 
    background: Back = None, 
    random: bool = False, 
    iter_colors: list[Fore] = []
) -> str:
    """
    Formateador de texto en terminal.
    Valido con cadenas de texto, listas de texto y docstrings.
    """
    
    #init(autoreset= autoreset)
    c = [Fore.BLACK, Fore.RED, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.WHITE, 
         Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTWHITE_EX]
    #? c = [f"Fore.{c}" for c in vars(Fore).keys()]
    #? vars()
    s = [Style.DIM, Style.NORMAL, Style.BRIGHT]
    b = [Back.BLACK, Back.RED, Back.BLUE, Back.CYAN, Back.GREEN, Back.MAGENTA, Back.YELLOW, Back.WHITE, Back.LIGHTBLACK_EX, Back.LIGHTBLUE_EX, 
    Back.LIGHTCYAN_EX, Back.LIGHTGREEN_EX, Back.LIGHTMAGENTA_EX, Back.LIGHTYELLOW_EX, Back.LIGHTWHITE_EX]

    if (color is not None and not color in c) or (style is not None and not style in s) or (background is not None and not background in b):
        return ValueError(cFormatter(f"Color o estilo o fondo no valido", color= Fore.RED))

    else:

        if iter_colors:
            if len(iter_colors) == 0 or [x for x in iter_colors if x not in c]:
                return TypeError(cFormatter("No se ha definido una lista de colores con los que iterar o algun color no es valido", color= Fore.RED))
            else: 
                letters = []
                for chars in string:
                    letters.append(f"{choice(iter_colors)}{chars}{Fore.RESET}")
                return "".join(letters)

        elif random:
            rcolor = choice(c)
            rstyle = choice(s)
            rback = choice(b)
            return f"{rcolor}{rstyle}{rback}{string}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"

        elif color:
            if background:
                return f"{color}{background}{string}{Fore.RESET}{Back.RESET}"
            elif style:
                return f"{color}{style}{string}{Fore.RESET}{Style.RESET_ALL}"
            else:
                return f"{color}{string}{Fore.RESET}"


def ValidatePath(path: Path | str) -> bool:
    """Retorna un booleano dependiendo de si el Path o el Path de la string existe o es un archivo"""
    if isinstance(path, str):
        fpath = Path(path)
        if not fpath.exists() or not fpath.is_file():
            return False
        else:
            return True
    elif isinstance(path, Path) and not path.exists() or not path.is_file():
        return False
    else:
        return True


def ReadLines(StrOrPath: Path | str) -> list[int]:
    """Lee las lineas de un archivo y devuelve el numero de lineas.\n
    ``list[0]`` -> Total lines\n
    ``list[1]`` -> Total lines without White lines\n
    ``list[2]`` -> White lines
    """
    if ValidatePath(StrOrPath):
        with open(StrOrPath if isinstance(StrOrPath, Path) else Path(StrOrPath), "r+b") as log:
            if os.path.getsize(log.name) == 0:
                return Logger("w", "El archivo esta vacio")
            else:
                pass
            mm = mmap.mmap(log.fileno(), 0, access=mmap.ACCESS_READ)
            total_lines = 0
            white_lines = 0

            for line in iter(mm.readline, b""):     #* b"" para leer en binario. El salto de linea == '\r\n'
                if line == b"\r\n":         
                    white_lines += 1
                else:
                    total_lines += 1
            log.close()                    
        return [total_lines+white_lines, total_lines, white_lines]
    else:
        return ValidatePath(StrOrPath)


def getSize(filePathOrStr: Path | str):
    if ValidatePath(filePathOrStr):
        return round(os.path.getsize(filePathOrStr)/1000, 2)
    else:
        return


def getInfo(filePathOrStr: Path | str) -> dict:
    TIME_FMT = "%Y-%m-%d %H:%M:%S"
    if ValidatePath(filePathOrStr):
        finfo = {}
        afile = t.strftime(TIME_FMT, t.localtime(os.path.getatime(filePathOrStr)))
        mfile = t.strftime(TIME_FMT, t.localtime(os.path.getmtime(filePathOrStr)))
        cfile = t.strftime(TIME_FMT, t.localtime(os.path.getctime(filePathOrStr)))    #* Devuelve la hora de creacion del archivo
        sfile = getSize(filePathOrStr)
        ext = os.path.splitext(filePathOrStr)[1]   #* Divide la ruta en dos, donde el segundo elemento es la ext.
        with open(filePathOrStr, "r+") as file:
            Tobytes = Path(filePathOrStr).read_bytes() if not isinstance(filePathOrStr, Path) else filePathOrStr.read_bytes()
            enc = file.encoding
        finfo["Name"] = file.name
        finfo["Absolute path"] = Path(filePathOrStr).absolute().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.absolute().as_posix()
        finfo["Home directory"] = Path(filePathOrStr).home().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.home().as_posix()
        finfo["Last access"] = afile
        finfo["Last modification"] = mfile
        finfo["Creation data"] = cfile
        finfo["File size"] = f"{sfile} KB"
        finfo["Total lines"] = ReadLines(filePathOrStr)[1]
        finfo["Extension"] = ext
        finfo["Language"] = detect(Tobytes).get("language") if detect(Tobytes).get("language") else "Unknown"
        finfo["Encoding"] = enc

        for k in finfo.keys():
            print(f"{cFormatter(k, color= Fore.LIGHTYELLOW_EX)}: {cFormatter(finfo[k] ,color= Fore.LIGHTWHITE_EX)}")
    else:
        return ValidatePath(filePathOrStr)


def checkPassword(hash_password: str | list, primitive_password: str) -> bool:
    if not isinstance(hash_password, list) and not hash_password.startswith("pbkdf2:"):
        raise TypeError("La contraseña no esta encriptada o no es un hash de contraseña.")
    else:
        if isinstance(hash_password, list):
            for p in hash_password:
                if check_password_hash(p, primitive_password):
                    return True
                else:
                    pass
        else:
            return check_password_hash(hash_password, primitive_password)