import tkinter as tk
from tkinter import ttk
import os
from pomodoro import Pomodoro 
from config import Config
from db_connection import DBConnection
from relatorio import Relatorio

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configurar_janela()
        self.configurar_variaveis()
        self.exibir_controles_iniciais()


    # ----- Janela e Configurações -----

    def configurar_janela(self):
        '''
        Cria uma janela para a aplicação organizando tamanho, icone e posição
        '''
        self.title("Pomodoro")
        self.altura_janela = 350
        self.largura_janela = 250
        self.minsize(350, 250)
        self.maxsize(350, 250)
        self.geometry(f"{str(self.altura_janela)}x{str(self.largura_janela)}")
        imagem_logo = os.path.join("imagens", "pomodoroLogo.png")
        self.wm_iconphoto(False, tk.PhotoImage(file=imagem_logo))

        # Centraliza a janela na tela do computador

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (self.largura_janela // 2)
        pos_y = (altura_tela // 2) - (self.altura_janela // 2) - 50 
        self.geometry(f"{str(self.largura_janela)}x{str(self.altura_janela)}+{pos_x}+{pos_y}")

        
    def configurar_variaveis(self):
        
        self.db_connection = DBConnection()
        
        self.config = Config(self.db_connection)
        self.opcoes_config = {
            "Tempo de Estudo": self.config.tempo_estudo,
            "Tempo de Pausa": self.config.tempo_pausa,
            "Quantidade de Ciclos": self.config.quantidade_ciclos
        }

        self.opcao_selecionada = tk.StringVar(self)
        self.opcao_selecionada.set("Configurações")
        self.valor_var = tk.IntVar()

        self.pomodoro = None
        self.protocol("WM_DELETE_WINDOW", self.quando_fechar)


    # ---- Tela Inicial -----


    def exibir_controles_iniciais(self):
        '''
        Exibe os controles iniciais, botão de começar o pomodoro, de configurações
        '''
        self.botao_iniciar = self.criar_botao("Iniciar Pomodoro", self.iniciar_pomodoro, 0.5, 0.3)
        self.dropdown_menu = self.criar_dropdown()
        self.criar_campo_valor()
        self.criar_botao_salvar()
        self.criar_botao_relatorio() 


    def criar_botao(self, texto, comando, rel_x, rel_y, largura= None):
        '''
        Cria um botão com base no texto, no comando e na posição vertical
        '''
        if largura != None:
            botao = tk.Button(self, text=texto, command=comando, width=largura)
        else:
            botao = tk.Button(self, text=texto, command=comando)
        botao.place(relx=rel_x, rely=rel_y, anchor="center")
        return botao


    def criar_dropdown(self):
        '''
        Cria o Combobox para selecionar a opção.
        '''
        combobox = ttk.Combobox(
            self, 
            textvariable=self.opcao_selecionada,
            values=list(self.opcoes_config.keys()), 
            state="readonly"
        )
        combobox.place(relx=0.5, rely=0.7, anchor="center")
        combobox.bind("<<ComboboxSelected>>", self.mostrar_campo_valor)
        return combobox
    
    # Método para criar botão de gerar relatório na interface
    def criar_botao_relatorio(self):
        """
        Cria e posiciona o botão de relatórios na interface.
        """
        botao_relatorio = ttk.Button(
            self,
            text="Relatórios",
            command=self.mostrar_relatorio_simples
        )
        botao_relatorio.place(relx=0.5, rely=0.5, anchor="center")
        return botao_relatorio


# Método para criar uma nova janela para exibir os relatorios
    def mostrar_relatorio_simples(self):
        """Exibe o relatório usando o método existente da classe Relatorio"""
        # Cria janela básica
        janela = tk.Toplevel(self)
        janela.title("Relatório Pomodoro")
        janela.geometry("500x400")
        
        # Cria os componentes mínimos
        treeview = ttk.Treeview(janela, columns=("ID", "Data", "Status", "Tempo"), show="headings")
        for col in ("ID", "Data", "Status", "Tempo"):
            treeview.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        
        lbl_estatisticas = ttk.Label(janela, text="", justify="left")
        
        # Layout
        treeview.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        lbl_estatisticas.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Chama o método existente da classe Relatorio
        try:
            relatorio = Relatorio(self.db_connection)
            relatorio.atualizar_interface(
                treeview=treeview,
                label_estatisticas=lbl_estatisticas
            )
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{str(e)}")

    # ---- Configurações ----


    def criar_campo_valor(self):
        '''
        Cria um campo para editar o valor da opção
        '''
        self.frame_valor = ttk.Frame(self)
        self.valor_entry = ttk.Entry(self.frame_valor, textvariable=self.valor_var, width=5, justify="center")

        self.botao_menos = ttk.Button(self.frame_valor, text="-", width=2, command=self.decrementar_valor)
        self.botao_mais = ttk.Button(self.frame_valor, text="+", width=2, command=self.incrementar_valor)

        self.botao_menos.pack(side="left", padx=2)
        self.valor_entry.pack(side="left", padx=2)
        self.botao_mais.pack(side="left", padx=2)

        self.frame_valor.place(relx=0.5, rely=0.8, anchor="center")
        self.frame_valor.place_forget()  


    def criar_botao_salvar(self):
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

        # Isso percorre todos os valores de opçoes e aplica em config
        valores = []
        for valor in self.opcoes_config.values():
            valores.append(valor)
        self.config.tempo_estudo = valores[0]
        self.config.tempo_pausa = valores[1]
        self.config.quantidade_ciclos = valores[2]
            
        self.frame_valor.place_forget()
        self.botao_salvar.place_forget()
        self.opcao_selecionada.set("Configurações")


    # ---- Pomodoro ----


    def iniciar_pomodoro(self):
        self.limpar_janela()
        self.pomodoro = Pomodoro(self, self.config, self.db_connection)
        self.pomodoro.iniciar_pomodoro()
        self.criar_botoes_controle()


    def limpar_janela(self):
        '''
        Remove todos os widgets da janela
        '''
        if self.pomodoro:
            self.pomodoro = None
        for widget in self.winfo_children():
            widget.destroy()


    def criar_botoes_controle(self):
        '''
        Coloca os botões de controle do pomodoro
        '''
        self.botao_pausar = self.criar_botao("Pausar", self.pomodoro.pausar_cronometro, 0.33, 0.75, 6)
        self.botao_reiniciar = self.criar_botao("Reiniciar", self.pomodoro.reiniciar_cronometro, 0.5, 0.75, 6)
        self.botao_encerrar = self.criar_botao("Encerrar", self.pomodoro.encerrar_pomodoro, 0.67, 0.75, 6)


    # ---- Atualizar Tela ----


    def atualizar_tempo_cronometro(self, novo_texto, rodando=True):
        if not hasattr(self, 'label_tempo') or not self.label_tempo.winfo_exists():
            self.label_tempo = tk.Label(self, text="", font=("Arial", 24))
            self.label_tempo.place(relx=0.5, rely=0.4, anchor="center")

        if rodando:
            self.label_tempo.config(text=novo_texto)
        else:
            self.limpar_janela()
            self.exibir_controles_iniciais()


    def quando_fechar(self):
        if self.pomodoro:
            self.pomodoro.encerrar_pomodoro(True)
        self.db_connection.close_connection()  
        self.destroy() 