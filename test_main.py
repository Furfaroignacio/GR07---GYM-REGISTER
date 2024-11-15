import pytest
from unittest.mock import mock_open, patch
from main import validarRol

# Prueba: El usuario existe en el archivo JSON
def test_validarRol_usuario_existente():
    datos_simulados = '[{"dni": 12345678, "rol": 1}, {"dni": 87654321, "rol": 2}]'
    with patch("builtins.open", mock_open(read_data=datos_simulados)):
        resultado = validarRol(12345678)
        assert resultado == 1  # Rol esperado

# Prueba: El usuario no existe en el archivo JSON
def test_validarRol_usuario_inexistente():
    datos_simulados = '[{"dni": 12345678, "rol": 1}, {"dni": 87654321, "rol": 2}]'
    with patch("builtins.open", mock_open(read_data=datos_simulados)):
        resultado = validarRol(99999999)
        assert resultado is None  # No se encuentra el usuario

# Prueba: El archivo JSON no existe
def test_validarRol_archivo_no_existe():
    with patch("builtins.open", side_effect=FileNotFoundError):
        resultado = validarRol(12345678)
        assert resultado is None  # Archivo inexistente, resultado esperado
