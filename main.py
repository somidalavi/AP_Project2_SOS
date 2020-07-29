#! /bin/python3
import os
import pathlib
from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets
import Gui
import sys
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__();
        self.layout = QtWidgets.QVBoxLayout();
        v2 = Gui.SosGridView(10);
        self.layout.addWidget(v2);
        self.setLayout(self.layout);
if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.absolute());
    app = QApplication();
    v = MainWindow();
    v.show()
    sys.exit(app.exec_());
