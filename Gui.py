from PySide2.QtWidgets import QGraphicsScene,QGraphicsView ,QGraphicsSimpleTextItem
from PySide2.QtCore import Qt ,Slot,QRectF
from PySide2.QtGui import QFont

csize = 50; # size of each cell
col_offset = 20; #used as an offset to centre grid text
row_offset = 5
font_size = 20;
cell_font =  QFont()
cell_font.setPointSize(font_size);
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

