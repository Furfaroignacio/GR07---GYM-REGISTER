import json
import tkinter as tk
from tkinter import messagebox
from user import verPerfil, editarPerfil, inscribirseCurso
from admin import registrarUsuario, listarMiembros, borrarMiembro, buscarMiembro

def obtenerDNI():
    def validarDNI():
        dni_input = entry_dni.get()
        if dni_input.isdigit() and len(dni_input) == 8:
            dni = int(dni_input)
            rol = validarRol(dni)
            if rol is not None:
                ventana_dni.destroy()
                if rol == 1:
                    menuUsuario(dni)
                elif rol == 2:
                    menuAdministrador()
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")
        else:
            messagebox.showerror("Error", "DNI inválido, debe contener 8 dígitos numéricos.")
    
    ventana_dni = tk.Tk()
    ventana_dni.title("Iniciar sesión")
    
    tk.Label(ventana_dni, text="Iniciar sesión con DNI:").pack()
    entry_dni = tk.Entry(ventana_dni)
    entry_dni.pack()
    tk.Button(ventana_dni, text="Ingresar", command=validarDNI).pack()
    ventana_dni.mainloop()

def validarRol(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
            for usuario in usuarios:
                if usuario['dni'] == dni:
                    return usuario['rol']
    except FileNotFoundError:
        print("Archivo de usuarios no encontrado.")
    return None

def menuUsuario(dniRegistro):
    ventana_usuario = tk.Tk()
    ventana_usuario.title("Menú Usuario")
    
    def verPerfilUsuario():
        verPerfil(dniRegistro)
        
    def editarPerfilUsuario():
        editarPerfil(dniRegistro)
    
    def inscribirseCursoUsuario():
        inscribirseCurso(dniRegistro)
    
    tk.Label(ventana_usuario, text="Bienvenido al Gimnasio").pack()
    tk.Button(ventana_usuario, text="Ver mi perfil", command=verPerfilUsuario).pack()
    tk.Button(ventana_usuario, text="Editar mi perfil", command=editarPerfilUsuario).pack()
    tk.Button(ventana_usuario, text="Inscribirme a un curso", command=inscribirseCursoUsuario).pack()
    tk.Button(ventana_usuario, text="Salir", command=ventana_usuario.destroy).pack()
    ventana_usuario.mainloop()

def menuAdministrador():
    ventana_admin = tk.Tk()
    ventana_admin.title("Menú Administrador")

    tk.Label(ventana_admin, text="Bienvenido al sistema de registro de miembros").pack()
    
    tk.Button(ventana_admin, text="Registrar usuario", command=registrarUsuario).pack()
    tk.Button(ventana_admin, text="Lista de miembros", command=listarMiembros).pack()
    tk.Button(ventana_admin, text="Borrar miembro", command=borrarMiembro).pack()
    tk.Button(ventana_admin, text="Buscar miembro", command=buscarMiembro).pack()
    tk.Button(ventana_admin, text="Gestionar miembros", command=gestionarMiembro).pack()
    tk.Button(ventana_admin, text="Salir", command=ventana_admin.destroy).pack()
    
    ventana_admin.mainloop()

def main():
    obtenerDNI()

if __name__ == "__main__":
    main()
