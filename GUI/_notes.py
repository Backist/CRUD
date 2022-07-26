
#* <----------    Set the window to be in the center of the screen and hide the main window    ---------->
# Screen.setWindowFlags(QtCore.Qt.FramelessWindowHint)
# Screen.setAttribute(QtCore.Qt.WA_TranslucentBackground)
# Screen.setWindowTitle("Master Panel")

#* <----------    Make sure that when we run the file, the below code will be executed (not in imports)    ---------->
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     SplashScreen = QtWidgets.QMainWindow()    # Less ms response making a MainWindow
#     ui = SplashScreenUI()
#     ui.setupUi(SplashScreen)
#     SplashScreen.show()
#     sys.exit(app.exec_())  
