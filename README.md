# Sistema de Administración de Gimnasio 🏋️‍♂️

Este proyecto es un sistema de administración de un gimnasio desarrollado en **Python**, que permite gestionar usuarios, clases, pagos y más. Está diseñado para funcionar como una aplicación de con interfaz gráfica.

---

## Características ✨

- **Gestión de Usuarios**:
  - Registrar nuevos usuarios.
  - Buscar, listar y borrar usuarios.
- **Gestión de Clases**:
  - Registro y asignación de clases a los usuarios.
  - Listado de clases disponibles.
- **Gestión de Pagos**:
  - Crear Facturas luego de la subscripcion de una clase
- **Roles de Usuario**:
  - **Administrador**: acceso completo al sistema.
  - **Miembro**: acceso limitado a inscripciones de clases y consultar facturas, ver perfil y editar
- **Persistencia de Datos**:
  - Uso de archivos **JSON** para almacenar datos (simula Base de Datos).

---

## Requisitos 🛠️

- **Python 3.10 o superior**
- Librerías necesarias (instalar con `pip`):
  - `tkinter` 
  - `customtkinter` 
  - `pypdf` 
  - `pytest`
  - `reportlab`

---

## Testing ✅

- Nombre de la branch: **testing**
  - `test_main.py` 
  - `test_user.py` 

Pruebas relacionadas a nuestras funciones de validacion. 

---

