import asyncio
from json import dumps
import logging
import os
import mmap
import logging

from pathlib import Path, PurePath
from sqlite3 import Connection
import time as t

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
#* //////////////////////////////

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


class Checker:
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

    @staticmethod
    def ValidatePath(path: Path | str) -> bool:
        """Retorna un booleano dependiendo de si el Path o el Path de la string existe o es un archivo"""
        if isinstance(path, str):
            fpath = Path(path)
            if not fpath.exists() or not fpath.is_file():
                return False
            return True
        elif isinstance(path, PurePath) and not path.exists() or not path.is_file():
            return False
        else:
            return True

    @staticmethod
    def ReadLines(StrOrPath: Path | str) -> list[int]:
        """Lee las lineas de un archivo y devuelve el numero de lineas.\n
        ``list[0]`` -> Total lines\n
        ``list[1]`` -> Total lines without White lines\n
        ``list[2]`` -> White lines
        """
        if Checker.ValidatePath(StrOrPath):
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
            return Checker.ValidatePath(StrOrPath)

    @staticmethod
    def GetFileSize(filePathOrStr: Path | str):
        if Checker.ValidatePath(filePathOrStr):
            return round(os.path.getsize(filePathOrStr)/1000, 2)
        else:
            return Checker.ValidatePath(filePathOrStr)

    @staticmethod
    def GetFileInfo(filePathOrStr: Path | str) -> dict:
        if Checker.ValidatePath(filePathOrStr):
            finfo = {}
            afile = t.asctime(t.localtime(os.path.getatime(filePathOrStr)))
            mfile = t.asctime(t.localtime(os.path.getmtime(filePathOrStr)))
            cfile = t.asctime(t.localtime(os.path.getctime(filePathOrStr)))    #* Devuelve la hora de creacion del archivo
            sfile = Checker.GetFileSize(filePathOrStr)
            ext = os.path.splitext(filePathOrStr)[1]   #* Divide la ruta en dos, donde el segundo elemento es la ext.
            with open(filePathOrStr, "r+") as file:
                enc = file.encoding
            finfo["Name"] = file.name
            finfo["Absolute path"] = Path(filePathOrStr).absolute().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.absolute().as_posix()
            finfo["Home directory"] = Path(filePathOrStr).home().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.home().as_posix()
            finfo["Last access"] = afile
            finfo["Last modification"] = mfile
            finfo["Creation data"] = cfile
            finfo["File size"] = f"{sfile} KB"
            finfo["Total lines"] = Checker.ReadLines(filePathOrStr)[1]
            finfo["Extension"] = ext
            finfo["Enconding"] = enc
            return finfo
        else:
            return Checker.ValidatePath(filePathOrStr)

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
    
    async def checkAll(self, log_path: Path | str, temp_db: Connection, main_db: Connection = None):
        """Coroutine para verificar con un solo metodo toda la configuracoin del log y bases de datos.\n
        Segun si se importa una configuracion o con los valores predeterminados."""
        self.logger.info("Iniciando Chequeo de toda la configuracion...")
        await asyncio.sleep(2)
        await self.CheckLog(log_path)
        await asyncio.sleep(2)
        await self.CheckTempDB(db=temp_db)
        #await self.CheckMainDB(main_db)
        self.logger.info("Chequeo finalizado.")

    async def CheckLog(self, log_path: Path | str, max_lines: int = 200):
        self.logger.debug("Iniciando Chequeo de Log...")
        if not self.ValidatePath(log_path):
            self.logger.error(f"El archivo '{log_path}' no existe o no es un archivo valido (Solo texto).")
            return self.logger.error("Se ha encontrado un error en el chequeo del log.")
        else:
            with open(log_path, "r+") as log:
                mm = mmap.mmap(log.fileno(), 0)
                total_lines = 0
                while mm.readline():
                    total_lines += 1

                if total_lines >= max_lines:
                    dumped_log = log.read()
                    self.logger.warning(f"El archivo '{log_path}' tiene {total_lines} lineas.")
                    self.logger.warning("Limpiando el archivo log...")
                    log.write("")
                    log.flush()
                    log.close()
                    with open("log.txt", "a+") as log:
                        log.write(dumped_log)
                        self.logger.info(f"Se ha creado un archivo con la copia del ultimo log con el nombre {log.name} (Debido a que se ha limpiado).")
                        log.close()
                else:
                    return self.logger.info("Chequeo de Log finalizado con exito.")

    async def CheckTempDB(self, db_name: str, db_conn: Connection, max_elems: int = 500, max_size: int = 50000):
        print(self.logger.info("Iniciando Chequeo de la base de datos temporal..."))
        
        if max_size:
            tempdb_size = self.GetFileSize(db_name)
            if tempdb_size >= max_size:
                return self.logger.warning(f"La base de datos temporal tiene un tamaño de {tempdb_size} KB, supera el tamaño permitido.")
            else:
                return self.logger.info("Chequeo de la base de datos temporal finalizado con exito.") 
        elif max_elems:
            tables = [t for t in db_conn.execute('SELECT name FROM sqlite_master WHERE type= "table"')]     
            #TODO: La tabla 'sqlite_master' contiene todas las tablas de la base de datos
            tempdb_elems = len(db_conn.execute(f"SELECT * FROM '{[t for t in tables]}'").fetchall())
            if tempdb_elems >= max_elems:
                db_conn.execute(f"DELETE FROM {[t for t in tables]}")
                self.logger.error(f"La base de datos temporal tiene {tempdb_elems} elementos, supera el numero de elementos permitido.")
                return self.logger.warning(f"Borrados | {tempdb_elems} | elementos")
            else:
                return self.logger.info("Chequeo de la base de datos temporal finalizado con exito.") 
        else:
            return self.logger.info("Chequeo de la base de datos temporal finalizado con exito")

    async def CheckTempDB(self, db: Connection, max_elems: int = 500, max_size: int = 50000):
        pass

print(Checker.GetFileInfo("requeriments.txt"))