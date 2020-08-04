#! /bin/python3
import os
import pathlib
from PySide2.QtWidgets import QApplication,QLabel
from PySide2 import QtWidgets
import SOS_gui as Gui
import Model
import sys
import Login_gui
from database_manager import Account,AccountManager
from AccountEdit_gui import AccountManagerWidget,EditAccountDialog;
from SOS_gui import SOSWindow,SOSDialog
from Helper import add_button, add_label,show_message
import random
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self,model):
        super().__init__();
        self.model = model
        self.layout = QtWidgets.QVBoxLayout();
        cur_ac = model.get_login()
        self.a_username =  add_label(self.layout,'username: ' + cur_ac.username);
        self.a_f_name = add_label(self.layout,'first name: ' + cur_ac.f_name);
        self.a_l_name = add_label(self.layout,'last name: ' + cur_ac.l_name);
        self.a_games  = add_label(self.layout,'games: ' + str(cur_ac.games))
        self.a_wins   = add_label(self.layout,'wins: ' + str(cur_ac.wins));
        
        add_button(self.layout,'Login',self.change_account);
        add_button(self.layout,'Edit',self.edit);
        add_button(self.layout,'Open Account Manager',lambda : self.v.show()); 
        add_button(self.layout,'New game',self.new_game)

        self.v =AccountManagerWidget(self,self.model);
        self.setLayout(self.layout);
        self.game = None;
    def edit(self):
        ac = self.model.get_login()
        v = EditAccountDialog(self,ac,self.model,ac.username)
        if not v.exec_(): show_message("failed to edit")
        else: self.account_changed()
    def change_account(self):
        v = Login_gui.LoginWindow(self.model)
        res = v.exec_()

    def account_changed(self):
        cur_ac = self.model.get_login()
        self.a_username.setText('username: '+ cur_ac.username);
        self.a_f_name.setText('first name: ' + cur_ac.f_name);
        self.a_l_name.setText('last name: ' + cur_ac.l_name);
        self.a_games.setText('games: ' + str(cur_ac.games))
        self.a_wins.setText('wins: ' + str(cur_ac.wins));
    def end_game(self,obj):
        self.game = None;
        self.account_changed()
    def new_game(self):
        if self.game != None : return ;
        account1 = self.model.get_login();
        di = SOSDialog(self.model);
        res = di.exec_();
        if not res:  return ;
        account2_user = di.username
        n = di.n;
        if account1.username == account2_user : 
            show_message("can't start a game with yourself")
            return ;
        account2 = self.model.accounts_model.usernames[account2_user];
        if random.randint(0,1) == 1:account1,account2 = account2,account1
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
    if not model.get_login(): sys.exit()
    if not res:
        di = EditAccountDialog(None,model.get_login(),model,'admin');
        res = di.exec_()
        if not res: sys.exit()
    v = MainWindow(model);
    v.show()
    sys.exit(app.exec_());
