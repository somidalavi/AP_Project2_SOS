from PySide2.QtWidgets import QGraphicsScene,QGraphicsView ,\
                                QGraphicsSimpleTextItem,QWidget,QLabel,QDialog
from PySide2 import QtWidgets
from PySide2.QtCore import Qt ,Slot,QRectF
from PySide2.QtGui import QFont,QWindow
csize = 50; # size of each cell
col_offset = 20; #used as an offset to centre grid text
row_offset = 5
font_size = 20;
cell_font =  QFont()
cell_font.setPointSize(font_size);

class SosPlayerHeader(QWidget):
    def __init__(self,account,score_signal):
        super().__init__();
        layout = QtWidgets.QVBoxLayout();
        self.username_lb = QLabel(account.username);
        self.score_lb = QLabel('Score : %2d'% (0,));
        self.games_lb = QLabel("Games : %2d"% (account.games, ));
        self.wins_lb  = QLabel("Wins  : %2d"% (account.wins,));
        score_signal.connect(self.score_changed);
        layout.addWidget(self.username_lb);
        layout.addWidget(self.score_lb)
        layout.addWidget(self.games_lb);
        layout.addWidget(self.wins_lb);
        self.setLayout(layout);
    def score_changed(self,score):
        self.score_lb.setText("Score: %2d" %(score));

class SosHeader(QWidget):
    def __init__(self,sos_game,account1,account2):
        super().__init__();
        layout = QtWidgets.QHBoxLayout();
        self.accounts = [account1,account2];
        layout.addWidget(SosPlayerHeader(account1,sos_game.p1scoreUpdated));
        layout.addWidget(SosPlayerHeader(account2,sos_game.p2scoreUpdated));
        self.turn_lb = QLabel("%s's turn" % (account1.username));
        sos_game.turnChanged.connect(self.change_turn)
        layout.addWidget(self.turn_lb);
        self.setLayout(layout);
    def change_turn(self,turn):
        self.turn_lb.setText("%s's turn" %(self.accounts[turn].username))

class SosGridCell(QGraphicsSimpleTextItem):
    def __init__(self,sos_game,row,col):
        super().__init__("-");
        self.row = row
        self.col = col;
        self.game = sos_game
    def mousePressEvent(self,e):
        super(SosGridCell,self).mousePressEvent(e);
        button = e.button();
        if button == Qt.LeftButton : letter = 's';
        elif button == Qt.RightButton : letter = 'o';
        else : return ;
        self.game.move(self.row,self.col,letter);

class SosGrid(QGraphicsScene):
    def __init__(self,sos_game):
        self.game = sos_game;
        self.n = sos_game.size
        n = self.n;
        super().__init__(0,0,csize*n,csize*n);
        self.vlines = [self.addLine(0,i * csize,n * csize,i * csize) for i in range(n + 1)];
        self.hlines = [self.addLine(j * csize,0,j * csize,n * csize) for j in range(n + 1)]
        self.cells = [];
        for i in range(n):
            ls = [];
            for j in range(n):
                textItem = SosGridCell(sos_game,i,j);
                textItem.setPos(j * csize + col_offset,i * csize -row_offset)
                textItem.setFont(cell_font);
                self.addItem(textItem)
                ls.append(textItem);
            self.cells.append(ls);
        sos_game.letterPlaced.connect(self.change_letter);
    @Slot(int,int,str)
    def change_letter(self,row,col,letter):
        self.cells[row][col].setText(letter);

class SosGridView(QGraphicsView):
    def __init__(self,sos_game):
        self.grid = SosGrid(sos_game);
        super().__init__(self.grid);
        self.n = sos_game.size
    def resizeEvent(self,e):
        super(SosGridView,self).resizeEvent(e);
        self.fitInView(0,0,csize * self.n,csize * self.n);

class SOSWindow(QWidget):
    def __init__(self,parent,n,account1,account2,model):
        super(SOSWindow,self).__init__(parent);
        self.setWindowFlags(Qt.Window);
        layout = QtWidgets.QVBoxLayout();
        self.game = model.new_game(n);
        self.a = account1
        self.b = account2
        layout.addWidget(SosHeader(self.game,account1,account2));
        layout.addWidget(SosGridView(self.game));
        self.setLayout(layout)
        self.game.gameEnded.connect(self.game_ended);
    def game_ended(self,result):
        msg_box = QtWidgets.QMessageBox();
        if result == -1 :
            msg_box.setText("%s has won!!" % (self.a.username));
        elif result == 0:
            msg_box.setText("the game ended in a draw");
        else :
            msg_box.setText("%s has won!!" % (self.b.username));
        #self.test_add();
        msg_box.exec();
        self.close()
    def closeEvent(self,e):
        self.deleteLater()
from PySide2.QtWidgets import QComboBox,QSpinBox,QPushButton,QFormLayout
class SOSDialog(QDialog):
    def __init__(self,model):
        super(SOSDialog,self).__init__();
        self.setWindowTitle("login");
        self.model = model;
        self.combo_box = QComboBox()
        self.combo_box.setModel(self.model.accounts_model);
        self.n_input = QSpinBox();
        self.new_game_button = QPushButton("New Game");
        self.new_game_button.clicked.connect(self.new_game);
        layout = QFormLayout();
        layout.addRow('Second Player:',self.combo_box);
        layout.addRow("Grid size :",self.n_input);
        layout.addWidget(self.new_game_button);
        self.setLayout(layout);
    def new_game(self):
        self.username = self.combo_box.currentText();
        self.n = self.n_input.value();
        if self.n >= 1 and self.n <= 25:
            self.accept();

