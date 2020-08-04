import sqlite3
import os
import pathlib
import bcrypt
class Account:
    data_len = 5
    data_field_names = ['username','first name','last name','games','wins']
    def __init__(self,database_id,username,f_name,l_name,pass_hash,games,wins): 
        self.database_id = database_id
        self.f_name = f_name;
        self.l_name = l_name;
        self.username = username;
        self.pass_hash = pass_hash;
        self.games = games
        self.wins = wins;
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.pass_hash)

class AccountManager():
    database_schema = '''
    CREATE TABLE accounts (
        account_id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        f_name   TEXT NOT NULL,
        l_name   TEXT NOT NULL,
        password_hash BLOB NOT NULL,
        num_games INTERGER NOT NULL,
        num_wins  INTERGER NOT NULL
    );
    '''
    def __init__(self,database_path):
        exists = os.path.isfile(database_path)
        self.con = sqlite3.connect(database_path)
        if exists : return 
        self.con.execute(AccountManager.database_schema);
        self.con.commit()
    def remove_account(self,account):
        self.con.execute('''DELETE FROM accounts
                         WHERE account_id = ?;''',(account.database_id,));
        self.con.commit();
    def get_account(self,username):
        cursor  = self.con.execute('''
                 SELECT account_id,username,f_name,l_name,password_hash,num_games,num_wins
                 FROM accounts
                 WHERE username = ?;
                 ''',(username,));
        rows = cursor.fetchall()
        if len(rows) != 1:
            raise Exception("Database Error Occured");
        row = list(rows[0])
        return Account(*row);
    #updates only the number of games and wins
    #you should use other functions to change the password
    def update_account(self,account):
        self.con.execute('''
                UPDATE accounts
                SET num_games = ?,
                    num_wins  = ?,
                    f_name = ?,
                    l_name = ?
                WHERE account_id = ?;
                         ''',(account.games,account.wins,account.f_name,account.l_name,account.database_id));
        self.con.commit();
    #this assumes that the operation is permitted
    #it also updates the pass_hash of the account object itself
    def update_password(self,account,new_pass):    
        print(new_pass);
        new_hash = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt( 12 ));
        account.pass_hash = new_hash;
        self.con.execute('''
            UPDATE accounts
            SET password_hash = ?
            WHERE account_id = ?;
        ''',(new_hash,account.database_id));
        self.con.commit();
    #this function assumes that another account with the same username doesn't already
    #exist
    def add_account(self,username,f_name,l_name,password):
        pass_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(12));
        self.con.execute('''
                INSERT INTO accounts values
                (NULL,?,?,?,?,0,0);
                ''',(username,f_name,l_name,pass_hash))
        self.con.commit();
        return self.get_account(username);
    def get_all_accounts(self):
        #this should change from * to explicitly stating all values
        cursor = self.con.execute('''
                select * from accounts;
                ''');
        ls = [Account(row[0],row[1],row[2],row[3],row[4],row[5],row[6]) for row in cursor];
        return ls
