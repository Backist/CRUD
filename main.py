import DbComms as D
from checker import Checker

u = D.User("Alvao", "Alvaromon1", "asd")
e = u.encryptPassword()
print(e)
