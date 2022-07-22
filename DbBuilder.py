import sqlite3 as sql
from tabnanny import check
import time as t
import os.path #* Para saber todo acerca de un archivo (tamaño, tipo, historial de cambios, etc.)
import os
import checker

#* import sqlalchemy para uso de db en API's o Webs

from asyncio import run
from colorama import Fore, Style, Back #, init
from dataclasses import dataclass
from datetime import datetime
from platform import python_version
from typing import NoReturn
from json import dumps
from pathlib import Path
from random import choice, randint, sample
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash


__all__: list[str] = ["User", "cFormatter", "Database"]     
#TODO: Solo se importaran esos modulos o clases pero los metodos o funciones privados no seran importados


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

    c = [Fore.BLACK, Fore.RED, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.WHITE]
    s = [Style.DIM, Style.NORMAL, Style.BRIGHT]
    b = [Back.BLACK, Back.RED, Back.BLUE, Back.CYAN, Back.GREEN, Back.MAGENTA, Back.YELLOW, Back.WHITE]

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

def cls():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


@dataclass(init=True)
class User:
    """Dataclase para instanciar usuarios para poder acceder a la base de datos.\n
    Si necesitamos acceder a la base de datos, deberemos utilizar el metodo de clase `Database.CreateToken` para asignar a un usuario un token valido
    para acceder a la base de datos."""

    class UserError(Exception):
        """
        Clases para manejar los errores u excepciones de la clase User.
        """
        pass

    def __init__(self, username: str, password: str, email: str = None,ids_range: list[int] | tuple[int] = []):
        self.username: str = username
        self.email: str = email
        self.token: str = None
        self._ids_range: list[int] | tuple[int] = ids_range

        if len(password) < 8 or len(list(filter(lambda char: str(char) in password, list(range(0, 9+1))))) == 0:
            raise User.UserError(cFormatter("La contraseña debe tener al menos 8 caracteres y contener al menos un número.", color= Fore.RED))
        else:
            self.password: str = password
        self.UId = self._AsignIdentifier()

    def encryptPassword(self, mode: str = "pbkdf2:sha256"):
            encryp = generate_password_hash(self.password, mode, salt_length= 32)
            return encryp

    def _AsignIdentifier(self) -> int:
        """
        Asigna un identificador a un usuario
        """
        avariable_ids = list(range(1000, 10000+1))  #* +1 para incluir el numero (ya que empieza a contar desde el cero)
        #* Definimos unalista predeterminada por si no se configura ningun intervalo

        if self._ids_range:
            if self._ids_range[0] > self._ids_range[1]:
                print(cFormatter("El primer indice debe ser el término mas pequeño del intervalo", color= Fore.RED))
                return User.UserError()
            elif len(self._ids_range) > 2:
                print(cFormatter("El intervalo debe ser entre un máximo de 2 numeros comprendidos. E.g [1, 100]", color= Fore.RED))
                return User.UserError()
            elif self._ids_range[1]-self._ids_range[0]:
                print(cFormatter("Debe de haber una distacia de al menos 50 entre numeros del intervalo. E.g [1, 100]", color= Fore.RED))
                return User.UserError()
            else:
                avariable_ids = list(range(self._ids_range[0], self._ids_range[1]+1))
                self._identifier = avariable_ids.pop(randint(0, len(avariable_ids)))
                return self._identifier
        else:   
            self._identifier = avariable_ids.pop(randint(0, len(avariable_ids)))
            return self._identifier
        

    def __str__(self) -> str:
        secret_password = "*" * len(self.password[:-4])+self.password[-4:]  #* Si se printea el objeto, se muestran los cuatro ultimos caracteres de la contraseña
        userDict = {
            "Username": self.username,
            "Email": self.email,
            "UId": self.UId,
            "Token": self.token if self.token is not None else "No posee token",
            "Password": secret_password,
            "Created at": self.created_at
        }
        return dumps(userDict, indent= 4)

    @property
    def created_at(self) -> str:
        """
        Devuelve la fecha de creacion del usuario
        """
        return t.strftime('%Y-%m-%d %H:%M:%S')
                #? datetime.datetime.now()


class Database:
    """
    Instancia un objeto de clase Database. Es decir, el objeto actua como base de datos.

    ## Importante:
    El acceso a la base de datos
    """

    class DatabaseInitializationError(Exception):
        """
        Clases para manejar los errores u excepciones de la clase Database.
        """
        pass

    class Clock:

        ClockErrorMsg = cFormatter("El cronometro no esta activo. (Probablemente porque no se ha iniciado una conexion con la base de datos)", color= Fore.RED)

        def __init__(self, refresh_timer_ms: int = 500):
            self.Clockrefresh = refresh_timer_ms
            self._initTime = datetime.now()
            self._active = False

        @property
        def active(self):
            return self._active if self._active else print(self.ClockErrorMsg)

        def _calc_passed_time_format(self):
            passed_seconds = (datetime.now() - self._initTime).total_seconds()
            return self._primitive_timer(int(passed_seconds))
            
        def _primitive_timer(self, segundos):
            horas = int(segundos / 60 / 60)
            segundos -= horas*60*60
            minutos = int(segundos/60)
            segundos -= minutos*60
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        
        def timer(self):
            while True:
                self._active = True
                print(self._calc_passed_time_format(), end= '\r')
            
        def pauseTimer(self):
            if self.active:
                self._initTime = datetime.now()
                self._active = False
            else:
                return print(self.ClockErrorMsg)

        def activeTimer(self):
            """Activa el cronometro si esta pausado.\nTambien lo hace si esta parado pero es mejor utilizar el metodo ``.timer()``"""
            if self.active:
                pass
            else:
                self._active = True
                return self._calc_passed_time_format()

        def resetTimer(self):
            if self._active:
                self._initTime = datetime.now()
                print(cFormatter("El cronometro se ha reseteado", color= Fore.GREEN))
            else:
                return print(self.ClockErrorMsg)


    def __init__(self, user: User = None, log_path: Path = None):
        self.user: User | str = user if user is not None else "Invitado"
        self.userToken = user.token if user is not None else None
        try:
            self.log_path: Path = log_path if log_path is not None else Path("log.txt")
        except not checker.Checker.ValidatePath(log_path):
            raise Database.DatabaseInitializationError(cFormatter("El archivo de log no existe o no es valido (Probablemente no sea un archivo o no de tipo texto)", color= Fore.RED))
        self.EntryDataEnabled: bool = None
        self.Running: bool = False
        self.CheckEntryDataEnabled()       #* Comprobamos si se pueden introducir datos en la base de datos
        self.Checker = checker.Checker(self)
        try:
            run(self.Checker.checkAll(self.log_path, self._InitTempDb()))
        except KeyboardInterrupt:
            raise Database.DatabaseInitializationError(cFormatter(
                "Se ha parado el chequeo de las configuraciones, inicializacion pausada.", 
                color= Fore.YELLOW
                )
            )
        self.CloseConnection()

    @property
    def in_transaction(self):
        """
        Devuelve True si hay una transaccion en curso
        """
        return self.conn.in_transaction() if self.is_operative else print(cFormatter("No se ha iniciado la base de datos", color= Fore.RED))

    @property
    def is_operative(self) -> list[bool | str]:
        """
        Devuelve el estado de la base de datos
        """
        return self.Running

    @property
    def runtime(self):
        """Devuelve el tiempo que lleva la base de datos encendida"""
        return self.DbRunTime if self.is_operative else cFormatter("No se ha iniciado la base de datos", color= Fore.RED)


    @classmethod
    def CreateToken(cls, user: User) -> str:
        """
        Crea un token unico que se asigna a un usuario.
        El token es una cadena de caracteres aleatoria de 16 caracteres privada y unica para cada usuario.
        """
        
        temp_db = cls._InitTempDb(cls)
        used_tokens = temp_db.execute("SELECT Tokens from AUC").fetchall()

        minus = "abcdefghijklmñopqrstuwxyz"
        mayus = minus.upper()
        symbols = "@#/-*&'=€"
        numbers = "0123456789"
        base = (minus + numbers + mayus + symbols)

        extract = sample(base, 16)
        token = "8/x::"+"".join(extract)

        if not token in used_tokens:
            temp_db.execute(f"INSERT INTO AUC (Tokens) VALUES ('{token}')")     #! Muy importante las comillas a pesar de hacer f-string
            temp_db.commit()
            temp_db.close()
            user.token = token
            return token
        else:
            return cls.CreateToken(user)

    def _LogWritter(
        self, 
        message: str, 
        username: str | User, 
        level: str = "INFO",
        timestamp: str | datetime = t.strftime('%Y-%m-%d %H:%M:%S') ,
        special_info: list | tuple = None,
        max_lines: int = 1000, 
    ) -> str | Exception:
        """Escribe cada evento en el archivo log.
        
            # Parametros:

                (Opcional) ``timestamp``: | ``str`` = ``t.strftime('%Y-%m-%d %H:%M:%S')`` | Fecha y hora de la accion o evento.
                (Obligatorio) ``message``: | ``str`` | Mensaje que se escribe en el log.
                (Obligatorio) ``username``: | ``str`` | User, Usuario que realiza la accion.
                (Obligatorio) ``level``: | ``str`` | Nivel de importancia del evento o acción.
                (Obligatorio) ``special_info``: | ``list | tuple`` | Lista de parametros especiales a mostrar junto con el nombre de usuario
                (Opcional) ``max_lines``: | ``int`` = ``1000`` | Numero de lineas para borrar el contenido del archivo log (limpieza).
        """

        valid_levels = ["INFO", "WARNING", "ERROR", "CRITICAL", "SPECIAL_EVENT"]

        if not level.upper() in valid_levels:
            print(cFormatter(f"El nivel de importancia no es valido. Niveles de importancia admitidos: {[l for l in valid_levels]}", color= Fore.RED))
            return
        else:
            for l in valid_levels:
                if l == level.upper():
                    try:
                        with open(self.log_path, "a+") as log:   #* a+ indica que se abre el archivo si existe de lo contrario lo crea, y se escribe al final del mismo.
                            log.write(f"[{timestamp}][{l}] - | {username} ({special_info}) | -> {message}\n")
                            log.close()
                    except Exception as e:
                        print(cFormatter("Error al escribir en el log: ", color=Fore.RED)+cFormatter(f"{e}", color= Fore.CYAN))
                        return


    def _InitThreadClock(self) -> None:
        """Inicia una funcion en un hilo independiente que se encarga de llevar y actualizar el tiempo que lleva la base de datos operativa"""
        self.DbRunTime = 0
        self.Running = True
        self._DbRunTimeThread = Thread(target=self._Clock, name= "Db-BaseClock", args=())
        try:
            self._DbRunTimeThread.start()
        except KeyboardInterrupt:
            print(cFormatter("Se ha interrumpido la ejecucion de la base de datos", color=Fore.RED))
            self.Running = False
            self._DbRunTimeThread.join()

    
    def _Clock(self) -> Clock | NoReturn:
        """Funcion que se encarga de llevar y actualizar el tiempo que lleva la base de datos operativa"""
        timer = self.Clock()
        self.DbRunTime = timer.timer()


    def _InitTempDb(self, max_elems: int = 500) -> sql.Connection:
        """
        Inicializa la base de datos temporal para la ejecucion de las pruebas y para verificar algunos parametros y permisos.

        ## Importante:
        La base de datos debe cerrarse para que los cambios surgan efecto
        """
        TempDbWakeTime = t.time()

        self.temp_db_path = Path("PUC.db")
        self.conn = sql.connect(self.temp_db_path.name)    #* Private User Credentials (PUC)
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            UId INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT,
            Userlevel INTEGER,
            Email TEXT,
            Password TEXT,
            Token TEXT,
            Created_at TIMESTAMP ASC
        )
        """)
        self.c.execute("""                  
        CREATE TABLE IF NOT EXISTS AUC (    
            Tokens NTEXT,
            IDs INTEGER
        ) 
        """)                        #TODO: AUC --> Already Used Credentials              
        self.conn.commit()

        if len(self.c.execute(f"SELECT * from users").fetchall()) >= max_elems:
            self.delElems()
            print(cFormatter("Eliminados 500 elementos para limpieza de la base de datos temporal"))
        else:
            pass
        TempDbWakeTime = round((t.time()-TempDbWakeTime)*1000, 2)
        print(cFormatter(f"Base de datos temporal inicializada en {TempDbWakeTime} ms", color=Fore.GREEN))
        return self.conn        

    def reseTables(self, table: str):
        """
        Resetea las tablas de la base de datos
        """
        self.c.execute(f"DROP TABLE {table}")
        self.conn.commit()

    def delAct(self, elem: str = None, table: str = "users") -> None:
        """Elimina elementos de la tabla de datos.
        Si no se pasa un elemento a eliminar, el metodo borrará todos los elementos de la tabla users (Excepto que se proporcione una)"""
        if elem:
            self.c.execute(f"DELETE FROM {table} WHERE {elem} =")
            self.conn.commit()
        else:
            self.c.execute(f"DELETE FROM {table}")
            self.conn.commit()

    def DbDiskSize(self):
        return f"{round(os.path.getsize(Path('PUC.db'))/1000, 2)} KB"


    def CheckEntryDataEnabled(self) -> bool:
        
        temp_db = self._InitTempDb()
        dumped_data = temp_db.execute("SELECT * FROM users").fetchall()   
        flist = [f for f in dumped_data]
        ids = [i[0] for i in flist]
        usernames = [u[1] for u in flist]
        tokens = [t[5] for t in flist]       

        if not self.user == "Invitado":
            if self.userToken is not None:
                if self.userToken in tokens:
                    self._LogWritter(f"Se ha habilitado la entrada de datos", self.user.username, special_info= [self.user.token])
                    self.EntryDataEnabled = True
                    return True
                elif self.userToken not in tokens and self.user.UId in ids:
                    print(cFormatter(f"Se ha encontrado un usuario activo con el mismo nombre de usuario pero con un token diferente.Por favor, compruebe su token y si es necesario cree una de nuevo", color= Fore.YELLOW))
                    self.EntryDataEnabled = False
                    return False
                else:
                    temp_db.execute("INSERT INTO users (UId, Username, Email, Password, Token, Created_at) VALUES (?, ?, ?, ?, ?, ?)", (self.user.UId ,self.user.username, self.user.email, self.user.encryptPassword(), self.user.token, self.user.created_at))
                    print(cFormatter(f"Se ha añadido al usuario {self.user.username} con ID [{self.user.UId}] a usuarios permitidos", color= Fore.GREEN))
                    self._LogWritter(f"Se ha habilitado la entrada de datos", self.user.username, special_info= [self.user.token])
                    self.EntryDataEnabled = True
                    return True
            else:
                self.EntryDataEnabled = False
                print(cFormatter(f"El usuario {self.user.username} no posee un token asignado para acceder a la base de datos. Use ``Database.CreateToken()`` para asignar un token unico al usuario.", color= Fore.YELLOW))
                return False
        else:
            self.EntryDataEnabled = False
            print(cFormatter(f"El usuario no esta en usuarios activos y solo puede acceso a ver la base de datos, accedera como INVITADO", color=Fore.YELLOW))
            return False



    #TODO: <--------- PUBLIC METHODS ---------->

    def BuildConnection(
        self, 
        _db: str | Path,
        _timeout: int | float = 5,
        _detect_types: int = 0,
        _isolation_level: str | None = None, #* None para usar 'autocommit' para guardar cambios
        _check_same_thread: bool = True,
        _cached_statements: int = 100,
        _uri: bool | str = False,
        user: str = None   
    ):
        """
        Comienza una conexion con la base de datos e inicializa las tablas internas predeterminadamente
        """
        
        self.DbWakeTime = t.time()
        self.conn = sql.connect(
            database= _db,
            timeout= _timeout,
            detect_types= _detect_types,
            isolation_level= _isolation_level,
            check_same_thread= _check_same_thread,
            cached_statements= _cached_statements,
            uri= _uri
        )
        self._InitThreadClock()                                             #TODO: Marcamos la conexion como operativa
        self.DbWakeTime = round((t.time()-self.DbWakeTime)*1000, 4)     #TODO: Guardamos el tiempo de ejecuccion de la conexio (1000ms = 1s)
        print(cFormatter(f"Base de datos inicializada en {self.DbWakeTime} ms", color=Fore.GREEN))
        return self.conn

    def ExecuteRequest(self, _sql_request: str):
        """
        Ejecuta una sentencia SQL
        """
        try:
            self.conn.execute(_sql_request)
            self.conn.commit()  #* Commit para guardar cambios en la base de datos
        except Exception as error:
            return error("Error al ejecutar la sentencia SQL, seguramente debido a que no es un formato valido (docstring) o no existe la tabla")
            
    def CreateTable(self, table: str, columns: list):
        """
        Crea una tabla en la base de datos
        """

        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")

    def CloseConnection(self):
        """
        Cierra la conexion con la base de datos
        """
        try:
            if self.conn.total_changes >= 1 and not self.conn.commit(): 
                print(cFormatter("Se han realizado cambios en la base de datos y no se ha realizado un commit. Seguro que desea cerrar la conexion?", color= Fore.YELLOW))
            else:
                self.conn.close()
                self.DbRunTime = t.time() - self.DbRunTime
                print(cFormatter(f"Base de datos cerrada en {round(self.DbRunTime*1000, 2)} ms correctamente", color=Fore.GREEN))
        except Exception as error:
            print(cFormatter("No se ha iniciado una conexion con la base de datos", color=Fore.RED))




if __name__ == "__main__":

    pyver = python_version()
    sysname = os.name

    if sysname.upper() != "NT":
        print(cFormatter("Este programa esta probado en dispositivos Windows. Puede experimentar problemas si ejecuta el programa en otro sistema operativo", color= Fore.YELLOW))
        exit()
    if pyver < "3.10.2":
        print(cFormatter(f"Esta aplicacion requiere Python 3.10.2 o superior. {cFormatter(f'Version actual: {pyver}', color= Fore.MAGENTA)}", color=Fore.RED))
        exit()

    #TODO: <--------- TESTING ---------->

    u = User("Alvaro", "Byalvaro54", "alvarodrumer54@gmail.com")
    Database.CreateToken(u)
    db = Database(u)
    print(db.is_operative)
    print(db.runtime)
