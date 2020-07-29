#! /bin/python3
import os
import pathlib
from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets
import Gui
import Model
import sys
from database_manager import Account
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__();
        self.layout = QtWidgets.QVBoxLayout();
        self.a = Account(1,'admin',[],0,0);
        self.b = Account(2,'admin2',[],2,1);
        game = Model.SOS(5);
        game.gameEnded.connect(self.display_end_message);
        v2 = Gui.SosGridView(game);
        self.layout.addWidget(Gui.SosHeader(game,self.a,self.b));
        self.layout.addWidget(v2);
        self.setLayout(self.layout);
    def display_end_message(self,result):
        msg_box = QtWidgets.QMessageBox();
        if result == -1 :
            msg_box.setText("%s has won!!" % (self.a.username));
        elif result == 0:
            msg_box.setText("the game ended in a draw");
        else :
            msg_box.setText("%s has won!!" % (self.b.username));

        msg_box.exec();
            
if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.absolute());
    app = QApplication();
    v = MainWindow();
    v.show()
    sys.exit(app.exec_());
