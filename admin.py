import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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

# Registrar un nuevo usuario
def registrarUsuario():
    def guardarUsuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        dni = entry_dni.get()
        rol = entry_rol.get()

        if not validarTexto(nombre) or not validarTexto(apellido):
            messagebox.showerror("Error", "Nombre y apellido deben contener solo letras.")
            return
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

        if any(usuario["dni"] == int(dni) for usuario in usuarioDiccionario):
            messagebox.showinfo("Info", "El DNI ya está registrado.")
            return

        usuario = {
            "nombre": nombre,
            "apellido": apellido,
            "dni": int(dni),
            "fecha_registro": datetime.now().strftime("%d-%m-%Y"),
            "rol": int(rol), # Por defecto es usuario
        }

        usuarioDiccionario.append(usuario)

        with open('usuarios.json', 'w') as archivo:
            json.dump(usuarioDiccionario, archivo, indent=4)

        messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
        ventana_registro.destroy()

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar Usuario")

    tk.Label(ventana_registro, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(ventana_registro)
    entry_nombre.grid(row=0, column=1)

    tk.Label(ventana_registro, text="Apellido:").grid(row=1, column=0)
    entry_apellido = tk.Entry(ventana_registro)
    entry_apellido.grid(row=1, column=1)

    tk.Label(ventana_registro, text="DNI:").grid(row=2, column=0)
    entry_dni = tk.Entry(ventana_registro)
    entry_dni.grid(row=2, column=1)

    tk.Label(ventana_registro, text="ROL:").grid(row=3, column=0)
    entry_rol = tk.Entry(ventana_registro)
    entry_rol.grid(row=3, column=1)

    tk.Button(ventana_registro, text="Guardar", command=guardarUsuario).grid(row=4, column=0, columnspan=2)

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
    def mostrarLista():
        rol = entry_rol.get()
        if rol not in ['1', '2']:
            messagebox.showerror("Error", "Rol inválido. Debe ser 1 o 2.")
            return

        verificarArchivoUsuarios()
        
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        lista_usuarios.delete(0, tk.END)  # Limpiar lista antes de mostrar nueva consulta

        for usuario in usuarioDiccionario:
            if int(rol) == usuario["rol"]:
                lista_usuarios.insert(tk.END, f"Nombre: {usuario['nombre']}")
                lista_usuarios.insert(tk.END, f"Apellido: {usuario['apellido']}")
                lista_usuarios.insert(tk.END, f"DNI: {usuario['dni']}")
                lista_usuarios.insert(tk.END, f"Fecha de registro: {usuario['fecha_registro']}")
                lista_usuarios.insert(tk.END, f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}")
                lista_usuarios.insert(tk.END, "")

    ventana_listar = tk.Toplevel()
    ventana_listar.title("Listar Miembros")

    tk.Label(ventana_listar, text="Rol (1 para usuario, 2 para admin):").pack()
    entry_rol = tk.Entry(ventana_listar)
    entry_rol.pack()

    lista_usuarios = tk.Listbox(ventana_listar, width=50)
    lista_usuarios.pack()

    tk.Button(ventana_listar, text="Mostrar", command=mostrarLista).pack()

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
