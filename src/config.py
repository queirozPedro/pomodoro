import sqlite3
import traceback

class Config():
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()
        self.cursor = self.conn.cursor()
        self.tempo_estudo, self.tempo_pausa, self.quantidade_ciclos = self.obter_ultima_config()


    @property
    def tempo_estudo(self):
        return self._tempo_estudo


    @tempo_estudo.setter
    def tempo_estudo(self, valor):
        if valor < 1:
            valor = 1
        self._tempo_estudo = valor


    @property
    def tempo_pausa(self):
        return self._tempo_pausa


    @tempo_pausa.setter
    def tempo_pausa(self, valor):
        if valor < 1:
            valor = 1
        self._tempo_pausa = valor


    @property
    def quantidade_ciclos(self):
        return self._quantidade_ciclos


    @quantidade_ciclos.setter
    def quantidade_ciclos(self, valor):
        if valor < 1:
            valor = 1
        self._quantidade_ciclos = valor


    def obter_ultima_config(self):
        try:
            # Consulta para obter o último pomodoro e o cronômetro correspondente
            self.cursor.execute("""
                SELECT c.tempo_estudo, c.tempo_pausa, c.quantidade_ciclos
                FROM cronometro c
                INNER JOIN pomodoro p ON c.id_pomodoro = p.id
                ORDER BY p.data_hora DESC
                LIMIT 1
            """)

            # Obter o resultado da consulta
            configuracoes = self.cursor.fetchone()

            if configuracoes:
                tempo_estudo, tempo_pausa, quantidade_ciclos = configuracoes
                return tempo_estudo, tempo_pausa, quantidade_ciclos
            else:
                print("Nenhuma configuração encontrada, retornando os valores padrão.")
                return 25, 5, 10  # Valores padrão

        except sqlite3.Error as e:
            print("Erro ao obter configurações:", e)
            traceback.print_exc()  # Exibe o traceback completo
            return 25, 5, 10  # Valores padrão caso ocorra um erro no banco de dados
