from database_manager import Account , AccountManager
from PySide2.QtCore import QObject , Signal
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QAbstractTableModel,QModelIndex
class SOS(QObject):
    
    p1scoreUpdated = Signal(int);
    p2scoreUpdated = Signal(int);
    letterPlaced  = Signal(int,int,str);
    turnChanged   = Signal(int);
    gameEnded =  Signal(int); #-1 player 1 wins 0 is a draw and 1 player 2 has won
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
        super().__init__()
        self.board = [['0' for j in range(n)] for i in range(n)];
        self.p1_score = 0;
        self.p2_score = 0;
        self.moves = 0;
        self.turn = 0 ; #1 for turn of player 2 0 if it's second player's turn
        self.size = len(self.board);

    def move(self,row,col,letter):
        if not self.is_valid_pos(row,col):
            raise Exception('not a valid position');
        if self.board[row][col] != '0':
            return False;
        self.board[row][col] = letter;
        print("placed %s at %d ,%d" %(letter,row,col))
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
                if self.letters[i] != self.board[st_r][st_c]:
                    flag = False;
                    break;
                st_r += dr;
                st_c += dc;
            if flag: num_scored += 1;
        
        self.moves += 1; 
        
        if num_scored == 0:
            self.turn ^= 1;
            self.turnChanged.emit(self.turn);  
        elif self.turn == 0:
            self.p1_score += num_scored
            self.p1scoreUpdated.emit(self.p1_score);
        else :
            self.p2_score += num_scored
            self.p2scoreUpdated.emit(self.p2_score);
        
        if self.moves == self.size * self.size:
            if self.p2_score == self.p1_score : self.gameEnded.emit(0);
            elif self.p2_score > self.p1_score : self.gameEnded.emit(1);
            else : self.gameEnded.emit(-1);
    def is_valid_pos(self,row,col):
        return (row >= 0 and row < self.size) and (col >= 0 and col < self.size);
    
    def get_letter(self,row,col):
        if not self.is_valid_pos(row,col):
            raise ValueError('invalid row or column');
        return self.board[row][col];


class AccountsModel(QAbstractTableModel):
    def __init__(self,db_manager):
        super(AccountsModel,self).__init__();
        self.db_manager = db_manager;
        self.accounts = self.db_manager.get_all_accounts();
        self.usernames = {account.username : account for account in self.accounts};
    def addAccount(self,username,f_name,l_name,password):
        if (not self.check_input(username,f_name,l_name,password)) or username in self.usernames:
            return False;
        n_account = self.db_manager.add_account(username,f_name,l_name,password);
        self.usernames[username] = n_account;
        self.accounts.append(n_account);
        self.insertRows(len(self.accounts),1);
        return True;
    def check_input(self,username,f_name,l_name,password):
        if f_name == '' or l_name =='' or password == '':
            return False
        return True;

    def editAccount(self,username,f_name,l_name,password):
        if (not self.check_input(username,f_name,l_name,"PlaceHoldervalue")) :
            return False;
        account = self.usernames[username];
        if password != '':
            self.db_manager.update_password(account,password)
        account.f_name = f_name;
        account.l_name = l_name;
        self.db_manager.update_account(account);

        self.emitChange(self.accounts.index(account))
        return True;

    def emitChange(self,row):
        topleft  = self.index(row,0)
        botright = self.index(row,Account.data_len - 1)
        self.dataChanged.emit(topleft,botright)

    def updateAccount(self,account):
        self.db_manager.update_account(account)
        self.emitChange(self.accounts.index(account))
    #should only be called internally
    def insertRows(self,row,count,parent=None):
        #for now we only support insert a single row to the end of the list
        self.beginInsertRows(QtCore.QModelIndex(),row,row);
        self.endInsertRows();
    
    def removeRows(self,row,count,parent=None):
        #again we only remove one row at a time
        #you also can't delte the first account which is the admin
        print(row)
        if row == 0  or row >= self.rowCount() or count != 1:
            return False;
        self.beginRemoveRows(QtCore.QModelIndex(),row,row);
        account = self.accounts[row];
        self.db_manager.remove_account(account);
        self.accounts.pop(row);
        self.endRemoveRows();
    
    def flags(self,index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return Account.data_field_names[section];
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def data(self,index,role):
        if role == Qt.DisplayRole:
            col = index.column();
            account = self.accounts[index.row()];
            if col == 0: return account.username
            elif col == 1: return account.f_name;
            elif col == 2: return account.l_name;
            elif col == 3: return account.games
            elif col == 4: return account.wins;

    def rowCount(self,index = None):
        return len(self.accounts);
    
    def columnCount(self,index = None):
        return Account.data_len;
        
class Model(QObject):
    loginChanged = Signal();
    def __init__(self):
        super().__init__();
        self.db = AccountManager('lib.db');
        self.accounts_model = AccountsModel(self.db);
        self.logged_account = None;
    def login(self,username,password):
        #this assumes that the username is at least correct (as in it exists)
        account = self.accounts_model.usernames[username];
        print(account.username,account.pass_hash,account.check_password(password),password)
        if account.check_password(password):
            self.logged_account = account; 
            if account.username == 'admin' and password == '123456':
                return False;
            self.loginChanged.emit();
        else : raise ValueError("wrong password")
        return True;
    def new_game(self,n):
        return SOS(n);
    def get_login(self):
        return self.logged_account;
    def is_admin(self):
        return self.logged_account.username == 'admin';
        

