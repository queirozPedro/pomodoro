from types import SimpleNamespace
import pytest
from src.cronometro import Cronometro


def teste_iniciar_pomodoro():
  atualizacoes = []
  def atualizar(tempo_formatado, rodando):
    atualizacoes.append((tempo_formatado, rodando))
  pomodoro = SimpleNamespace(atualizar_cronometro=atualizar)
  crono = Cronometro(pomodoro, 1)
  crono.iniciar()
  
  assert crono.rodando is True
  assert atualizacoes[0] == ("01:00", True)


def teste_pausar_cronometro():
  atualizacoes = []
  def atualizar(tempo_formatado, rodando):
    atualizacoes.append((tempo_formatado, rodando))
  pomodoro = SimpleNamespace(atualizar_cronometro=atualizar)
  crono = Cronometro(pomodoro, 1)
  crono.iniciar()
  crono.pausar()
  
  assert crono.rodando is False


def teste_formatar_tempo():
  def atualizar(tempo_formatado, rodando):
    pass
  pomodoro = SimpleNamespace(atualizar_cronometro=atualizar)
  crono = Cronometro(pomodoro, 1)
  crono.tempo_restante = 65
  
  assert crono.formatar_tempo() == "01:05"


def teste_esta_rodando():
  def atualizar(tempo_formatado, rodando):
    pass
  pomodoro = SimpleNamespace(atualizar_cronometro=atualizar)
  crono = Cronometro(pomodoro, 1)
  crono.rodando = True
  
  assert crono.esta_rodando() is True


def teste_tempo_restante():
  def atualizar(tempo_formatado, rodando):
    pass
  pomodoro = SimpleNamespace(atualizar_cronometro=atualizar)
  crono = Cronometro(pomodoro, 1)
  crono.tempo_restante = 42
  
  assert crono.get_tempo_restante() == 42
