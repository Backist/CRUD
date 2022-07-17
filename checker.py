import asyncio
import logging
import os
import logging
import datetime
from time import sleep
from pathlib import Path
from mmap import mmap
from sqlite3 import Connection

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


#//////////////////////////////////////////////////////////////////////////////////////////////
#TODO: TODO POR ARREGLAR (NO FUNCIONA NADA)
#//////////////////////////////////////////////////////////////////////////////////////////////


class Checker:
    def __init__(self, type_or_class: type, import_config: dict = None, logger: logging.Logger = None):
        self.obj = type_or_class
        self.logger: Logger = logger if logger else logging.getLogger("Checker")
        self.logger.info(f"Iniciando Chequeo para '{type_or_class}'")
        if import_config is not None:
            try:
                self.config = import_config
                self.logger.info("Configuracion importada.")
            except not self._ValidateConfig(self.config):
                self.logger.error("Error al importar la configuracion.")

    @staticmethod
    def _ValidatePath(path: Path | str) -> bool:
        if isinstance(path, str) and not Path(path).exists() or Path(path).is_file():
            return False
        else:
            if not path.exists() or not path.is_file():
                return False
            return True

    def _ValidateConfig(self, config: dict) -> bool:
        for ck in config.keys():
            if not ck in ["Log", "TempDB", "MainDB"]:
                return self.logger("Las claves validas para la configuracion son: ['Log', 'TempDB', 'MainDB']")
            else:
                for cv in config[ck].keys():
                    if not cv in ["MaxElems", "MaxLines", "MaxSize"]:
                        self.logger("Los valores configurables en cada caso son: ['Log': 'MaxLines' | 'TempDB': 'MaxElems', 'MaxSize' | 'MainDB': 'MaxSize', 'MaxElems']")
                        return False
                    else:
                        if cv == "MaxElems":
                            if not isinstance(config[ck][cv], int):
                                self.logger("El valor MaxElems debe ser un numero entero.")
                                return False
                            elif config[ck][cv] < 10:
                                    self.logger("El valor MaxElems debe ser mayor o igual a 10.")
                                    return False
                            else:
                                self.max_elems = config[ck][cv]
                                return True
                        elif cv == "MaxLines":
                            if not isinstance(config[ck][cv], int):
                                self.logger("El valor MaxLines debe ser un numero entero.")
                                return False
                            else:
                                if config[ck][cv] < 10:
                                    self.logger("El valor MaxLines debe ser mayor a 10.")
                                    return False
                                else:
                                    self.max_lines = config[ck][cv]
                                    return True
                        elif cv == "MaxSize":
                            if not isinstance(config[ck][cv], int):
                                self.logger("El valor MaxSize debe ser un numero entero.")
                                return False
                            else:
                                if config[ck][cv] < 0:
                                    self.logger("El valor MaxSize debe ser mayor a 0 KB.")
                                    return False
                                else:
                                    self.max_size = config[ck][cv]
                                    return True
    
    async def checkAll(self, log_path: Path | str, temp_db: Connection, main_db: Path | str = None):
        self.logger.info("Iniciando Chequeo de todos los metodos...")
        sleep(2)
        await self.CheckLog(log_path)
        sleep(2)
        await self.CheckTempDB(temp_db)
        sleep(2)
        #await self.CheckMainDB(main_db)
        sleep(2)
        self.logger.info("Chequeo finalizado.")

    async def CheckLog(self, log_path: Path | str, max_lines: int = 200):
        self.logger.info("Iniciando Chequeo de Log...")
        if self._ValidatePath(log_path) == False:
            self.logger.error(f"El archivo '{log_path}' no existe o no es un archivo valido (Solo texto).")
            return self.logger.error("Se ha encontrado un error en el chequeo del log.")
        else:
            with open(log_path, "r+") as log:
                mm = mmap(log.fileno(), 0)
                total_lines = 0
                while mm.readline():
                    total_lines += 1

                dumped_log = mm.readlines().decode("utf-8").split("\n")
                print(dumped_log)       #TODO: Eliminar mas tarde
                if total_lines >= max_lines:
                    self.logger.error(f"El archivo '{log_path}' tiene {total_lines} lineas.")
                    self.logger.error("Limpiando el archivo log...")
                    log.write("")
                    pass
                else:
                    log.flush()  #* Flush the file to disk
                    log.close()
            with open("log.txt", "a+") as log:
                log.write(dumped_log)
                self.logger.info(f"Se ha creado un archivo con la copia del ultimo log con el nombre {log.name} (Debido a que se ha limpiado).")
            return self.logger.info("Chequeo de Log finalizado con exito.")

    async def CheckTempDB(self, db_path: Connection, max_elems: int = 500, max_size: int = 50000):
        self.logger.info("Iniciando Chequeo de la base de datos temporal...")

        if max_size:
            tempdb_size = os.path.getsize(Path(db_path.__getattribute__("database")))/1000, 2
            if tempdb_size >= max_size:
                return self.logger.error(f"La base de datos temporal tiene un tamaño de {tempdb_size} KB, supera el tamaño permitido.")
            else:
                if max_elems:
                    tempdb_elems = len(db_path.execute("SELECT * FROM tempdb").fetchall())
                    if tempdb_elems >= max_elems:
                        return self.logger.error(f"La base de datos temporal tiene {tempdb_elems} elementos, supera el numero de elementos permitido.")
                    else:
                        return self.logger.info("Chequeo de la base de datos temporal finalizado con exito.")

    async def CheckTempDB(self, db_path: Connection, max_elems: int = 500, max_size: int = 50000):
        pass




            


