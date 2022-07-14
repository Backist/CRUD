import sys

from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QComboBox, QDialog, QMenuBar)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        pass

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())