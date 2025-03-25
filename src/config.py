class Config():
    def __init__(self, tempo_estudo = 25, tempo_pausa = 5, quantidade_ciclos = 4):
        self.tempo_estudo = tempo_estudo
        self.tempo_pausa = tempo_pausa
        self.quantidade_ciclos = quantidade_ciclos

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