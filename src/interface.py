import tkinter as tk
from tkinter import ttk
import os
from pomodoro import Pomodoro 
from config import Config

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configurar_janela()
        self.exibir_controles_iniciais()


    def configurar_janela(self):
        '''
        Cria uma janela para a aplicação organizando tamanho, icone e posição
        '''
        self.title("Pomodoro")
        self.altura_janela = 350
        self.largura_janela = 250
        self.minsize(350, 250)
        self.geometry(f"{str(self.altura_janela)}x{str(self.largura_janela)}")
        imagem_logo = os.path.join("imagens", "pomodoroLogo.png")
        self.wm_iconphoto(False, tk.PhotoImage(file=imagem_logo))

        # Centraliza a janela na tela do computador

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (self.largura_janela // 2)
        pos_y = (altura_tela // 2) - (self.altura_janela // 2) - 50 
        self.geometry(f"{str(self.largura_janela)}x{str(self.altura_janela)}+{pos_x}+{pos_y}")


    def exibir_controles_iniciais(self):
        '''
        Exibe os controles iniciais, botão de começar o pomodoro, de configurações
        '''
        self.botao_iniciar = tk.Button(self, text="Iniciar Pomodoro", command=self.iniciar_pomodoro)
        self.botao_iniciar.place(relx=0.5, rely=0.3, anchor="center")

        self.opcoes_config = {
            "Tempo de Estudo": 25,
            "Tempo de Pausa": 5,
            "Quantidade de Ciclos": 4
        }

        self.opcao_selecionada = tk.StringVar(self)
        self.opcao_selecionada.set("Configurações")

        self.criar_dropdown()
        self.criar_campo_valor()
        self.criar_botao()


    def criar_dropdown(self):
        '''
        Cria o Combobox para selecionar a opção.
        '''
        self.combobox = ttk.Combobox(
            self, 
            textvariable=self.opcao_selecionada,
            values=list(self.opcoes_config.keys()), 
            state="readonly"
        )
        self.combobox.place(relx=0.5, rely=0.7, anchor="center")
        self.combobox.bind("<<ComboboxSelected>>", self.mostrar_campo_valor)


    def criar_campo_valor(self):
        '''
        Cria um campo para editar o valor da opção
        '''
        self.frame_valor = ttk.Frame(self)

        self.valor_var = tk.IntVar()
        self.valor_entry = ttk.Entry(self.frame_valor, textvariable=self.valor_var, width=5, justify="center")

        self.botao_menos = ttk.Button(self.frame_valor, text="-", width=2, command=self.decrementar_valor)
        self.botao_mais = ttk.Button(self.frame_valor, text="+", width=2, command=self.incrementar_valor)

        self.botao_menos.pack(side="left", padx=2)
        self.valor_entry.pack(side="left", padx=2)
        self.botao_mais.pack(side="left", padx=2)

        self.frame_valor.place(relx=0.5, rely=0.8, anchor="center")
        self.frame_valor.place_forget()  


    def criar_botao(self):
        '''
        Cria o botão para salvar a edição do valor
        '''
        self.botao_salvar = ttk.Button(self, text="Salvar", command=self.salvar_valor)
        self.botao_salvar.place(relx=0.5, rely=0.9, anchor="center")
        self.botao_salvar.place_forget()  


    def mostrar_campo_valor(self, event=None):
        '''
        Exibe o campo de valor e preenche com o valor da opção selecionada
        '''
        opcao = self.opcao_selecionada.get()

        if opcao == "Configurações":
            return  

        self.valor_var.set(self.opcoes_config[opcao])

        self.frame_valor.place(relx=0.5, rely=0.8, anchor="center")
        self.botao_salvar.place(relx=0.5, rely=0.9, anchor="center")


    def incrementar_valor(self):
        '''
        Aumenta o valor do campo de edição
        '''
        self.valor_var.set(self.valor_var.get() + 1)


    def decrementar_valor(self):
        '''
        Diminui o valor do campo de edição, evitando valores negativos
        '''
        if self.valor_var.get() > 0:
            self.valor_var.set(self.valor_var.get() - 1)


    def salvar_valor(self):
        '''
        Salva o valor editado no dicionário, imprime no console e esconde os botões
        '''
        opcao = self.opcao_selecionada.get()
        novo_valor = self.valor_var.get()
        self.opcoes_config[opcao] = novo_valor  

        self.frame_valor.place_forget()
        self.botao_salvar.place_forget()
        self.opcao_selecionada.set("Configurações")


    def iniciar_pomodoro(self):
        self.limpar_janela()
        self.criar_pomodoro()
        self.criar_botoes_controle()


    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()


    def criar_pomodoro(self):
        self.pomodoro = Pomodoro(self, Config(self.opcoes_config["Tempo de Estudo"], self.opcoes_config["Tempo de Pausa"], self.opcoes_config["Quantidade de Ciclos"]))
        self.pomodoro.iniciar_pomodoro()


    def criar_botoes_controle(self):
        self.botao_pausar = tk.Button(self, text="Pausar", command=self.pomodoro.pausar_cronometro)
        self.botao_reiniciar = tk.Button(self, text="Reiniciar", command=self.pomodoro.reiniciar_cronometro)
        self.botao_pausar.pack(side="left", expand=False, padx=10, pady=10)
        self.botao_reiniciar.pack(side="right", expand=False, padx=10, pady=10)


    def atualizar_tempo_cronometro(self, novo_texto, rodando = True):
        
        # Se o label do tempo não existir ele é criado
        if not hasattr(self, 'label_tempo'):
            self.label_tempo = tk.Label(self, text="", font=("Arial", 24))
            self.label_tempo.place(relx=0.5, rely=0.3, anchor="center")
        if rodando:
            self.label_tempo.config(text=novo_texto)
        else:
            self.limpar_janela()