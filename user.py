from datetime import datetime
import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

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

# Inscribirse a un curso
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

    if opcion and 1 <= opcion <= len(cursos):
        curso_seleccionado = cursos[opcion - 1]
        messagebox.showinfo("Inscripción exitosa", f"Te has inscrito en {curso_seleccionado[0]}. Generando factura...")
        generarFactura(dni, curso_seleccionado)
        agregarCursoAlPerfil(dni, curso_seleccionado)
    else:
        messagebox.showerror("Error", "Selección inválida.")

# Generar factura
def generarFactura(dni, curso):
    n = random.randint(1000, 9999)
    with open(f"facturas/factura_{n}_{dni}.txt", 'w') as factura:
        factura.write(f"Factura para el DNI: {dni}\n")
        factura.write(f"Curso: {curso[0]}\n")
        factura.write(f"Total a pagar: ${curso[1]}\n")
        factura.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    messagebox.showinfo("Factura generada", f"Factura generada: factura_{n}_{dni}.txt")

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

