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
            self.cursor.execute("""
                SELECT 
                    p.id,
                    p.data_hora,
                    p.status,
                    c.tempo_estudado,
                    c.tempo_estudo,
                    c.tempo_pausa,
                    c.quantidade_ciclos
                FROM pomodoro p
                JOIN cronometro c ON p.id = c.id_pomodoro
                ORDER BY p.data_hora DESC
                LIMIT 50
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar pomodoros: {e}")


    # Faz uma busca e a estatística dos pomodoros armazenados
    def buscar_estatisticas(self):
        """Calcula estatísticas dos últimos 7 dias"""
        try:
            data_limite = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
            
            # Total de pomodoros concluídos
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM pomodoro 
                WHERE status = 'concluido' 
                AND data_hora >= ?
            """, (data_limite,))
            total_concluidos = self.cursor.fetchone()[0]

            # Tempo total estudado
            self.cursor.execute("""
                SELECT SUM(c.tempo_estudado)
                FROM cronometro c
                JOIN pomodoro p ON c.id_pomodoro = p.id
                WHERE p.status = 'concluido'
                AND p.data_hora >= ?
            """, (data_limite,))
            tempo_total = self.cursor.fetchone()[0] or 0

            return {
                'total_concluidos': total_concluidos,
                'tempo_total': tempo_total,
                'tempo_medio': tempo_total / total_concluidos if total_concluidos > 0 else 0
            }
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar estatísticas: {e}")

    def formatar_data(self, data_original):
        """Formata a data para exibição"""
        try:
            return datetime.strptime(data_original, "%d-%m-%Y %H:%M:%S").strftime("%d/%m/%Y %H:%M")
        except:
            return data_original


    # Exibe as estatísticas na interface
    def atualizar_interface(self, treeview, label_estatisticas=None):
        """Atualiza a interface com dados dos pomodoros"""
        try:
            # Limpa a treeview
            for item in treeview.get_children():
                treeview.delete(item)

            # Obtém e exibe os registros
            registros = self.buscar_pomodoros()
            for registro in registros:
                treeview.insert("", "end", values=registro)

            # Atualiza estatísticas se o label foi fornecido
            if label_estatisticas:
                estatisticas = self.buscar_estatisticas()
                texto = (f"Pomodoros concluídos: {estatisticas['total_concluidos']}\n"
                        f"Tempo total estudado: {estatisticas['tempo_total']} min\n"
                        f"Tempo médio por pomodoro: {estatisticas['tempo_medio']:.1f} min")
                label_estatisticas.config(text=texto)

        except Exception as e:
            raise Exception(f"Erro ao atualizar interface: {e}")