from GUIBuilder import MainWindow
import DbBuilder as D

...
u = D.User("Alvaro", "ByAlvaro54", "alvarodrumer54@gmail.com")
u2 = D.User("Jorge", "#megustaelqueso", "jorgehola@gmail.com")
D.Database.CreateToken(u)
d = D.Database(u)
