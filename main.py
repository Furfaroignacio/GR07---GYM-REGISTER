import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Funciones previas adaptadas para la interfaz gráfica
def validarRol(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
            for usuario in usuarios:
                if usuario['dni'] == dni:
                    return usuario['rol']
    except FileNotFoundError:
        return None

def verPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
            for usuario in usuarios:
                if usuario['dni'] == dni:
                    messagebox.showinfo("Perfil", f"Nombre: {usuario['nombre']}\n"
                                                  f"Apellido: {usuario['apellido']}\n"
                                                  f"DNI: {usuario['dni']}\n"
                                                  f"Fecha de registro: {usuario['fecha_registro']}\n"
                                                  f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}")
                    return
        messagebox.showerror("Error", "Usuario no encontrado.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se ha encontrado el archivo de usuarios.")

def editarPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
            for usuario in usuarios:
                if usuario['dni'] == dni:
                    ventana_editar = tk.Toplevel()
                    ventana_editar.title("Editar Perfil")

                    lbl_nombre = tk.Label(ventana_editar, text="Nombre:")
                    lbl_nombre.pack()

                    entry_nombre = tk.Entry(ventana_editar)
                    entry_nombre.insert(0, usuario['nombre'])
                    entry_nombre.pack()

                    lbl_apellido = tk.Label(ventana_editar, text="Apellido:")
                    lbl_apellido.pack()

                    entry_apellido = tk.Entry(ventana_editar)
                    entry_apellido.insert(0, usuario['apellido'])
                    entry_apellido.pack()

                    lbl_dni = tk.Label(ventana_editar, text="DNI:")
                    lbl_dni.pack()

                    entry_dni = tk.Entry(ventana_editar)
                    entry_dni.insert(0, usuario['dni'])
                    entry_dni.pack()

                    btn_guardar = tk.Button(ventana_editar, text="Guardar", command=lambda: (dni, entry_nombre.get(), entry_apellido.get(), entry_dni.get()))
                    btn_guardar.pack()

                    return
        messagebox.showerror("Error", "Usuario no encontrado.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se ha encontrado el archivo de usuarios.")

def registrarUsuario():
    # Aquí también puedes crear una ventana adicional para registrar un nuevo usuario
    pass

def listarMiembros():
    # Mostrar miembros según el rol
    pass

def borrarMiembro():
    # Aquí puedes implementar la interfaz gráfica para borrar miembros
    pass

def buscarMiembro():
    # Aquí puedes implementar la interfaz gráfica para buscar miembros
    pass

# Funciones para el menú de Usuario y Administrador con botones
def menuUsuario(dni):
    ventana_usuario = tk.Toplevel()
    ventana_usuario.title("Menú de Usuario")

    lbl_bienvenida = tk.Label(ventana_usuario, text=f"Bienvenido Usuario {dni}")
    lbl_bienvenida.pack()

    btn_ver_perfil = tk.Button(ventana_usuario, text="Ver Perfil", command=lambda: verPerfil(dni))
    btn_ver_perfil.pack()

    btn_editar_perfil = tk.Button(ventana_usuario, text="Editar Perfil", command=lambda: editarPerfil(dni))
    btn_editar_perfil.pack()

    btn_salir = tk.Button(ventana_usuario, text="Salir", command=ventana_usuario.destroy)
    btn_salir.pack()

def menuAdministrador():
    ventana_admin = tk.Toplevel()
    ventana_admin.title("Menú de Administrador")

    lbl_bienvenida = tk.Label(ventana_admin, text="Bienvenido Administrador")
    lbl_bienvenida.pack()

    btn_registrar = tk.Button(ventana_admin, text="Registrar Usuario", command=registrarUsuario)
    btn_registrar.pack()

    btn_listar = tk.Button(ventana_admin, text="Listar Miembros", command=listarMiembros)
    btn_listar.pack()

    btn_borrar = tk.Button(ventana_admin, text="Borrar Miembro", command=borrarMiembro)
    btn_borrar.pack()

    btn_buscar = tk.Button(ventana_admin, text="Buscar Miembro", command=buscarMiembro)
    btn_buscar.pack()

    btn_salir = tk.Button(ventana_admin, text="Salir", command=ventana_admin.destroy)
    btn_salir.pack()

# Ventana principal de inicio de sesión
def iniciarSesion():
    dni = int(entry_dni.get())
    rol = validarRol(dni)

    if rol is None:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return

    if rol == 1:
        menuUsuario(dni)
    elif rol == 2:
        menuAdministrador()
    else:
        messagebox.showerror("Error", "Rol no reconocido.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Registro de Gimnasio")

lbl_dni = tk.Label(ventana, text="Iniciar sesión con DNI:")
lbl_dni.pack()

entry_dni = tk.Entry(ventana)
entry_dni.pack()

btn_iniciar = tk.Button(ventana, text="Iniciar sesión", command=iniciarSesion)
btn_iniciar.pack()

btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit)
btn_salir.pack()

ventana.mainloop()
