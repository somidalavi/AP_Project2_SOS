from PySide2.QtWidgets import QWidget,QComboBox,QFormLayout,\
                                QPushButton, QLineEdit,QDialog

from AccountEdit_gui import AddAccountDialog
from Helper import add_button
class LoginWindow(QDialog):
    def __init__(self,model):
        super(LoginWindow,self).__init__();
        self.setWindowTitle("login");
        self.model = model;
        self.combo_box = QComboBox()
        self.combo_box.setModel(self.model.accounts_model);
        self.password_input = QLineEdit();
        layout = QFormLayout();
        layout.addRow('username:',self.combo_box);
        layout.addRow("password:",self.password_input);
        add_button(layout,"Login",self.login)
        add_button(layout,"Register",self.register)
        self.setLayout(layout);
    def register(self):
        v = AddAccountDialog(self,self.model);
        res = v.exec_()
        if res : 
            self.model.login(v.username_inp.text(),v.password_inp.text())
            self.accept();
    def login(self):
        username = self.combo_box.currentText();
        password = self.password_input.text();
        try:
            ok = self.model.login(username,password);
            if ok: self.accept();
            else : self.reject();
        except:
            self.setWindowTitle("password Incorrect!!");
            

