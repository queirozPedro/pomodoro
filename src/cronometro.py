import tkinter as tk

class Cronometro():
    def __init__(self, interface, tempo_estudo, tempo_pausa):
        self.interface = interface
        self.tempo_estudo = tempo_estudo
        self.tempo_pausa = tempo_pausa
        self.tempo_restante_estudo = tempo_estudo * 60
        self.tempo_restante_pausa = tempo_pausa * 60
        self.rodando = False


    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            self.atualizar_tempo()


    def pausar(self):
        self.rodando = False 


    def reiniciar(self):
        self.tempo_restante_estudo = self.tempo_estudo * 60
        # Atualização na interface é feita a partir do Cronometro
        self.interface.atualizar_label_cronometro(self.formatar_tempo(self.tempo_estudo, self.tempo_restante_estudo)) #passando dois argumentos  
        self.rodando = False


    def atualizar_tempo(self):
        if self.rodando and self.tempo_restante_estudo > 0:
            self.tempo_restante_estudo -= 1
            self.interface.atualizar_label_cronometro(f"Estudando\n{self.formatar_tempo(self.tempo_estudo, self.tempo_restante_estudo)}")  
            self.interface.after(1000, self.atualizar_tempo) 
        elif self.rodando and self.tempo_restante_pausa > 0:
            self.tempo_restante_pausa -= 1
            self.interface.atualizar_label_cronometro(f"Intervalo\n{self.formatar_tempo(self.tempo_pausa, self.tempo_restante_pausa)}")  
            self.interface.after(1000, self.atualizar_tempo) 
        elif self.tempo_restante_estudo == 0 and  self.tempo_restante_pausa == 0:
            self.interface.atualizar_label_cronometro(f"Fim do Pomodoro")


    def esta_rodando(self):
        return self.rodando


    def formatar_tempo(self, tempo, tempo_restante):
        tempo = tempo_restante // 60
        segundos = tempo_restante % 60
        return f"{tempo:02}:{segundos:02}" 