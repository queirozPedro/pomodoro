import sqlite3
from datetime import datetime, timedelta

class Relatorio:
    # Inicializa a classe com a conexão do banco de dados
    def __init__(self, db_connection):
        self.db_connection = db_connection  # Instância da classe DBConnection
        self.conn = self.db_connection.get_connection()  # Obtém a conexão do banco
        self.cursor = self.conn.cursor()

    # Faz a busca dos pomodoros que estão armazenados no banco de dados
    def buscar_pomodoros(self):
        try:
            data_limite = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")  # Busca nos últimos 7 dias
            self.cursor.execute("""
                SELECT id, data_hora, status FROM pomodoro
                WHERE DATE(data_hora) >= ?
                ORDER BY data_hora ASC
            """, (data_limite,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar pomodoros: {e}")


    # Faz uma busca e a estatística dos pomodoros armazenados
    def buscar_estatisticas(self):
        try:
            data_limite = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")  # busca nos últimos 7 dias

            # Total de pomodoros concluídos
            self.cursor.execute("""
                SELECT COUNT(*) FROM pomodoro
                WHERE DATE(data_hora) >= ? AND status = 'Concluído'
            """, (data_limite,))
            total_concluidos = self.cursor.fetchone()[0]

            # Faz a estatística do tempo total estudado
            self.cursor.execute("""
                SELECT SUM(c.tempo_estudado) 
                FROM cronometro c
                JOIN pomodoro p ON c.id_pomodoro = p.id
                WHERE DATE(p.data_hora) >= ? AND p.status = 'Concluído'
            """, (data_limite,))
            tempo_total = self.cursor.fetchone()[0] or 0

            return {
                'total_concluidos': total_concluidos,
                'tempo_total': tempo_total,
                'tempo_medio': tempo_total / total_concluidos if total_concluidos > 0 else 0
            }

        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar estatísticas: {e}")


    # Exibe as estatísticas na interface
    def atualizar_interface(self, treeview, label_estatisticas=None):
        try:
            # Limpa a tabela antes de preencher
            for item in treeview.get_children():
                treeview.delete(item)

            # Obtém e exibe os registros
            registros = self.buscar_pomodoros()
            for registro in registros:
                treeview.insert("", "end", values=registro)

            # Atualiza as estatísticas se o label foi fornecido
            if label_estatisticas:
                estatisticas = self.buscar_estatisticas()
                texto = (f"Pomodoros concluídos: {estatisticas['total_concluidos']}\n"
                         f"Tempo total estudado: {estatisticas['tempo_total']} min\n"
                         f"Tempo médio por pomodoro: {estatisticas['tempo_medio']:.1f} min")
                label_estatisticas.config(text=texto)

        except Exception as e:
            raise Exception(f"Erro ao atualizar interface: {e}")
