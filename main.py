"""Main program"""

import sys
from colorama import Fore

from PyQt5.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, 
    QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient
)
from PyQt5.QtCore import (QTimer, Qt, QCoreApplication, QPropertyAnimation, QPoint, QSize, QUrl,
    QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent
)
from PyQt5.QtWidgets import *


from errors import *
from utils import *
from GUI.SplashScreen.splashUI import SplashScreenUI
from GUI.Login.LoginUI import LoginUI
# from GUI.Register.RegisterUI import registerUI
# from GUI.MainWindow.MainWindowUI import mainWindowUI
from db import Database

#TODO: Globals and constants
counter = 0
CRUD_ICON = 'GUI\Icons\CRUDIcon.png'


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

        if len(self.username) == 0 or len(self.password) == 0:
            QMessageBox.warning(self, "Error", "Please enter your username and password.")
            return
        else:
            self.conn = Database()
            if not self.conn.checkUser(self.username, self.password):
                raise DatabaseCredentialsError(cFormatter("Invalid username or password", color= Fore.RED))
            else:
                QMessageBox("Login Successful", "Welcome {}".format(self.username), parent= self, flags= Qt.WindowStaysOnTopHint)
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
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
