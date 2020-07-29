from PySide2.QtWidgets import QGraphicsScene,QGraphicsView ,\
                                QGraphicsSimpleTextItem,QWidget,QLabel
from PySide2 import QtWidgets
from PySide2.QtCore import Qt ,Slot,QRectF
from PySide2.QtGui import QFont
csize = 50; # size of each cell
col_offset = 20; #used as an offset to centre grid text
row_offset = 5
font_size = 20;
cell_font =  QFont()
cell_font.setPointSize(font_size);
class SosPlayerHeader(QWidget):
    def __init__(self,account,score_signal):
        super().__init__();
        self.account = account;
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
        layout.addWidget(SosPlayerHeader(account1,sos_game.p1scoreUpdated));
        layout.addWidget(SosPlayerHeader(account2,sos_game.p2scoreUpdated));
        self.setLayout(layout);

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

