import json
import tkinter as tk
from tkinter import messagebox
from customtkinter import * 
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
    
    # Inicializar la ventana
    ventana_dni = CTk()  # Usamos customTkinter (CTk) en lugar de tk.Tk
    ventana_dni.title("Iniciar sesión")
    ventana_dni.geometry("350x200")
    ventana_dni.resizable(False, False)
    centrar_ventana(ventana_dni, 350, 200)

    # Frame con diseño de customTkinter
    frame = CTkFrame(ventana_dni, corner_radius=10, width=300, height=150)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Etiqueta de título
    label_titulo = CTkLabel(
        frame, text="Iniciar sesión", font=("Helvetica", 14, "bold"), text_color="white"
    )
    label_titulo.pack(pady=(10, 5))

    # Entrada de DNI
    entry_dni = CTkEntry(
        frame, font=("Arial", 12), width=200, placeholder_text="Ingrese su DNI"
    )
    entry_dni.pack(pady=5)

    # Botón de ingreso
    btn_ingresar = CTkButton(
        frame,
        text="Ingresar",
        fg_color="#475B5A",  # Color del fondo
        hover_color="#3A4746",  # Color al pasar el mouse
        font=("Arial", 12, "bold"),
        command=validarDNI
    )
    btn_ingresar.pack(pady=10)

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
    ventana_usuario = CTk()  # Usamos customTkinter (CTk) en lugar de tk.Tk()
    ventana_usuario.title("Menú Usuario")
    ventana_usuario.geometry("350x400")
    ventana_usuario.resizable(False, False)
    centrar_ventana(ventana_usuario, 350, 400)

    # Frame principal con fondo y bordes redondeados
    frame = CTkFrame(ventana_usuario, corner_radius=15, width=300, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título de bienvenida
    label_bienvenida = CTkLabel(
        frame, text="Bienvenido al Gimnasio", font=("Arial", 16, "bold"), text_color="white"
    )
    label_bienvenida.pack(pady=10)

    # Botones de navegación
    btn_perfil = CTkButton(
        frame, text="Ver mi perfil", command=lambda: verPerfil(dniRegistro), font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#4CAF50", hover_color="#45a049"
    )
    btn_perfil.pack(pady=5)

    btn_editar_perfil = CTkButton(
        frame, text="Editar mi perfil", command=lambda: editarPerfil(dniRegistro), font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#2196F3", hover_color="#1976D2"
    )
    btn_editar_perfil.pack(pady=5)

    btn_inscribirse = CTkButton(
        frame, text="Inscribirme a un curso", command=lambda: inscribirseCurso(dniRegistro), font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#FF5722", hover_color="#E64A19"
    )
    btn_inscribirse.pack(pady=5)

    btn_ver_facturas = CTkButton(
        frame, text="Ver mis facturas", command=lambda: verFacturas(dniRegistro), font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#9C27B0", hover_color="#8E24AA"
    )
    btn_ver_facturas.pack(pady=5)

    btn_salir = CTkButton(
        frame, text="Salir", command=ventana_usuario.destroy, font=("Arial", 12), width=250,
        height=40, corner_radius=8, fg_color="#9E9E9E", hover_color="#757575"
    )
    btn_salir.pack(pady=5)

    ventana_usuario.mainloop()

def menuAdministrador():
    ventana_admin = CTk()  # Usamos customTkinter (CTk) en lugar de tk.Tk()
    ventana_admin.title("Menú Administrador")
    ventana_admin.geometry("350x400")
    ventana_admin.resizable(False, False)
    centrar_ventana(ventana_admin, 350, 400)

    # Frame principal con fondo y bordes redondeados
    frame = CTkFrame(ventana_admin, corner_radius=15, width=300, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título de bienvenida
    label_bienvenida = CTkLabel(
        frame, text="Bienvenido al sistema de registro", font=("Arial", 16, "bold"), text_color="white"
    )
    label_bienvenida.pack(pady=10)

    # Botones de administración
    btn_registrar_usuario = CTkButton(
        frame, text="Registrar usuario", command=registrarUsuario, font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#4CAF50", hover_color="#45a049"
    )
    btn_registrar_usuario.pack(pady=5)

    btn_lista_miembros = CTkButton(
        frame, text="Lista de miembros", command=listarMiembros, font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#2196F3", hover_color="#1976D2"
    )
    btn_lista_miembros.pack(pady=5)

    btn_borrar_miembro = CTkButton(
        frame, text="Borrar miembro", command=borrarMiembro, font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#FF5722", hover_color="#E64A19"
    )
    btn_borrar_miembro.pack(pady=5)

    btn_buscar_miembro = CTkButton(
        frame, text="Buscar miembro", command=buscarMiembro, font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#9C27B0", hover_color="#8E24AA"
    )
    btn_buscar_miembro.pack(pady=5)

    btn_salir = CTkButton(
        frame, text="Salir", command=ventana_admin.destroy, font=("Arial", 12),
        width=250, height=40, corner_radius=8, fg_color="#9E9E9E", hover_color="#757575"
    )
    btn_salir.pack(pady=5)

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
