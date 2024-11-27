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
from customtkinter import *



# Validar texto y DNI
def validarTexto(texto):
    return texto.isalpha()

def validarDNI(dni):
    return str(dni).isdigit() and len(str(dni)) == 8

# Mostrar perfil de usuario
def verPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            info = (
                f"Nombre: {usuario['nombre']}\n"
                f"Apellido: {usuario['apellido']}\n"
                f"DNI: {usuario['dni']}\n"
                f"Fecha de registro: {usuario['fecha_registro']}\n"
                f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}\n"
                f"Cursos inscritos: {', '.join([curso[0] for curso in usuario.get('cursos_inscritos', [])])}"
            )
            messagebox.showinfo("Perfil del usuario", info)
            return
    messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")

# Editar perfil de usuario
def editarPerfil(dni):
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
        return

    for usuario in usuarios:
        if usuario['dni'] == dni:
            nuevo_nombre = simpledialog.askstring("Editar Perfil", f"Nombre ({usuario['nombre']}):")
            while not validarTexto(nuevo_nombre):
                messagebox.showerror("Error", "Nombre inválido, debe contener solo letras.")
                nuevo_nombre = simpledialog.askstring("Editar Perfil", "Ingresa un nombre válido:")

            usuario['nombre'] = nuevo_nombre

            nuevo_apellido = simpledialog.askstring("Editar Perfil", f"Apellido ({usuario['apellido']}):")
            while not validarTexto(nuevo_apellido):
                messagebox.showerror("Error", "Apellido inválido, debe contener solo letras.")
                nuevo_apellido = simpledialog.askstring("Editar Perfil", "Ingresa un apellido válido:")

            usuario['apellido'] = nuevo_apellido
            
            nuevo_dni = simpledialog.askstring("Editar Perfil", f"DNI ({usuario['dni']}):")
            if nuevo_dni and validarDNI(nuevo_dni):
                usuario['dni'] = int(nuevo_dni)
            else:
                messagebox.showinfo("Aviso", "DNI inválido. Manteniendo el DNI anterior.")

            break
    else:
        messagebox.showwarning("Usuario no encontrado", "No se encontró un usuario con ese DNI.")
        return

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)
    
    messagebox.showinfo("Perfil actualizado", "El perfil ha sido actualizado exitosamente.")

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
    pdf_filename = f"facturas/factura_{n}_{dni}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Configuración general
    c.setFont("Helvetica-Bold", 14)
    ancho, alto = letter

    
    c.setFillColor(colors.darkblue)
    c.drawString(100, alto - 100, "Fitness Gym")
    c.setFont("Helvetica", 10)
    c.drawString(100, alto - 120, "Factura oficial")
    c.drawImage("logo/fitnessLogo.jpg", ancho - 200, alto - 150, width=100, height=100)
    
    
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
            usuario['cursos_inscritos'].append([curso[0], curso[1]])
            break
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
    ventana_facturas = CTkToplevel()
    ventana_facturas.title("Seleccionar Factura")
    ventana_facturas.iconbitmap("gym.ico")
    ventana_facturas.geometry("300x200")

    for i, archivo in enumerate(archivos_dni):
        btn_factura = CTkButton(ventana_facturas, text=f"{archivo}", command=lambda f=archivo: abrirFactura(f))
        btn_factura.pack(pady=5)

    def abrirFactura(archivo):
        archivo_seleccionado = os.path.join(carpeta_facturas, archivo)
        subprocess.Popen([archivo_seleccionado], shell=True)
        ventana_facturas.destroy()
