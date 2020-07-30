from PySide2.QtWidgets import QWidget,QComboBox,QFormLayout,\
                                QPushButton, QLineEdit,QDialog



class LoginWindow(QDialog):
    def __init__(self,model):
        super(LoginWindow,self).__init__();
        self.setWindowTitle("login");
        self.model = model;
        self.combo_box = QComboBox()
        self.combo_box.setModel(self.model.accounts_model);
        self.password_input = QLineEdit();
        self.login_button = QPushButton("login");
        self.login_button.clicked.connect(self.login);
        layout = QFormLayout();
        layout.addRow('username:',self.combo_box);
        layout.addRow("password:",self.password_input);
        layout.addRow('',self.login_button);
        self.setLayout(layout);
    def login(self):
        username = self.combo_box.currentText();
        password = self.password_input.text();
        try:
            ok = self.model.login(username,password);
            if ok: self.accept();
            else : self.reject();
        except:
            self.setWindowTitle("password Incorrect!!");
            

