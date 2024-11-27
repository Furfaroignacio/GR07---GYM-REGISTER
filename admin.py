import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Validaciones básicas
def validarTexto(texto):
    """Valida que el texto contenga solo letras."""
    return texto.isalpha()

def validarDNI(dni):
    """Valida que el DNI sea un número de 8 dígitos."""
    return dni.isdigit() and len(dni) == 8

def validarRol(rol):
    """Valida que el rol sea 1 o 2."""
    return rol in [1, 2]

def verificarArchivoUsuarios():
    """Crea el archivo `usuarios.json` si no existe."""
    try:
        with open('usuarios.json', 'r') as archivo:
            pass
    except FileNotFoundError:
        with open('usuarios.json', 'w') as archivo:
            json.dump([], archivo)

def administrarRoles():
    def cambiarRol():
        dni = entry_dni.get()
        rol = entry_rol.get()

        if not validarDNI(dni):
            messagebox.showerror("Error", "DNI inválido, debe tener 8 dígitos.")
            return
        if not validarRol(int(rol)):
            messagebox.showerror("Error", "Rol inválido. Debe ser 1 o 2.")
            return

        verificarArchivoUsuarios()
        
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        for usuario in usuarioDiccionario:
            if usuario["dni"] == int(dni):
                usuario["rol"] = int(rol)
                with open('usuarios.json', 'w') as archivo:
                    json.dump(usuarioDiccionario, archivo, indent=4)
                messagebox.showinfo("Éxito", "Rol cambiado con éxito.")
                ventana_roles.destroy()
                return

        messagebox.showinfo("Info", "Usuario no encontrado.")
        ventana_roles.destroy()

    ventana_roles = tk.Toplevel()
    ventana_roles.title("Administrar Roles")

    tk.Label(ventana_roles, text="DNI del miembro a modificar:").pack()
    entry_dni = tk.Entry(ventana_roles)
    entry_dni.pack()

    tk.Label(ventana_roles, text="Nuevo rol (1 para usuario, 2 para admin):").pack()
    entry_rol = tk.Entry(ventana_roles)
    entry_rol.pack()

    tk.Button(ventana_roles, text="Cambiar Rol", command=cambiarRol).pack()


    

# Borrar un usuario por DNI
def borrarMiembro():
    def borrar():
        dni = entry_dni.get()
        if not validarDNI(dni):
            messagebox.showerror("Error", "DNI inválido, debe tener 8 dígitos.")
            return

        verificarArchivoUsuarios()
        
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        for usuario in usuarioDiccionario:
            if usuario["dni"] == int(dni):
                usuarioDiccionario.remove(usuario)
                with open('usuarios.json', 'w') as archivo:
                    json.dump(usuarioDiccionario, archivo, indent=4)
                messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
                ventana_borrar.destroy()
                return

        messagebox.showinfo("Info", "Usuario no encontrado.")
        ventana_borrar.destroy()

    ventana_borrar = tk.Toplevel()
    ventana_borrar.title("Borrar Miembro")

    tk.Label(ventana_borrar, text="DNI del miembro a borrar:").pack()
    entry_dni = tk.Entry(ventana_borrar)
    entry_dni.pack()
    tk.Button(ventana_borrar, text="Borrar", command=borrar).pack()

# Listar usuarios por rol
def listarMiembros():
    def cargarUsuarios():
        verificarArchivoUsuarios()
        
        try:
            with open('usuarios.json', 'r') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

    def mostrarLista(usuarios):
        for row in tree.get_children():
            tree.delete(row)  # Limpiar tabla antes de mostrar nueva consulta

        for usuario in usuarios:
            tree.insert("", tk.END, values=(
                usuario['nombre'],
                usuario['apellido'],
                usuario['dni'],
                usuario['fecha_registro'],
                'Usuario' if usuario['rol'] == 1 else 'Administrador'
            ))

        # Establecer separaciones entre filas y columnas
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", borderwidth=1, relief="solid")
        style.configure("Treeview.Cell", borderwidth=1, relief="solid")

    def filtrarLista():
        rol = entry_rol.get()
        if rol not in ['1', '2']:
            messagebox.showerror("Error", "Rol inválido. Debe ser 1 o 2.")
            return

        usuarios = cargarUsuarios()
        usuarios_filtrados = [usuario for usuario in usuarios if int(rol) == usuario["rol"]]
        mostrarLista(usuarios_filtrados)

    ventana_listar = ttk.Toplevel()
    ventana_listar.title("Listar Miembros")

    ttk.Label(ventana_listar, text="Rol (1 para usuario, 2 para admin):").pack(pady=5)
    entry_rol = ttk.Entry(ventana_listar)
    entry_rol.pack(pady=5)

    columns = ("Nombre", "Apellido", "DNI", "Fecha de registro", "Rol")
    tree = ttk.Treeview(ventana_listar, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10)

    ttk.Button(ventana_listar, text="Filtrar", command=filtrarLista).pack(pady=5)

    # Cargar y mostrar todos los usuarios al iniciar la ventana
    usuarios = cargarUsuarios()
    mostrarLista(usuarios)

# Buscar usuario por DNI
def buscarMiembro():
    def buscar():
        dni = entry_dni.get()
        if not validarDNI(dni):
            messagebox.showerror("Error", "DNI inválido, debe tener 8 dígitos.")
            return

        verificarArchivoUsuarios()
        
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        for usuario in usuarioDiccionario:
            if usuario["dni"] == int(dni):
                messagebox.showinfo("Resultado", 
                                    f"Nombre: {usuario['nombre']}\n"
                                    f"Apellido: {usuario['apellido']}\n"
                                    f"DNI: {usuario['dni']}\n"
                                    f"Fecha de registro: {usuario['fecha_registro']}")
                ventana_buscar.destroy()
                return

        messagebox.showinfo("Info", "Usuario no encontrado.")
        ventana_buscar.destroy()

    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("Buscar Miembro")

    tk.Label(ventana_buscar, text="DNI del miembro a buscar:").pack()
    entry_dni = tk.Entry(ventana_buscar)
    entry_dni.pack()
    tk.Button(ventana_buscar, text="Buscar", command=buscar).pack()
