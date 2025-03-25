from cronometro import Cronometro

class Pomodoro():
    def __init__(self, interface, config):
        # Referência para a interface
        self.interface = interface

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
        if self.ciclo_atual >= self.quantidade_ciclos:
            self.rodando = False
            self.interface.atualizar_tempo_cronometro('', self.rodando)
            return

        # Se for o último ciclo e não for de estudo
        if self.ciclo_atual + 1 >= self.quantidade_ciclos and not self.estudando:
            self.rodando = False
            self.interface.atualizar_tempo_cronometro('', self.rodando)
            return

        if self.estudando:
            self.cronometro = Cronometro(self, self.tempo_estudo)
            self.interface.atualizar_tempo_cronometro(f"Estudando\n{self.cronometro.formatar_tempo()}")
        else:
            self.cronometro = Cronometro(self, self.tempo_pausa)
            self.interface.atualizar_tempo_cronometro(f"Pausa\n{self.cronometro.formatar_tempo()}")

        self.cronometro.iniciar()
        self.agendar_atualizacao()


    def pausar_cronometro(self):
        '''
        Pausa ou continua o cronômetro atual
        '''
        if self.rodando:
            self.rodando = False
            self.cronometro.pausar()
            if self.after_id:
                self.interface.after_cancel(self.after_id) 
        else:
            self.rodando = True
            self.cronometro.iniciar()
            self.agendar_atualizacao() 


    def reiniciar_cronometro(self):
        '''
        Reinicia o Pomodoro e o ciclo
        '''
        self.ciclo_atual = 0
        self.estudando = True
        if self.after_id:
            self.interface.after_cancel(self.after_id)
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
        if self.cronometro.esta_rodando():
            self.after_id = self.interface.after(1000, self.atualizar_tempo)


    def atualizar_tempo(self):
        '''
        Atualiza o cronômetro e reagenda a próxima atualização
        '''
        if self.cronometro.esta_rodando():
            self.cronometro.atualizar_tempo()
            self.agendar_atualizacao()


    def encerrar_pomodoro(self):
        '''
        Encerra o Pomodoro, limpa a janela e retorna à tela inicial
        '''
        if self.rodando:
            self.rodando = False
            if self.cronometro:
                self.cronometro.pausar()

            if self.after_id:
                self.interface.after_cancel(self.after_id)
        
        # Limpa a tela e exibe os controles iniciais
        self.interface.limpar_janela()
        self.interface.exibir_controles_iniciais()
