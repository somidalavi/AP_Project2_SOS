#! /bin/python3
import os
import pathlib
from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets
import SOS_gui as Gui
import Model
import sys
import Login_gui
from database_manager import Account,AccountManager
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self,tb):
        super().__init__();
        self.layout = QtWidgets.QVBoxLayout();
        self.a = Account(1,'admin',[],0,0);
        self.b = Account(2,'admin2',[],2,1);
        game = Model.SOS(5);
        game.gameEnded.connect(self.display_end_message);
        v2 = Gui.SosGridView(game);
        self.tableModel = tb
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.tableModel);
        self.tableModel.addAccount("efds",'fsd');
        self.tableModel.addAccount('fdshgfhf','gdsgds');
        self.layout.addWidget(self.table)
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
        self.test_add();
        msg_box.exec();
        print("Hello")
        self.close()
    def test_add(self):
        self.tableModel.removeRows(2,1,None);
if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.absolute());
    app = QApplication();
    model = Model.Model(); 
    v = Login_gui.LoginWindow(model);
    res = v.exec_()
    del v
    print(res)
    db = AccountManager('lib.db');
    tb = Model.AccountsModel(db);
    v = MainWindow(tb);
    v.show()
    #b = MainWindow(tb);
    #b.show()
    sys.exit(app.exec_());
