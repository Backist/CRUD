"""Main program"""


import sys
import typing

from os import system
from metadata import pyver, opsys

try:
    #import psutil
    # import keyboard
    from colorama import Fore

    from PyQt5.QtGui import (
        QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, 
        QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QKeyEvent
    )
    from PyQt5.QtCore import (QTimer, Qt, QCoreApplication, QPropertyAnimation, QPoint, QSize, QUrl,
        QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent
    )
    from PyQt5.QtWidgets import *

except ImportError:

    print("Problem Found: Please install all the dependencies")
    getDepens = input("Do you want to install all the dependencies? (y/n) ")
    if getDepens.lower() in ["y", "yes"]:
        if opsys.upper() == "WINDOWS":
            system("pip install colorama")
            system("pip install psutil")
            system("pip install PyQt5")
            system("pip install keyboard")
        else:
            system("pip3 install colorama")
            system("pip3 install psutil")
            system("pip3 install PyQt5")
            system("pip3 install keyboard")
    else:
        sys.exit("Make sure you have insatlled all the dependencies to run the program")

from errors import *
from utils import *
from GUI.SplashScreen.splashUI import SplashScreenUI
from GUI.Login.LoginUI import LoginUI
# from GUI.Register.RegisterUI import registerUI
# from GUI.MainWindow.MainWindowUI import mainWindowUI
from db import Database

#TODO: Globals and constants
counter = 0
CRUD_PATH = 'GUI\Icons\CRUDIcon.png'


# class RegisterWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.ui = RegisterUI()
#         self.ui.setupUi(self)
#         #self.createFuncs()
    # def createFuncs(self):
    #     self.ui.loginButton.clicked.connect(self.checkCredents)
    #     self.ui.closeButton.clicked.connect(self.CloseUI)


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.createFuncs()
    
    def createFuncs(self):
        self.ui.loginButton.setCheckable(True)
        self.ui.loginButton.toggled.connect(self.checkCredents)
        self.ui.loginButton.clicked.connect(self.checkCredents)
        self.ui.exitButton.clicked.connect(self.CloseUI)

    def checkCredents(self):
        self.username = self.ui.usernameLabel.text()
        self.password = self.ui.passwordLabel.text()

        if len(self.username) == 0 or len(self.password) == 0:
            self.msgbx = QMessageBox()
            self.msgbx.setModal(True)
            self.msgbx.about(self, "Error", "Please fill in all fields")
        else:
            self.conn = Database()
            if not self.conn.checkUser(self.username, self.password):
                raise DatabaseCredentialsError(cFormatter("Invalid username or password", color= Fore.RED))
            QMessageBox(
                "Login Successful",
                f"Welcome {self.username}",
                parent=self,
                flags=Qt.WindowStaysOnTopHint,
            )
            print(cFormatter(f"Login Successful by {self.username}", color= Fore.RED))
        return 

    def CloseUI(self):
        self.destroy()
        sys.exit()  

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = SplashScreenUI()
        self.ui.setupUi(self)

        #* <----------  Hide the main window    ---------->
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Master Panel")

        #* Drop Shadow Effect
        self.ui.dropShadowFrame.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius= 20, 
            xOffset=0, 
            yOffset=0, 
            color= QColor(0,0,0,60)
            )
        )
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        #* timer in MILISECONDS
        self.timer.start(35)

        #* Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY DATABASE")

        #* Change Splash Descriptions
        QTimer.singleShot(1000, lambda: self.ui.label_description.setText("<strong>SEARCHING FOR</strong> UPDATES"))
        QTimer.singleShot(2000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(2700, lambda: self.ui.label_description.setText("<strong>INITIALIZING</strong> CONFIGURATION"))
        QTimer.singleShot(3300, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        #* Show Main Window (which contains the widget)
        self.show()

    #* ==> APP FUNCTIONS
    def progress(self):
        global counter

        #* pass Counter to Progress Bar
        self.ui.progressBar.setValue(counter)

        #* Close SplashScreen and open APP
        if counter >= 100:
            self.timer.stop()
            #* Show Login Window
            self.login = LoginWindow()
            self.login.show()
            #* Close SplashScreen
            self.close()
        else:
            #* Increase counter
            counter += 1
 

if __name__ == "__main__":

    #TODO: <----------  Check OS Cofing and vers    ---------->

    if opsys is not None and opsys == "Windows" and pyver <= "3.10.2":
        print(cFormatter("Ejecuting on Windows. Your Python version must be greater than 3.10.2!", color= Fore.YELLOW))
        sys.exit(1)
    elif opsys is not None and opsys == "Linux" and pyver <= "3.10.2":
        print(cFormatter("Ejecuting on Linux. Your Python version must be greater than 3.10.2!", color= Fore.YELLOW))
        sys.exit(1)
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
