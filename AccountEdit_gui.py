from PySide2.QtWidgets import QWidget,QLabel,QTableView,QAction,QMenu,QDialog
from PySide2 import QtWidgets
from PySide2 import QtGui
from Helper import show_message,add_label,add_button
from PySide2.QtCore import Qt
class AddAccountDialog(QDialog):
    def __init__(self,parent,model):
        super(AddAccountDialog,self).__init__(parent);
        self.model = model;
        self.username_inp = QtWidgets.QLineEdit();
        self.password_inp = QtWidgets.QLineEdit();
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow('username',self.username_inp)
        self.layout.addRow('password',self.password_inp);
        self.l_name_inp = QtWidgets.QLineEdit();
        self.f_name_inp = QtWidgets.QLineEdit();
        self.layout.addRow('first name:',self.f_name_inp)
        self.layout.addRow('last name:',self.l_name_inp);
        self.add_button = add_button(self.layout,"add",self.add_account)
        self.setLayout(self.layout)
    def add_account(self):
        username = self.username_inp.text()
        password = self.password_inp.text()
        f_name = self.f_name_inp.text()
        l_name = self.l_name_inp.text();
        if self.model.accounts_model.addAccount(username,f_name,l_name,password):
            self.accept()
        else : self.reject()

class EditAccountDialog(AddAccountDialog):
    def __init__(self,parent,account,model,username):
        super(EditAccountDialog,self).__init__(parent,model);
        self.username = username
        self.layout.removeRow(4);
        self.layout.removeRow(0);
        del self.username_inp;
        del self.add_button;
        self.l_name_inp.setText(account.l_name);
        self.f_name_inp.setText(account.f_name);
        add_button(self.layout,'Edit',self.edit_account)
    def edit_account(self):
        password = self.password_inp.text()
        f_name = self.f_name_inp.text()
        l_name = self.l_name_inp.text()
        print(password,f_name,l_name)
        if self.model.accounts_model.editAccount(self.username,f_name,l_name,password):
            print('acception')
            self.accept();
        else : self.reject()


class AccountManagerWidget(QtWidgets.QTableView):
    def __init__(self,parent,model):
        super(AccountManagerWidget,self).__init__(parent);
        print(dir(Qt.WindowFlags))
        self.setWindowFlags(Qt.Window)
        self.setModel(model.accounts_model);
        self.menu = QMenu(self);
        self.model = model
        #alot of lines jst for a menu but which is bad
        self.edit_action=   QtWidgets.QAction('edit',self);
        self.add_action =   QAction('add an account',self);
        self.remove_action= QAction('delete',self);
        self.remove_action.triggered.connect(self.delete_row);
        self.add_action.triggered.connect(self.add_account);
        self.edit_action.triggered.connect(self.edit_account);
        self.menu.addAction(self.edit_action);
        self.menu.addAction(self.add_action);
        self.menu.addAction(self.remove_action);
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows);
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    def contextMenuEvent(self,e):
        if not self.model.is_admin(): return 
        self.menu.popup(QtGui.QCursor.pos());
    def delete_row(self):
        rows = self.selectionModel().currentIndex().row()
        print("row is",rows)
        self.model.accounts_model.removeRows(rows,1);
    def add_account(self):
        di = AddAccountDialog(self,self.model)
        res = di.exec_();
        if  res : return 
        show_message("couldn't add the account")
    def edit_account(self):
        #this is bad stuff
        row = self.selectionModel().currentIndex().row()
        account = self.model.accounts_model.accounts[row];
        di = EditAccountDialog(self,account,self.model,account.username)
        ok = di.exec_()
        if ok : return


        
