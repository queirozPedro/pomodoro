import sqlite3
from datetime import datetime

class Connection:
    #Inicializa a conexão com o banco de dados
    def __init__(self, db_name="pomodoro.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.conectar()

    #Conecta ao banco
    def conectar(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
       

    #Cria as tabelas pomodoro e cronometro no banco de dados
    def criar_tabelas(self):
        self.cursor.execute("""
         CREATE TABLE IF NOT EXISTS pomodoro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL
        )""")

        self.cursor.execute("""
         CREATE TABLE IF NOT EXISTS cronometro (
            id_pomodoro INTEGER PRIMARY KEY,
            tempo_estudo INTEGER NOT NULL,
            tempo_pausa INTEGER NOT NULL,
            quantidade_ciclos INTEGER NOT NULL,
            tempo_estudado INTEGER NOT NULL,
            FOREIGN KEY (id_pomodoro) REFERENCES pomodoro(id) ON DELETE CASCADE
        )""")
        
        self.conn.commit()
    
    #Insere dados no cronometro
    def salvar_cronometro(self, id_pomodoro, tempo_estudo, tempo_pausa, quantidade_ciclos, tempo_estudado):
        try:
            self.cursor.execute("""
            INSERT INTO cronometro (id_pomodoro, tempo_estudo, tempo_pausa, quantidade_ciclos, tempo_estudado)
            VALUES (?, ?, ?, ?, ?)
            """, (id_pomodoro, tempo_estudo, tempo_pausa, quantidade_ciclos, tempo_estudado))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao salvar cronômetro: {e}")
            return False

    #Salva um novo registro de Pomodoro
    def salvar_pomodoro(self, status):
        try:
            data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.cursor.execute("""
            INSERT INTO pomodoro (data_hora, status)
            VALUES (?, ?)
            """, (data_hora, status))
            self.conn.commit()
            return self.cursor.lastrowid  # Retorna o ID do pomodoro inserido
        except sqlite3.Error as e:
            print(f"Erro ao salvar pomodoro: {e}")
            return None
         
    #Fecha a conexão com o banco de dados
    def fechar(self):
        if self.conn:
            self.conn.close()