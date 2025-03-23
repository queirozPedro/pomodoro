import sqlite3
class Connection:

    #Inicializa a conexão com o banco de dados
    def __init__(self, banco="pomodoro.db"):
        self.banco = banco
        self.conn = None         
        self.cursor = None       
        self.conectar()

    def conectar(self):
        #Conecta ao bd
        self.conn = sqlite3.connect(self.banco)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pomodoro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data,
            tempo_estudo INTEGER,
            tempo_pausa INTEGER
        )
        """)

    def salvar_pomodoro(self, tempo_estudo, tempo_pausa):
       
        from datetime import datetime

        data_atual = datetime.now().strftime("%d-%m-%y %H:%M:%S")

        self.cursor.execute("""
        INSERT INTO pomodoro (data, tempo_estudo, tempo_pausa)
        VALUES (?, ?, ?)
        """, (data_atual, tempo_estudo, tempo_pausa))
        self.conn.commit()
        

    #Fecha a conexão do bd
    def fechar(self):
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.fechar()
