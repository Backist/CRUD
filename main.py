import sys
from PyQt5 import QtCore
# from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *


from GUI.SplashScreen.splashUIModel2 import SplashScreenUI
from GUI.Login.LoginUI import LoginUI
# from GUI.Register.RegisterUI import RegisterUI
# from GUI.MainWindow.mainWindow import MainWindow


## ==> GLOBALS
counter = 0

# ==> MAIN APP
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = LoginUI()
        self.ui.setupUi(self)


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = SplashScreenUI()
        self.ui.setupUi(self)

        #* REMOVE Master Window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        #* timer in MILISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY DATABASE")

        # Change Texts
        QtCore.QTimer.singleShot(1000, lambda: self.ui.label_description.setText("<strong>SEARCHING FOR</strong> UPDATES"))
        QtCore.QTimer.singleShot(2000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(2700, lambda: self.ui.label_description.setText("<strong>INITIALIZING</strong> CONFIGURATION"))
        QtCore.QTimer.singleShot(3300, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter

        #* pass Counter to Progress Bar
        self.ui.progressBar.setValue(counter)

        #* Close SlapshScreen and open APP
        if counter >= 100:
            self.timer.stop()
            #* SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()
            #* Close SplashScreen
            self.close()
        else:
            #* INCREASE COUNTER
            counter += 1
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
