from GUIBuilder import MainWindow
from DbBuilder import *
from DbBuilder import Database

...

er = User("Alvaro", "Aasdfzzz", "asdlma@gmail.-com")
Database.CreateToken(er)
e = Database(er)
e.ClockThread
e._Clock()