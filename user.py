from datetime import datetime
import json
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import tkinter as tk
from tkinter import messagebox, simpledialog , filedialog
import os
import subprocess


# Validar texto y DNI
def validarTexto(texto):
    return texto.isalpha()

def validarDNI(dni):
    return str(dni).isdigit() and len(str(dni)) == 8

# Mostrar perfil de usuario
import customtkinter as ctk
import json
from tkinter import messagebox

def verPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            # Creamos una ventana emergente personalizada
            ventana_perfil = ctk.CTkToplevel()
            ventana_perfil.title("Perfil del Usuario")
            ventana_perfil.geometry("350x350")
            ventana_perfil.resizable(False, False)

            # Creamos el frame para contener la información
            frame = ctk.CTkFrame(ventana_perfil, corner_radius=10, width=300, height=300, 
                                 fg_color=("white"), border_color="#A5C8F3", border_width=2)
            frame.pack(pady=10, padx=10)

            # Información del perfil
            info = (
                f"Nombre: {usuario['nombre']}\n"
                f"Apellido: {usuario['apellido']}\n"
                f"DNI: {usuario['dni']}\n"
                f"Fecha de registro: {usuario['fecha_registro']}\n"
                f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}\n"
                f"Cursos inscritos: {', '.join([curso[0] for curso in usuario.get('cursos_inscritos', [])])}"
            )

            label_info = ctk.CTkLabel(frame, text=info, font=("Arial", 12), anchor="w", justify="left", text_color="black", 
                                      fg_color="white")
            label_info.pack(pady=10)

            # Botón para cerrar con color claro y borde redondeado
            btn_cerrar = ctk.CTkButton(frame, text="Cerrar", command=ventana_perfil.destroy, font=("Arial", 12), 
                                       width=20, corner_radius=8, fg_color="#57A6C0", hover_color="#3B86A3", text_color="white")
            btn_cerrar.pack(pady=5)

            ventana_perfil.mainloop()
            return

    # Si el usuario no es encontrado
    messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")    
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            # Creamos una ventana emergente personalizada
            ventana_perfil = ctk.CTkToplevel()
            ventana_perfil.title("Perfil del Usuario")
            ventana_perfil.geometry("350x350")
            ventana_perfil.resizable(False, False)

            # Creamos el frame para contener la información
            frame = ctk.CTkFrame(ventana_perfil, corner_radius=10, width=300, height=300)
            frame.pack(pady=10, padx=10)

            # Información del perfil
            info = (
                f"Nombre: {usuario['nombre']}\n"
                f"Apellido: {usuario['apellido']}\n"
                f"DNI: {usuario['dni']}\n"
                f"Fecha de registro: {usuario['fecha_registro']}\n"
                f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}\n"
                f"Cursos inscritos: {', '.join([curso[0] for curso in usuario.get('cursos_inscritos', [])])}"
            )

            label_info = ctk.CTkLabel(frame, text=info, font=("Arial", 12), anchor="w", justify="left", text_color="black")
            label_info.pack(pady=10)

            # Botón para cerrar
            btn_cerrar = ctk.CTkButton(frame, text="Cerrar", command=ventana_perfil.destroy, font=("Arial", 12), width=20)
            btn_cerrar.pack(pady=5)

            ventana_perfil.mainloop()
            return

    # Si el usuario no es encontrado
    messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")


def editarPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            # Crear una ventana emergente para editar el perfil con customTkinter
            ventana_editar = ctk.CTkToplevel()
            ventana_editar.title("Editar Perfil")
            ventana_editar.geometry("400x350")
            ventana_editar.resizable(False, False)

            # Frame para los campos de texto
            frame = ctk.CTkFrame(ventana_editar, width=350, height=300, corner_radius=10, fg_color="white")
            frame.pack(pady=10, padx=10)

            # Campos de entrada para editar nombre, apellido y DNI
            nuevo_nombre = ctk.CTkEntry(frame, placeholder_text=f"Nombre ({usuario['nombre']})", font=("Arial", 12))
            nuevo_nombre.pack(pady=5)
            nuevo_apellido = ctk.CTkEntry(frame, placeholder_text=f"Apellido ({usuario['apellido']})", font=("Arial", 12))
            nuevo_apellido.pack(pady=5)
            nuevo_dni = ctk.CTkEntry(frame, placeholder_text=f"DNI ({usuario['dni']})", font=("Arial", 12))
            nuevo_dni.pack(pady=5)

            # Función para guardar los cambios
            def guardarCambios():
                # Validar y actualizar nombre
                nombre = nuevo_nombre.get()
                while not validarTexto(nombre):
                    messagebox.showerror("Error", "El nombre debe contener solo letras.")
                    nombre = simpledialog.askstring("Editar Perfil", "Ingrese un nombre válido:")
                usuario['nombre'] = nombre

                # Validar y actualizar apellido
                apellido = nuevo_apellido.get()
                while not validarTexto(apellido):
                    messagebox.showerror("Error", "El apellido debe contener solo letras.")
                    apellido = simpledialog.askstring("Editar Perfil", "Ingrese un apellido válido:")
                usuario['apellido'] = apellido

                # Validar y actualizar DNI
                dni_input = nuevo_dni.get()
                if dni_input and validarDNI(dni_input):
                    usuario['dni'] = int(dni_input)
                else:
                    messagebox.showinfo("Aviso", "DNI inválido. Manteniendo el DNI anterior.")

                # Guardar cambios en el archivo
                with open('usuarios.json', 'w') as archivo:
                    json.dump(usuarios, archivo, indent=4)

                messagebox.showinfo("Perfil actualizado", "El perfil ha sido actualizado exitosamente.")
                ventana_editar.destroy()

            # Botón para guardar los cambios
            btn_guardar = ctk.CTkButton(frame, text="Guardar cambios", command=guardarCambios, font=("Arial", 12), width=20)
            btn_guardar.pack(pady=10)

            # Botón para cerrar sin guardar
            btn_cancelar = ctk.CTkButton(frame, text="Cancelar", command=ventana_editar.destroy, font=("Arial", 12), width=20)
            btn_cancelar.pack(pady=5)

            ventana_editar.mainloop()
            return

    messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")

def inscribirseCurso(dni):
    cursos = [
        ["Crossfit", 7000],
        ["Yoga", 3000],
        ["Entrenamiento Funcional", 7000],
        ["Pilates", 4000],
        ["Boxeo", 6000],
        ["Spinning", 3500],
        ["Zumba", 2500]
    ]

    curso_nombres = [f"{curso[0]} - ${curso[1]}" for curso in cursos]
    opcion = simpledialog.askinteger("Inscribirse en Curso", f"Selecciona el número del curso:\n" + "\n".join([f"{i + 1}. {curso}" for i, curso in enumerate(curso_nombres)]))

    # Verifica si se seleccionó una opción válida o si se canceló
    if opcion is None:
        return  # Salir de la función si se presionó "Cancelar"
    
    if 1 <= opcion <= len(cursos):
        curso_seleccionado = cursos[opcion - 1]
        messagebox.showinfo("Inscripción exitosa", f"Te has inscrito en {curso_seleccionado[0]}. Generando factura...")
        generarFactura(dni, curso_seleccionado)
        agregarCursoAlPerfil(dni, curso_seleccionado)
    else:
        messagebox.showerror("Error", "Selección inválida.")


# Generar factura
def generarFactura(dni, curso):
    n = random.randint(1000, 9999)
    carpeta_facturas = "facturas"
    if not os.path.exists(carpeta_facturas):
        os.makedirs(carpeta_facturas)  # Crear la carpeta si no existe
    
    pdf_filename = os.path.join(carpeta_facturas, f"factura_{n}_{dni}.pdf")
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Configuración general
    c.setFont("Helvetica-Bold", 14)
    ancho, alto = letter

    
    c.setFillColor(colors.darkblue)
    c.drawString(100, alto - 100, "Fitness Gym")
    c.setFont("Helvetica", 10)
    c.drawString(100, alto - 120, "Factura oficial")
    c.drawImage("fitnessLogo.jpg", ancho - 200, alto - 150, width=100, height=100)
    
    
    c.setStrokeColor(colors.grey)
    c.line(50, alto - 140, ancho - 50, alto - 140)

    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(100, alto - 160, f"Cliente DNI: {dni}")
    c.drawString(100, alto - 180, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(100, alto - 220, "Detalles del curso:")
    c.setFont("Helvetica", 10)
    c.drawString(120, alto - 240, f"- Nombre: {curso[0]}")
    c.drawString(120, alto - 260, f"- Precio: ${curso[1]}")

    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.red)
    c.drawString(100, alto - 300, f"Total a pagar: ${curso[1]}")

    
    c.setStrokeColor(colors.grey)
    c.line(50, 50, ancho - 50, 50)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawString(50, 30, "Gracias por su preferencia - Fitness Gym")

    
    c.save()
    messagebox.showinfo("Factura generada", f"Factura generada: factura_{n}_{dni}.pdf")


# Agregar curso al perfil
def agregarCursoAlPerfil(dni, curso):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            if 'cursos_inscritos' not in usuario:
                usuario['cursos_inscritos'] = []
            # Evitar agregar el mismo curso más de una vez
            if not any(curso[0] == c[0] for c in usuario['cursos_inscritos']):
                usuario['cursos_inscritos'].append([curso[0], curso[1]])
                break
            else:
                messagebox.showwarning("Curso ya inscrito", f"Ya estás inscrito en el curso {curso[0]}.")
                return

    else:
        messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")
        return

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)

    messagebox.showinfo("Curso agregado", f"El curso {curso[0]} ha sido agregado a tu perfil.")

def verFacturas(dni):
    carpeta_facturas = "facturas"
    if not os.path.exists(carpeta_facturas):
        messagebox.showerror("Error", "La carpeta de facturas no existe.")
        return

    archivos_dni = [archivo for archivo in os.listdir(carpeta_facturas) if archivo.endswith(f"_{dni}.pdf")]

    if not archivos_dni:
        messagebox.showinfo("Sin facturas", f"No se encontraron facturas asociadas al DNI {dni}.")
        return

    # Crear una ventana emergente con botones para cada factura
    ventana_facturas = ctk.CTkToplevel()
    ventana_facturas.title("Seleccionar Factura")
    ventana_facturas.geometry("300x200")

    for i, archivo in enumerate(archivos_dni):
        btn_factura = ctk.CTkButton(ventana_facturas, text=f"{archivo}", command=lambda f=archivo: abrirFactura(f))
        btn_factura.pack(pady=5)

    def abrirFactura(archivo):
        archivo_seleccionado = os.path.join(carpeta_facturas, archivo)
        subprocess.Popen([archivo_seleccionado], shell=True)
        ventana_facturas.destroy()
