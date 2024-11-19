import os
import json
import pytest
from admin import validarTexto, validarDNI, verificarArchivoUsuarios

# Pruebas para validarTexto
@pytest.mark.parametrize("texto, esperado", [
    ("Juan", True),        # Texto válido
    ("Maria", True),       # Texto válido
    ("Juan123", False),    # Contiene números
    ("123", False),        # Solo números
    ("!@#", False),        # Solo símbolos
    ("", False)            # Vacío
])
def test_validarTexto(texto, esperado):
    assert validarTexto(texto) == esperado

# Pruebas para validarDNI
@pytest.mark.parametrize("dni, esperado", [
    ("12345678", True),    # DNI válido
    ("87654321", True),    # DNI válido
    ("1234567", False),    # Menos de 8 dígitos
    ("123456789", False),  # Más de 8 dígitos
    ("1234abcd", False),   # Alfanumérico
    ("", False)            # Vacío
])
def test_validarDNI(dni, esperado):
    assert validarDNI(dni) == esperado

# Pruebas para verificarArchivoUsuarios
def test_verificarArchivoUsuarios(tmpdir):
    # Usa un directorio temporal para pruebas
    archivo_usuarios = tmpdir.join("usuarios.json")
    
    # Asegurarse de que no existe antes de ejecutar
    assert not archivo_usuarios.check()
    
    # Ejecutar la función dentro del entorno temporal
    os.chdir(tmpdir)
    verificarArchivoUsuarios()
    
    # Verificar que el archivo fue creado
    assert archivo_usuarios.check()
    
    # Verificar que el archivo contiene un array vacío
    with open(archivo_usuarios, 'r') as archivo:
        contenido = json.load(archivo)
        assert contenido == []
