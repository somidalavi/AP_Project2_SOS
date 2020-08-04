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
from AccountEdit_gui import AccountManagerWidget,EditAccountDialog,show_message;
from SOS_gui import SOSWindow,SOSDialog
import random
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self,model):
        super().__init__();
        self.model = model
        self.layout = QtWidgets.QVBoxLayout();
        self.game_button = QtWidgets.QPushButton('New game')
        self.game_button.clicked.connect(self.new_game);
        self.accounts_button = QtWidgets.QPushButton('Open Account Manager');
        self.accounts_button.clicked.connect(self.account_manager);
        self.layout.addWidget(self.accounts_button);
        self.layout.addWidget(self.game_button);
        self.v =AccountManagerWidget(self,self.model);
        self.setLayout(self.layout);
        self.game = None;
    def account_manager(self):
        self.v.show()
        print('account manager');
    def end_game(self,obj):
        print("HEre")
        self.game = None;
    def new_game(self):
        if self.game != None : return ;
        account1 = self.model.get_login();
        di = SOSDialog(self.model);
        res = di.exec_();
        if not res:  return ;
        account2_user = di.username
        n = di.n;
        del di;
        if account1.username == account2_user : 
            show_message("can't start a game with yourself")
            return ;
        account2 = self.model.accounts_model.usernames[account2_user];
        self.game = SOSWindow(self,n,account1,account2,self.model);
        self.game.destroyed.connect(self.end_game);
        self.game.show()

if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.absolute());
    app = QApplication();
    model = Model.Model(); 
    v = Login_gui.LoginWindow(model);
    res = v.exec_()
    del v
    #if we didn't succed in signing and haven't signed as admin then exit
    if not model.get_login(): sys.exit()
    if not res:
        di = EditAccountDialog(None,model.get_login(),model,'admin');
        res = di.exec_()
        if not res: sys.exit()
    #v = AccountManagerWidget(model);
    #v.show()
    #db = AccountManager('lib.db');
    #tb = Model.AccountsModel(db);
    v = MainWindow(model);
    v.show()
    #b = MainWindow(tb);
    #b.show()
    sys.exit(app.exec_());
