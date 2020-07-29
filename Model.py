from database_manager import Account , AccountManager
from PySide2.QtCore import QObject , Signal
from PySide2 import QtCore
class SOS(QObject):
    
    scoresUpdated = Signal(int,int);
    letterPlaced  = Signal(int,int,str);
    turnChanged   = Signal(int);
    ps_triple = [
        (-1,-1, 1, 1),
        (-1, 0, 1, 0),
        ( 0,-1, 0, 1),
        ( 1,-1,-1, 1),
        ( 0, 0,-1,-1),
        ( 0, 0, 0,-1),
        ( 0, 0, 1,-1),
        ( 0, 0, 1, 0),
        ( 0, 0, 1, 1),
        ( 0, 0, 0, 1),
        ( 0, 0,-1, 1),
        ( 0, 0,-1, 0),
    ]
    letters = ['s','o','s']
    def __init__(self,n):
        self.board = [['0' for j in range(n)] for i in range(n)];
        self.p1_score = 0;
        self.p2_score = 0;
        self.turn = 0 ; #1 for turn of player 2 0 if it's second player's turn
        self.size = len(board);
    def move(self,row,col,letter):
        if not self.is_valid_pos(row,col):
            raise Exception('not a valid position');
        if self.board[row][col] != '0':
            raise Exception('that position is already full');
        self.board[row][col] = letter;
        self.letterPlaced.emit(row,col,letter);
        num_scored = 0
        for triple in self.ps_triple:
            st_r = row + triple[0];
            st_c = col + triple[1];
            dr = triple[2];
            dc = triple[3];
            flag = True;
            for i in range(3):
                if not self.is_valid_pos(st_r,st_c):
                    flag = False;
                    break;
                if letters[i] != self.board[st_r][st_c]:
                    flag = False;
                    break;
                st_r += dr;
                st_c += dc;
            if flag: num_scored += 1;
        if num_scored == 0:
            self.turn += 1;
            self.turnChanged.emit(self.turn);
            return ;
        if self.turn == 0:
            self.p1_score += num_scored
            self.scoresUpdated.emit(0,self.p1_scored);
        else :
            self.p2_score += num_scored
            self.scoresUpdated.emit(1,self.p2_scored);
    def is_valid_pos(self,row,col):
        return (row >= 0 and row < self.size) and (col >= 0 and col < self.size);

class Model:
    def __init__(self):
        self.db = AccountMananger('lib.db');
        self.accounts = self.db.get_all_accounts();
        self.username_dict = { acc.username : acc for acc in self.accounts}
        self.logged_account = None;

    def login(self,username,password):
        #this assumes that the username is at least correct (as in it exists)
        account = self.username_dict[username];
        if account.check_password(password):
            self.logged_account = account; 
            if account.username = 'admin' and password == '123456':
                return False;
        else : raise ValueError("wrong password")
        return True;

    def new_game(self,n):
        return SOS(n);
        

