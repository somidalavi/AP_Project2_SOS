from PySide2.QtWidgets import QPushButton,QLabel
def add_button(layout,name,callback):
    but =QPushButton(name)
    layout.addWidget(but);
    but.clicked.connect(callback);
    return but;
def add_label(layout,text):
    l = QLabel(text)
    layout.addWidget(l);
    return l
def show_message(msg):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(msg);
    msg_box.exec()
