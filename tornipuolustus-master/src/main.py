import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main_window import MainWindow

def main():
    # every Qt application must have one instance of QApplication
    global app # use global to prevent crash on exit
    app = QtWidgets.QApplication(sys.argv)
    # create the main window and main menu
    mainWindow = MainWindow()  
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()