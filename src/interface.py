import tkinter as tk
from tkinter import messagebox
import os

class Interface(tk.Tk):
    # Construtor
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("300x200")
        
        imagem_logo = os.path.join("imagens", "pomodoroLogo.png")
        self.wm_iconphoto(False, tk.PhotoImage(file=imagem_logo))
        self.centralizar_tela()

        # Criando um botão de exemplo
        self.btn_saudacao = tk.Button(self, text="Clique aqui", command=self.alterar_texto)
        self.btn_saudacao.pack(pady=70)


    def alterar_texto(self):
        self.btn_saudacao.pack_forget()


    def centralizar_tela(self):
        # Largura e altura da janela
        largura_janela = 300
        altura_janela = 200 

        # Largura e altura da tela do computador (em pixels)
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        '''
        Dividindo a largura e a altura por 2 obtemos o centro da tela (em pixels), mas
        se esse valor for diretamente atribuido para a posição da janela, a borda lateral
        direita que será colocada nessa posição, fazendo a tela ficar descentralizada.
        Para contornar isso, aplicamso um recuo usando as medidas da janela.
        '''
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2) - 100

        '''
        Nesse caso dá pra fazer self.geometry("300x200+100+200), onde 100 e 200 
        definem a posição da janela na tela.
        '''
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
