import logging
import os

from time import strftime
from utils import *
from colorama import Fore, Back, Style #, init
from pathlib import Path
from sqlite3 import Connection
from asyncio import sleep #, create_task

__all__ = [
    "CustomFmt",
    "Checker",
    "FMT",
    "FORMATS"
]


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

FMT = "[{levelname:^4}] [{name}] [{asctime}]: {message}"
FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[32m{FMT}\33[0m",            #* Green
    logging.WARNING: f"\33[1m\33[95m{FMT}\33[0m",   #* Cyan
    logging.ERROR: f"\33[31m{FMT}\33[0m",           #* Red
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",  #* Bold Red
}

class CustomFmt(logging.Formatter):
    """Subclase de ``logging.Formatter`` que ofrece un formateo preconfigurado para DEBUG; INFO; WARNING; ERROR Y CRITICAL.\n
    Asignar de esta manera:\n
    ``handler = logging.StreamHandler()``\n
    ``handler.setFormatter(CustomFmt())``\n
    ``logging.basicConfig(..., handler= [handler])``\n
    """
    def format(self, entry):
        log_fmt = FORMATS[entry.levelno]
        formatter = logging.Formatter(log_fmt, style="{", datefmt= '%Y-%m-%d %H:%M:%S')
        return formatter.format(entry)


#* To this file logging
handler = logging.StreamHandler()
handler.setFormatter(CustomFmt())
logging.basicConfig(
    level= logging.INFO,
    handlers=[handler]
)


class Checker:

    TIME_FMT = "%Y-%m-%d |- %H:%M:%S"

    def __init__(self, type_or_class: type, import_config: dict = None):
        self.obj = type_or_class
        self.logger: Logger = logging.getLogger("Checker")
        self.logger.info(f"Iniciando Chequeo para '{type_or_class.__class__.__name__}'")
        if import_config is not None:
            try:
                self.config = import_config
                self.logger.info("Configuracion importada.")
            except not self._ValidateConfig(self.config):
                self.logger.error("Error al importar la configuracion.")

    def _ValidateConfig(self, config: dict) -> bool:
        for ck, value in config.items():
            if ck not in ["Log", "TempDB", "MainDB"]:
                return self.logger("Las claves validas para la configuracion son: ['Log', 'TempDB', 'MainDB']")
            for cv in value.keys():
                if cv not in ["MaxElems", "MaxLines", "MaxSize"]:
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
                        if isinstance(config[ck][cv], int):
                            if config[ck][cv] < 10:
                                self.logger("El valor MaxLines debe ser mayor a 10.")
                                return False
                            else:
                                self.max_lines = config[ck][cv]
                                return True
                        else:
                            self.logger("El valor MaxLines debe ser un numero entero.")
                            return False
                    elif cv == "MaxSize":
                        if isinstance(config[ck][cv], int):
                            if config[ck][cv] < 0:
                                self.logger("El valor MaxSize debe ser mayor a 0 KB.")
                                return False
                            else:
                                self.max_size_kb = config[ck][cv]
                                return True

                        else:
                            self.logger("El valor MaxSize debe ser un numero entero.")
                            return False
    
    async def checkAll(self, *kwargs, log_path: Path | str, temp_db: Connection, main_db: Connection = None):
        """Coroutine para verificar con un solo metodo toda la configuracion del log y bases de datos.\n
        Segun si se importa una configuracion o con los valores predeterminados."""
        self.logger.info("Iniciando Chequeo de toda la configuracion...")
        await sleep(2)
        await self.CheckLog(*kwargs, log_path=log_path)
        # await sleep(2)
        await self.CheckTempDB(*kwargs, db_conn=temp_db)
        #await self.CheckMainDB(*kwargs, main_db)
        self.logger.info("Chequeo finalizado.")

    async def CheckLog(self, log_path: Path | str, max_lines: int = 5, log_dump_loc: Path | str = None):
        self.logger.debug("Iniciando Chequeo de Log...")
        if not ValidatePath(log_path):
            self.logger.error(f"El archivo '{log_path}' no existe o no es un archivo valido (Solo texto).")
            return self.logger.error("Se ha encontrado un error en el chequeo del log.")
        else:
            lines = ReadLines(log_path)[1]
            if lines < max_lines:
                return self.logger.info("Chequeo de Log finalizado con exito.")
            self.logger.warning(f"El archivo '{log_path}' tiene {lines} lineas cuando el maximo es {max_lines}.")
            self.logger.warning("Limpiando el archivo log y generando una copia...")
            log_content = Path(log_path).read_text()
            with open(log_path, "w+") as log:
                log.write("")
                log.close()
            if log_dump_loc is not None and ValidatePath(log_dump_loc):
                if isinstance(log_dump_loc, str):
                    log_dump_loc = Path(log_dump_loc)
                relative_path = os.path.join(log_dump_loc, f"log_dump_{strftime(self.TIME_FMT)}.txt")
                with open(relative_path, "w+") as log_copy:
                    log_copy.write(log_content)
                    self.logger.info(f"Se ha creado un archivo con la copia del ultimo log con el nombre '{log_copy.name}' (Debido a que se ha limpiado).")
                    log_copy.close()

    async def CheckTempDB(self, db_conn: Connection, max_elems: int = 500, max_size_kb: int = 50000):
        self.logger.info("Iniciando Chequeo de la base de datos temporal...")

        tempDbMetadata = db_conn.execute('PRAGMA database_list;').fetchall()        #* Obtenemos el nombre de la base de datos con PRAGMA database_list
        tempDbPath = Path(tempDbMetadata[0][2])
        if max_size_kb:
            tempdb_size = getSize(tempDbPath)
            if tempdb_size >= max_size_kb:
                return self.logger.warning(f"La base de datos temporal tiene un tamaño de {tempdb_size} KB, supera el tamaño permitido.")
            else:
                return self.logger.info("Chequeo de la base de datos temporal finalizado con exito.")
        elif max_elems:
            self.tables = list(
                db_conn.execute('SELECT * FROM sqlite_master WHERE type="table"')
            )
            #TODO: La tabla 'sqlite_master' contiene todas las tablas de la base de datos
            tempdb_elems = len(
                db_conn.execute(f"SELECT * FROM '{list(self.tables)}'").fetchall()
            )
            if tempdb_elems >= max_elems:
                db_conn.execute(f"DELETE FROM {list(self.tables)}")
                self.logger.error(f"La base de datos temporal tiene {tempdb_elems} elementos, supera el numero de elementos permitido.")
                return self.logger.warning(f"Borrados | {tempdb_elems} | elementos")
            else:
                return self.logger.info("Chequeo de la base de datos temporal finalizado con exito.")
        else:
            print(self.tables)
            return self.logger.info("Chequeo de la base de datos temporal finalizado con exito")

    async def CheckMainDB(self, db: Connection, max_elems: int = 500, max_size_kb: int = 50000):
        pass


if __name__ == "__main__":
    print(Checker.getInfo("log.txt"))