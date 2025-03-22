class Config():
    def __init__(self, tempo_estudo = 25, tempo_pausa = 5, quantidade_ciclos = 5):
        self.tempo_estudo = tempo_estudo
        self.tempo_pausa = tempo_pausa
        self.quantidade_ciclos = quantidade_ciclos
    
    def get_tempo_estudo(self):
        return self.tempo_estudo
    
    def get_tempo_pausa(self):
        return self.tempo_pausa
    
    def get_quantidade_ciclos(self):
        return self.quantidade_ciclos