import asyncio
import logging
import os
import logging
import datetime
from pathlib import Path

#* ////////////
#*  COLORS
#* ////////////

    #\33[30m	Black
    #\33[31m	Red
    #\33[32m	Green
    #\33[33m	Yellow
    #\33[34m	Blue
    #\33[35m	Purple
    #\33[36m	Cyan
    #\33[37m	White

#? Add \33[1m\33[<ansiref>]{FMT}\33[0m to add bolb messages


FMT = "[{levelname:^4}] [{name}] {asctime}: {message}"
FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[32m{FMT}\33[0m",            #* Green
    logging.WARNING: f"\33[1m\33[95m{FMT}\33[0m",   #* Cyan
    logging.ERROR: f"\33[31m{FMT}\33[0m",           #* Red
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",  #* Bold Red
}


class CustomFmt(logging.Formatter):
    def format(self, entry):
        log_fmt = FORMATS[entry.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(entry)

handler = logging.StreamHandler()
handler.setFormatter(CustomFmt())
logging.basicConfig(
    level= logging.INFO,
    handlers=[handler],
    datefmt= datetime.datetime.now().astimezone(),
)

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
        return log.warn(text)
    elif level == "c":
        return log.critical(text)
    elif level == "e":
        return log.error(text)
    else:
        return "Ha ocurrido un error. Establezca ['i', 'w', 'c' o 'e'] como valores para el parametro ['level']"


class Checker:
    def __init__(self, type_or_class: type, logger: logging.Logger = None):
        self.obj = type_or_class
        self.logger: Logger = Logger()
    
    async def LogControl(self, log_path: Path | str):
        if log_path == type(str) and not Path(log_path).exists() or not Path(log_path).is_file():
            return self.logger("e", f"El archivo '{log_path}' no existe o no es un archivo.")
        elif not log_path.exists() or log_path.is_file():
            return self.logger("e", f"El archivo '{log_path}' no existe o no es un archivo.")
        else:
            ...
            


