import json
import tkinter as tk
import datetime
from tkinter import messagebox
from user import verPerfil, editarPerfil, inscribirseCurso, verFacturas
from admin import administrarRoles, listarMiembros, borrarMiembro, buscarMiembro
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Función para centrar ventanas
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Función para cargar datos del archivo JSON
def cargar_datos():
    try:
        with open('usuarios.json', 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

# Función para guardar datos en el archivo JSON
def guardar_datos(usuarios):
    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)


# Ventana de inicio
def ventanaInicio():
    def iniciarSesion():
        ventana_inicio.destroy()
        obtenerDNI()

    def registrarse():
        ventana_inicio.destroy()
        ventanaRegistro()

    
    ventana_inicio = ttk.Window(themename="darkly")
    ventana_inicio.title("Bienvenido al Gimnasio")
    ventana_inicio.geometry("400x300")
    centrar_ventana(ventana_inicio, 400, 300)
    ventana_inicio.iconbitmap("gym.ico")
    frame = tk.Frame(ventana_inicio, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Sistema de Gestión de Gimnasio", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame, text="Iniciar Sesión", command=iniciarSesion, font=("Arial", 12), width=20).pack(pady=5)
    tk.Button(frame, text="Registrarse", command=registrarse, font=("Arial", 12), width=20).pack(pady=5)

    ventana_inicio.mainloop()

# Ventana de registro
def ventanaRegistro():
    def registrarNuevoUsuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        dni = entry_dni.get()

        if nombre and dni.isdigit() and len(dni) == 8:
            usuarios = cargar_datos()
            if any(u['dni'] == int(dni) for u in usuarios):
                messagebox.showerror("Error", "El DNI ya está registrado.")
            else:
                nuevo_usuario = {"nombre": nombre,"apellido":apellido,"dni": int(dni) ,"fecha_registro": datetime.datetime.now().strftime("%Y-%m-%d"), "rol": 1}
                usuarios.append(nuevo_usuario)
                guardar_datos(usuarios)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                ventana_registro.destroy()
                ventanaInicio()
        else:
            messagebox.showerror("Error", "Datos inválidos. Verifique el nombre y el DNI.")

    def regresar():
        ventana_registro.destroy()
        ventanaInicio()

    ventana_registro = ttk.Window(themename="darkly")
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("500x500")
    ventana_registro.iconbitmap("gym.ico")
    centrar_ventana(ventana_registro, 500, 500)

    frame = tk.Frame(ventana_registro, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Registro de Nuevo Usuario", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(frame, text="Nombre:").pack(anchor="w")
    entry_nombre = tk.Entry(frame)
    entry_nombre.pack(fill="x", pady=5)
    tk.Label(frame, text="Apellido:").pack(anchor="w")
    entry_apellido = tk.Entry(frame)
    entry_apellido.pack(fill="x", pady=5)
    tk.Label(frame, text="DNI (8 dígitos):").pack(anchor="w")
    entry_dni = tk.Entry(frame)
    entry_dni.pack(fill="x", pady=5)
    tk.Button(frame, text="Registrar", command=registrarNuevoUsuario, font=("Arial", 12), width=15).pack(pady=10)
    tk.Button(frame, text="Regresar", command=regresar, font=("Arial", 12), width=15).pack(pady=10)

    ventana_registro.mainloop()

# Obtener DNI para iniciar sesión
def obtenerDNI():
    def validarDNI():
        dni_input = entry_dni.get()
        if dni_input.isdigit() and len(dni_input) == 8:
            dni = int(dni_input)
            rol = validarRol(dni)
            if rol is not None:
                ventana_dni.destroy()
                if rol == 1 or rol == 2:
                    menuUsuario(dni)
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")
        else:
            messagebox.showerror("Error", "DNI inválido, debe contener 8 dígitos numéricos.")

    def regresar():
        ventana_dni.destroy()
        ventanaInicio()

    ventana_dni = ttk.Window(themename="darkly")
    ventana_dni.title("Iniciar sesión")
    ventana_dni.geometry("300x200")
    ventana_dni.iconbitmap("gym.ico")
    centrar_ventana(ventana_dni, 300, 200)

    frame = tk.Frame(ventana_dni, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Iniciar sesión con DNI:", font=("Arial", 12)).pack(pady=5)
    entry_dni = tk.Entry(frame, font=("Arial", 12), justify="center")
    entry_dni.pack(pady=5)
    tk.Button(frame, text="Ingresar", command=validarDNI, font=("Arial", 10), width=15).pack(pady=10)
    tk.Button(frame, text="Regresar", command=regresar, font=("Arial", 10), width=15).pack(pady=10)

    ventana_dni.mainloop()

# Validar rol de usuario
def validarRol(dni):
    usuarios = cargar_datos()
    for usuario in usuarios:
        if usuario['dni'] == dni:
            return usuario['rol']
    return None

# Menú para usuarios
def menuUsuario(dniRegistro):
    rol_usuario = validarRol(dniRegistro)  # Obtener el rol del usuario
    ventana_usuario = ttk.Window(themename="darkly")
    ventana_usuario.title("Menú Usuario")
    ventana_usuario.geometry("350x350")
    ventana_usuario.iconbitmap("gym.ico")
    centrar_ventana(ventana_usuario, 350, 350)

    frame = tk.Frame(ventana_usuario, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Bienvenido al Gimnasio", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame, text="Ver mi perfil", command=lambda: verPerfil(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Editar mi perfil", command=lambda: editarPerfil(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Inscribirme a un curso", command=lambda: inscribirseCurso(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Ver mis facturas", command=lambda: verFacturas(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)

    # Botón adicional solo para administradores
    if rol_usuario == 2:  # Verificar si el usuario es administrador
        tk.Button(frame, text="Opciones de Administrador", command=menuAdministrador, font=("Arial", 10), width=20).pack(pady=5)

    tk.Button(frame, text="Salir", command=ventana_usuario.destroy, font=("Arial", 10), width=20).pack(pady=5)
    

    ventana_usuario.mainloop()

# Menú para administradores
def menuAdministrador():
    ventana_admin = ttk.Window(themename="darkly")
    ventana_admin.title("Menú Administrador")
    ventana_admin.geometry("350x300")
    ventana_admin.iconbitmap("gym.ico")
    centrar_ventana(ventana_admin, 350, 300)

    frame = tk.Frame(ventana_admin, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Bienvenido al Menu Administrador", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame, text="Cambiar Rol", command=administrarRoles , font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Lista de miembros", command=listarMiembros, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Borrar miembro", command=borrarMiembro, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Buscar miembro", command=buscarMiembro, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Salir", command=ventana_admin.destroy, font=("Arial", 10), width=25).pack(pady=5)

    ventana_admin.mainloop()

# Función principal
def main():
    ventanaInicio()

if __name__ == "__main__":
    main()
