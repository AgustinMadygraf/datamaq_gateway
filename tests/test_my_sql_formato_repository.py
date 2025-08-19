
"""
Path: tests/test_my_sql_formato_repository.py
"""


import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.pymsql.pymysql_formato import MySQLFormatoRepository
from entities.formato import Formato

@patch("infrastructure.pymsql.my_sql_formato_repository.pymysql.connect")
def testget_ultimo_formato_returns_formato(mock_connect):
    "Prueba que get_ultimo_formato devuelve un Formato cuando hay datos"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        "id_formato": 1,
        "formato": "A4",
        "ancho_bobina_mm": 210
    }
    repo = MySQLFormatoRepository()

    # Act
    result = repo.get_ultimo_formato()

    # Assert
    assert isinstance(result, Formato)
    assert result.id_formato == 1
    assert result.formato == "A4"
    assert result.ancho_bobina_mm == 210

@patch("infrastructure.pymsql.my_sql_formato_repository.pymysql.connect")
def testget_ultimo_formato_returns_none_when_no_data(mock_connect):
    "Prueba que get_ultimo_formato devuelve None cuando no hay datos"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    repo = MySQLFormatoRepository()

    # Act
    result = repo.get_ultimo_formato()

    # Assert
    assert result is None
