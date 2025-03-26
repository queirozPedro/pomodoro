import pytest
from unittest.mock import MagicMock
from src.pomodoro import Pomodoro
from src.cronometro import Cronometro

@pytest.fixture
def setup_pomodoro():
    interface_mock = MagicMock()
    config_mock = MagicMock()
    config_mock.tempo_estudo = 25
    config_mock.tempo_pausa = 5
    config_mock.quantidade_ciclos = 4
    db_connection_mock = MagicMock()
    db_connection_mock.get_connection.return_value = MagicMock()
    pomodoro = Pomodoro(interface_mock, config_mock, db_connection_mock)
    return pomodoro, interface_mock


def test_iniciar_pomodoro(setup_pomodoro):
    pomodoro, interface_mock = setup_pomodoro
    pomodoro.iniciar_pomodoro()

    assert pomodoro.rodando is True


def test_pausar_cronometro(setup_pomodoro):
    pomodoro, interface_mock = setup_pomodoro
    pomodoro.iniciar_pomodoro()
    pomodoro.pausar_cronometro()
    assert pomodoro.rodando is False
    interface_mock.after_cancel.assert_called_once()


def test_reiniciar_cronometro(setup_pomodoro):
    pomodoro, interface_mock = setup_pomodoro
    pomodoro.iniciar_pomodoro()
    pomodoro.reiniciar_cronometro()
    assert pomodoro.ciclo_atual == 0


def test_encerrar_pomodoro(setup_pomodoro):
    pomodoro, interface_mock = setup_pomodoro
    pomodoro.iniciar_pomodoro()
    pomodoro.encerrar_pomodoro()
    assert pomodoro.rodando is False
    interface_mock.limpar_janela.assert_called_once()
    interface_mock.exibir_controles_iniciais.assert_called_once()
