import sqlite3
from datetime import datetime, time
from cronometro import Cronometro
import winsound

class Pomodoro():
    def __init__(self, interface, config, db_connection):
        # Referência para a interface
        self.interface = interface
        self.conn = db_connection.get_connection()
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        

        # Configurações do pomodoro
        self.tempo_estudo = config.tempo_estudo
        self.tempo_pausa = config.tempo_pausa
        self.quantidade_ciclos = config.quantidade_ciclos

        # Contagem de ciclos e estado e o id do after
        self.ciclo_atual = 0
        self.estudando = True
        self.rodando = False
        self.cronometro = None
        self.after_id = None 


    def iniciar_pomodoro(self):
        '''
        Inicia o Pomodoro e o ciclo inicial
        '''
        self.rodando = True
        self.iniciar_ciclo()


    def iniciar_ciclo(self):
        '''
        Inicia um novo ciclo de estudo ou pausa
        '''

        # Se for o último ciclo e não for de estudo então não tem pausa
        if self.ciclo_atual + 1 >= self.quantidade_ciclos and not self.estudando:
            self.rodando = False
            self.tocar_bipe_pausar()
            self.encerrar_pomodoro()
            self.interface.atualizar_tempo_cronometro('', self.rodando)
            return

        if self.estudando:
            self.tocar_bipe_iniciar()
            self.cronometro = Cronometro(self, self.tempo_estudo)
            self.interface.atualizar_tempo_cronometro(f"Estudando\n\n{self.cronometro.formatar_tempo()}")
        else:
            self.tocar_bipe_pausar()
            self.cronometro = Cronometro(self, self.tempo_pausa)
            self.interface.atualizar_tempo_cronometro(f"Pausa\n\n{self.cronometro.formatar_tempo()}")

        self.cronometro.iniciar()
        self.agendar_atualizacao()


    def pausar_cronometro(self):
        '''
        Pausa ou continua o cronômetro atual
        '''
        if self.after_id:
            self.interface.after_cancel(self.after_id) 
        
        if self.rodando:
            self.rodando = False
            self.cronometro.pausar()
        else:
            self.rodando = True
            self.cronometro.iniciar()
            self.agendar_atualizacao() 


    def reiniciar_cronometro(self):
        '''
        Reinicia o Pomodoro e o ciclo
        '''
        if self.after_id:
            self.interface.after_cancel(self.after_id)
        
        self.ciclo_atual = 0
        self.estudando = True
        self.iniciar_ciclo()


    def atualizar_cronometro(self, string, rodando):
        '''
        Atualiza a interface com o tempo e troca de ciclo quando necessário
        '''
        if rodando:
            estado = "Estudando" if self.estudando else "Pausa"
            self.interface.atualizar_tempo_cronometro(f"{estado}\n{string}")
        else:
            self.trocar_ciclo()


    def trocar_ciclo(self):
        '''
        Alterna entre estudo e pausa, contando ciclos
        '''
        if self.estudando:
            self.estudando = False
        else:
            self.estudando = True
            self.ciclo_atual += 1
        self.iniciar_ciclo()


    def agendar_atualizacao(self):
        '''
        Agendar a atualização do cronômetro a cada 1 segundo
        '''
        if self.after_id:
            self.interface.after_cancel(self.after_id)
        
        if self.cronometro.esta_rodando():
            self.after_id = self.interface.after(1000, self.atualizar_tempo)


    def atualizar_tempo(self):
        '''
        Atualiza o cronômetro e reagenda a próxima atualização
        '''
        if self.cronometro.esta_rodando():
            self.cronometro.atualizar_tempo()
            self.agendar_atualizacao()


    def encerrar_pomodoro(self, interrompido = False):
        '''
        Encerra o Pomodoro, limpa a janela e retorna à tela inicial
        '''
        if self.after_id:
            self.interface.after_cancel(self.after_id)
        
        if self.rodando:
            if interrompido:
                status = 'interrompido'
            else:
                status = 'encerrado'
            self.rodando = False
            if self.cronometro:
                self.cronometro.pausar()
                if self.estudando:
                    tempo_estudado = ((self.tempo_estudo * 60) * (self.ciclo_atual + 1)) - self.cronometro.get_tempo_restante()
                else:
                    tempo_estudado = (self.tempo_estudo * 60) * (self.ciclo_atual + 1)

        else:
            status = 'concluido'
            tempo_estudado = self.tempo_estudo * self.quantidade_ciclos
 

        id_pomodoro = self.salvar_pomodoro(status)
        self.salvar_cronometro(id_pomodoro, self.tempo_estudo, self.tempo_pausa, self.quantidade_ciclos, tempo_estudado)

        # Limpa a tela e exibe os controles iniciais
        self.interface.limpar_janela()
        self.interface.exibir_controles_iniciais()


    def salvar_cronometro(self, id_pomodoro, tempo_estudo, tempo_pausa, quantidade_ciclos, tempo_estudado = 0):
        '''
        Insere dados no cronômetro
        '''
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


    def salvar_pomodoro(self, status):
        '''
        Salva um novo registro de Pomodoro
        '''
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


    def criar_tabelas(self):
        self.cursor.execute("""
         CREATE TABLE IF NOT EXISTS pomodoro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL
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


    def tocar_bipe_iniciar(self, frequencia=1000, duracao=300):
        winsound.Beep(frequencia, duracao)  # Toca o bipe
    

    def tocar_bipe_pausar(self, frequencia=2400, duracao=300):
        winsound.Beep(frequencia, duracao)  # Toca o bipe
        
            