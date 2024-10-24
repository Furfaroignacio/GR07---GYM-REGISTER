import tkinter as tk
from tkinter import messagebox
from admin import registrarUsuario, listarMiembros, borrarMiembro, buscarMiembro
from user import verPerfil, editarPerfil
import json

def validarRol(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
            for usuario in usuarios:
                if usuario['dni'] == dni:
                    return usuario['rol']
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
    return None

def iniciarSesion():
    dni = dni_entry.get()
    try:
        dni = int(dni)
    except ValueError:
        messagebox.showerror("Error", "DNI inválido.")
        return

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

def menuUsuario(dni):
    # Crea menú para usuarios
    clear_window()
    tk.Label(root, text="Menú de Usuario", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(root, text="Ver mi perfil", command=lambda: verPerfil(dni)).pack(pady=10)
    tk.Button(root, text="Editar mi perfil", command=lambda: editarPerfil(dni)).pack(pady=10)
    tk.Button(root, text="Salir", command=root.quit).pack(pady=10)

def menuAdministrador():
    # Crea menú para administradores
    clear_window()
    tk.Label(root, text="Menú de Administrador", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(root, text="Registrar usuario", command=registrarUsuario).pack(pady=10)
    tk.Button(root, text="Listar miembros", command=listarMiembros).pack(pady=10)
    tk.Button(root, text="Borrar miembro", command=borrarMiembro).pack(pady=10)
    tk.Button(root, text="Buscar miembro", command=buscarMiembro).pack(pady=10)
    tk.Button(root, text="Salir", command=root.quit).pack(pady=10)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    # Ventana principal de la aplicación
    root = tk.Tk()
    root.title("Sistema del Gimnasio")

    # Interfaz de inicio de sesión
    tk.Label(root, text="Bienvenido al Gimnasio", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(root, text="DNI:").pack()
    dni_entry = tk.Entry(root)
    dni_entry.pack(pady=10)
    tk.Button(root, text="Iniciar sesión", command=iniciarSesion).pack(pady=10)

    root.mainloop()
