import json
import tkinter as tk
from tkinter import messagebox
from user import verPerfil, editarPerfil, inscribirseCurso, verFacturas
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
    ventana_dni.geometry("300x150")
    ventana_dni.resizable(False, False)

    # Agregar icono a la ventana
    ventana_dni.iconbitmap(r"C:\Users\Usuario\Pictures\logogim.ico")  # Asegúrate de que el archivo icono.ico esté en la misma carpeta que tu script
    
    centrar_ventana(ventana_dni, 300, 150)
    
    # Interfaz de inicio de sesión
    frame = tk.Frame(ventana_dni, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Iniciar sesión con DNI:", font=("Arial", 12)).pack(pady=5)
    entry_dni = tk.Entry(frame, font=("Arial", 12), justify="center")
    entry_dni.pack(pady=5)
    tk.Button(frame, text="Ingresar", command=validarDNI, font=("Arial", 10), width=15).pack(pady=10)
    
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
    ventana_usuario.geometry("350x300")
    ventana_usuario.resizable(False, False)

    # Agregar icono a la ventana
    ventana_usuario.iconbitmap(r"C:\Users\Usuario\Pictures\logogim.ico")

    centrar_ventana(ventana_usuario, 350, 300)
    
    frame = tk.Frame(ventana_usuario, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Bienvenido al Gimnasio", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame, text="Ver mi perfil", command=lambda: verPerfil(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Editar mi perfil", command=lambda: editarPerfil(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Inscribirme a un curso", command=lambda: inscribirseCurso(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Ver mis facturas", command=lambda: verFacturas(dniRegistro), font=("Arial", 10), width=20).pack(pady=5)
    tk.Button(frame, text="Salir", command=ventana_usuario.destroy, font=("Arial", 10), width=20).pack(pady=5)

    ventana_usuario.mainloop()

def menuAdministrador():
    ventana_admin = tk.Tk()
    ventana_admin.title("Menú Administrador")
    ventana_admin.geometry("350x300")
    ventana_admin.resizable(False, False)

    # Agregar icono a la ventana
    ventana_admin.iconbitmap(r"C:\Users\Usuario\Pictures\logogim.ico")

    centrar_ventana(ventana_admin, 350, 300)
    
    frame = tk.Frame(ventana_admin, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Bienvenido al sistema de registro", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame, text="Registrar usuario", command=registrarUsuario, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Lista de miembros", command=listarMiembros, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Borrar miembro", command=borrarMiembro, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Buscar miembro", command=buscarMiembro, font=("Arial", 10), width=25).pack(pady=5)
    tk.Button(frame, text="Salir", command=ventana_admin.destroy, font=("Arial", 10), width=25).pack(pady=5)
    
    ventana_admin.mainloop()

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def main():
    obtenerDNI()

if __name__ == "__main__":
    main()
