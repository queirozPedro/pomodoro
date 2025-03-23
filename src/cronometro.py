class Cronometro():
    def __init__(self, pomodoro, tempo):
        self.pomodoro = pomodoro
        self.tempo = tempo
        self.tempo_restante = tempo * 60
        self.rodando = False


    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)


    def pausar(self):
        self.rodando = False


    def reiniciar(self):
        self.tempo_restante = self.tempo * 60
        self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)
        self.rodando = False


    def atualizar_tempo(self):
        if self.rodando and self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)
        elif self.tempo_restante == 0:
            self.rodando = False
            self.pomodoro.atualizar_cronometro(self.formatar_tempo(), self.rodando)


    def esta_rodando(self):
        return self.rodando


    def formatar_tempo(self):
        minutos = self.tempo_restante // 60
        segundos = self.tempo_restante % 60
        return f"{minutos:02}:{segundos:02}"
