import sqlite3

class DBConnection:
    _instance = None  
    _connection = None  

    def __init__(self, db_path="pomodoro.db"):
        if DBConnection._connection is None:
            try:
                self.db_path = db_path
                self.connection = sqlite3.connect(self.db_path)
                DBConnection._connection = self.connection
            except sqlite3.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")


    @staticmethod
    def get_instance(db_path="pomodoro.db"):
        if DBConnection._instance is None:
            DBConnection._instance = DBConnection(db_path)
        return DBConnection._instance


    def get_connection(self):
        return self._connection


    def close_connection(self):
        try:
            if self._connection:
                self._connection.close()
        except sqlite3.Error as e:
            print(f"Erro ao fechar a conexão: {e}")
