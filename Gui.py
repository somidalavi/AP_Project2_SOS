from PySide2.QtWidgets import QGraphicsScene,QGraphicsView
class SosGrid(QGraphicsScene):
    def __init__(self,n):
        super().__init__(0,0,30*n,30*n);
        self.vlines = [self.addLine(0,i * 30,n * 30,i * 30) for i in range(n + 1)];
        self.hlines = [self.addLine(j * 30,0,j * 30,n * 30) for j in range(n + 1)]
        print(self.vlines[1].line());

class SosGridView(QGraphicsView):
    def __init__(self,n):
        self.grid = SosGrid(n);
        super().__init__(self.grid);
        self.n = n
    def resizeEvent(self,e):
        super(SosGridView,self).resizeEvent(e);
        self.fitInView(0,0,30 * self.n,30 * self.n);

