"""Main program"""

import sys
from colorama import Fore
from PyQt5 import QtCore
# from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from errors import *
from GUI.SplashScreen.splashUIModel2 import SplashScreenUI
from GUI.Login.LoginUI import LoginUI
from db import Database
from utils import cFormatter

# from GUI.Register.RegisterUI import RegisterUI
# from GUI.MainWindow.mainWindow import MainWindow


#TODO: Globals
counter = 0


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
        self.ui.loginButton.clicked.connect(self.checkCredents)
        self.ui.exitButton.clicked.connect(self.CloseUI)

    def checkCredents(self):
        self.username = self.ui.usernameLabel.text()
        self.password = self.ui.passwordLabel.text()
        self.conn = Database()
        if not self.conn.checkUser(self.username, self.password):
            raise DatabaseCredentialsError("Invalid username or password")
        else:
            print(cFormatter(f"Login Successful by {self.username}", color= Fore.RED))

    def CloseUI(self):
        self.destroy()
        sys.exit()  

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = SplashScreenUI()
        self.ui.setupUi(self)

        #* <----------  Hide the main window    ---------->
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("Master Panel")

        #* Drop Shadow Effect
        self.ui.dropShadowFrame.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius= 20, 
            xOffset=0, 
            yOffset=0, 
            color= QColor(0,0,0,60)
            )
        )
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        #* timer in MILISECONDS
        self.timer.start(35)

        #* Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY DATABASE")

        #* Change Splash Descriptions
        QtCore.QTimer.singleShot(1000, lambda: self.ui.label_description.setText("<strong>SEARCHING FOR</strong> UPDATES"))
        QtCore.QTimer.singleShot(2000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(2700, lambda: self.ui.label_description.setText("<strong>INITIALIZING</strong> CONFIGURATION"))
        QtCore.QTimer.singleShot(3300, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

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
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
