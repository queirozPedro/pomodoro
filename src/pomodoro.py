from cronometro import Cronometro
from connection import Connection
class Pomodoro():
    def __init__(self, interface, config):
        self.interface = interface
        self.tempo_estudo = config.get_tempo_estudo()
        self.tempo_pausa = config.get_tempo_pausa()
        self.cronometro = Cronometro(self.interface, self.tempo_estudo, self.tempo_pausa)
        self.banco = Connection()  # Conectando ao banco de dados

    def iniciar_estudo(self):
        self.cronometro.iniciar()

    def pausar_cronometro(self):
        if not self.cronometro.esta_rodando():
            self.cronometro.iniciar()
        else:
            self.cronometro.pausar()


    def reiniciar_cronometro(self):
        # Salvando os tempos no banco de dados
        self.banco.salvar_pomodoro(self.tempo_estudo, self.tempo_pausa)
        self.cronometro.reiniciar()