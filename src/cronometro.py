class Cronometro():
    def __init__(self, pomodoro, tempo):
        self.pomodoro = pomodoro
        self.tempo = tempo
        self.tempo_restante = tempo * 60
        self.rodando = False


    def iniciar(self):
        '''
        Dá o play no cronômetro
        '''
        if not self.rodando:
            self.rodando = True
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)


    def pausar(self):
        '''
        Atualiza o estados de rodando para falso, parando o cronômetro
        '''
        self.rodando = False


    def reiniciar(self):
        '''
        Reinicia os tempos do cronômetro
        '''
        self.tempo_restante = self.tempo * 60
        self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)
        self.rodando = False


    def atualizar_tempo(self):
        '''
        Incrementa um no valor do cronômetro desde que ele esteja rodando
        '''
        if self.rodando and self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)
        elif self.tempo_restante == 0:
            self.rodando = False
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)


    def formatar_tempo(self):
        '''
        Recebe o tempo em segundos e formata para minutos e segundos
        '''
        minutos = self.tempo_restante // 60
        segundos = self.tempo_restante % 60
        return f"{minutos:02}:{segundos:02}"


    def esta_rodando(self):
        return self.rodando
    
    def get_tempo_restante(self):
        return self.tempo_restante