import sqlite3
import pytest
from src.db_connection import DBConnection


def teste_instancia_unica():
  instancia1 = DBConnection.get_instance(":memory:")
  instancia2 = DBConnection.get_instance(":memory:")
  
  assert instancia1 is instancia2

  
def teste_obter_conexao():
  instancia = DBConnection.get_instance(":memory:")
  conn = instancia.get_connection()
  assert isinstance(conn, sqlite3.Connection)
  cur = conn.cursor()
  cur.execute("SELECT 1")
  resultado = cur.fetchone()
  assert resultado[0] == 1

  
def teste_fechar_conexao():
  instancia = DBConnection.get_instance(":memory:")
  conn = instancia.get_connection()
  instancia.close_connection()
  with pytest.raises(sqlite3.ProgrammingError):
    conn.execute("SELECT 1")
