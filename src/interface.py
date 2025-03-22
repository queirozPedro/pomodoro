import tkinter as tk
from tkinter import messagebox
import os
from pomodoro import Pomodoro 
from config import Config

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.exibir_janela()
        self.centralizar_janela()
        self.exibir_controles_iniciais()


    def exibir_janela(self):
        '''
        Cria uma janela para a aplicação
        '''
        self.title("Pomodoro")
        
        self.altura_janela = 300
        self.largura_janela = 200
        self.minsize(300, 200)
        self.geometry(f"{str(self.altura_janela)}x{str(self.largura_janela)}")

        imagem_logo = os.path.join("imagens", "pomodoroLogo.png")
        self.wm_iconphoto(False, tk.PhotoImage(file=imagem_logo))


    def centralizar_janela(self):
        '''
        Centraliza a janela na tela do computador
        '''
        # Largura e altura da tela do computador (em pixels)
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        '''
        Dividindo a largura e a altura por 2 obtemos o centro da tela (em pixels), mas
        se esse valor for diretamente atribuido para a posição da janela, a borda lateral
        direita que será colocada nessa posição, fazendo a tela ficar descentralizada.
        Para contornar isso, aplicamso um recuo usando as medidas da janela.
        '''
        pos_x = (largura_tela // 2) - (self.largura_janela // 2)
        pos_y = (altura_tela // 2) - (self.altura_janela // 2) - 50 #offset

        '''
        Nesse caso dá pra fazer self.geometry("300x200+100+200), onde 100 e 200 
        definem a posição da janela na tela.
        '''
        self.geometry(f"{str(self.largura_janela)}x{str(self.altura_janela)}+{pos_x}+{pos_y}")


    def exibir_controles_iniciais(self):
        '''
        Exibe os controles iniciais, botão de começar o pomodoro, de configurações
        '''
        self.botao_iniciar = tk.Button(self, text="Iniciar Pomodoro", command=self.iniciar_pomodoro)
        self.botao_iniciar.place(relx=0.5, rely=0.4, anchor="center")

        self.botao_config = tk.Button(self, text="Configurações")
        self.botao_config.pack(side='bottom', expand=False, padx=10, pady=5)


    def iniciar_pomodoro(self):
        self.exibir_cronometro()
        self.destruir_botoes()
        self.criar_pomodoro()
        self.criar_botoes_controle()


    def exibir_cronometro(self):
        # Exibe o cronômetro
        self.label_tempo = tk.Label(self, text="Tempo: 0", font=("Arial", 24))
        self.label_tempo.place(relx=0.5, rely=0.4, anchor="center")


    def destruir_botoes(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()


    def criar_pomodoro(self):
        # Cria o pomodoro e inicia o estudo
        self.pomodoro = Pomodoro(self, Config(1, 1, 2))
        self.pomodoro.iniciar_estudo()


    def criar_botoes_controle(self):
        # Cria os botões de pausa e de reiniciar
        self.botao_pausar = tk.Button(self, text="Pausar", command=self.pomodoro.pausar_cronometro)
        self.botao_reiniciar = tk.Button(self, text="Reiniciar", command=self.pomodoro.reiniciar_cronometro)
        self.botao_pausar.pack(side="left", expand=False, padx=10, pady=5)
        self.botao_reiniciar.pack(side="right", expand=False, padx=10, pady=5)


    def exibir_configuracoes(self):
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Quantidade de Sessões", command=lambda: print("Opção 1 selecionada"))
        self.popup_menu.add_command(label="Tempo de Estudo", command=lambda: print("Opção 1 selecionada"))
        self.popup_menu.add_command(label="Tempo de Pausa", command=lambda: print("Opção 2 selecionada"))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Fechar", command=self.destroy)


    def atualizar_label_cronometro(self, novo_texto):
        self.label_tempo.config(text=novo_texto)  # Atualiza a interface
        