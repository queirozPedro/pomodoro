import sqlite3
import pytest
from src.config import Config


class CursorFalso:
  def __init__(self, resultado=None, levantar_excecao=False):
    self.resultado = resultado
    self.levantar_excecao = levantar_excecao

  def execute(self, query):
    if self.levantar_excecao:
      raise sqlite3.Error("erro simulado")
    # executa sem ação

  def fetchone(self):
    return self.resultado


class ConexaoFalsa:
  def __init__(self, cursor):
    self._cursor = cursor

  def cursor(self):
    return self._cursor


class DBFalsa:
  def __init__(self, resultado=None, levantar_excecao=False):
    self._conn = ConexaoFalsa(CursorFalso(resultado, levantar_excecao))

  def get_connection(self):
    return self._conn


def test_inicializacao_valida():
  db = DBFalsa(resultado=(30, 10, 5))
  cfg = Config(db)
  
  assert cfg.tempo_estudo == 30
  assert cfg.tempo_pausa == 10
  assert cfg.quantidade_ciclos == 5

  
def test_inicializacao_default():
  db = DBFalsa(resultado=None)
  cfg = Config(db)
  
  assert cfg.tempo_estudo == 25
  assert cfg.tempo_pausa == 5
  assert cfg.quantidade_ciclos == 4

  
def test_inicializacao_excecao():
  db = DBFalsa(resultado=(30, 10, 5), levantar_excecao=True)
  cfg = Config(db)
  
  assert cfg.tempo_estudo == 25
  assert cfg.tempo_pausa == 5
  assert cfg.quantidade_ciclos == 4

  
def test_setters():
  db = DBFalsa(resultado=(10, 10, 10))
  cfg = Config(db)
  cfg.tempo_estudo = 0
  cfg.tempo_pausa = -5
  cfg.quantidade_ciclos = 0
  
  assert cfg.tempo_estudo == 1
  assert cfg.tempo_pausa == 1
  assert cfg.quantidade_ciclos == 1

  cfg.tempo_estudo = 15
  cfg.tempo_pausa = 8
  cfg.quantidade_ciclos = 3
  
  assert cfg.tempo_estudo == 15
  assert cfg.tempo_pausa == 8
  assert cfg.quantidade_ciclos == 3
