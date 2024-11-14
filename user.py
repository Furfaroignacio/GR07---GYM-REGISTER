from datetime import datetime
import json
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def validarTexto(texto):
    """Valida que el texto contenga solo letras."""
    return texto.isalpha()

def validarDNI(dni):
    """Valida que el DNI sea un número de 8 dígitos."""
    return str(dni).isdigit() and len(str(dni)) == 8

def verPerfil(dni):
    with open('usuarios.json', 'r') as archivo:
        usuarios = json.load(archivo)
        for usuario in usuarios:
            if usuario['dni'] == dni:
                print("Nombre: ", usuario["nombre"])
                print("Apellido: ", usuario["apellido"])
                print("DNI: ", usuario["dni"])
                print("Fecha de registro: ", usuario["fecha_registro"])
                print(f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}")
                print(f"Cursos inscritos: {', '.join([curso[0] for curso in usuario.get('cursos_inscritos', [])])}")
                break
        else:
            print("Usuario no encontrado.")

def editarPerfil(dni):
    with open('usuarios.json', 'r') as archivo:
        usuarios = json.load(archivo)

    for usuario in usuarios:
        if usuario['dni'] == dni:
            print("Editar perfil:")
            nuevo_nombre = input(f"Nombre ({usuario['nombre']}): ")
            while not validarTexto(nuevo_nombre):
                print("Nombre inválido, debe contener solo letras.")
                nuevo_nombre = input("Ingresa un nombre válido: ")
            usuario['nombre'] = nuevo_nombre

            nuevo_apellido = input(f"Apellido ({usuario['apellido']}): ")
            while not validarTexto(nuevo_apellido):
                print("Apellido inválido, debe contener solo letras.")
                nuevo_apellido = input("Ingresa un apellido válido: ")
            usuario['apellido'] = nuevo_apellido
            
            nuevo_dni = input(f"DNI ({usuario['dni']}): ")
            if nuevo_dni and validarDNI(nuevo_dni):
                usuario['dni'] = int(nuevo_dni)
            else:
                print("DNI inválido. Manteniendo el DNI anterior.")

            break
    else:
        print("Usuario no encontrado.")
        return

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)
    
    print("Perfil actualizado exitosamente.")

def inscribirseCurso(dni):
    # Curso, costo matriz
    cursos = [
        ["Crossfit", 7000],
        ["Yoga", 3000],
        ["Entrenamiento Funcional", 7000],
        ["Pilates", 4000],
        ["Boxeo", 6000],
        ["Spinning", 3500],
        ["Zumba", 2500]
    ]
    
    print("Cursos disponibles:")
    for i, curso in enumerate(cursos):
        print(f"{i + 1}. {curso[0]} - ${curso[1]}")

    opcion = input("Selecciona el número del curso al que deseas inscribirte: ")
    
    if not opcion.isdigit() or int(opcion) not in range(1, len(cursos) + 1):
        print("Selección inválida.")
        return
    
    curso_seleccionado = cursos[int(opcion) - 1]
    print(f"Te has inscrito en {curso_seleccionado[0]}. Generando factura...")

    generarFactura(dni, curso_seleccionado)  
    agregarCursoAlPerfil(dni, curso_seleccionado)
    
def generarFactura(dni, curso):
    n = random.randint(1000, 9999)
    
    # Crear el nombre del archivo PDF
    pdf_filename = f"facturas/factura_{n}_{dni}.pdf"
    
    # Crear un objeto Canvas para el PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Definir las posiciones y el contenido
    c.setFont("Helvetica", 12)
    
    # Escribir el contenido de la factura
    c.drawString(100, 750, f"Factura para el DNI: {dni}")
    c.drawString(100, 730, f"Curso: {curso[0]}")  # nombre del curso
    c.drawString(100, 710, f"Total a pagar: ${curso[1]}")  # costo del curso
    c.drawString(100, 690, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Guardar el archivo PDF
    c.save()
    
    print(f"Factura generada: {pdf_filename}")

def agregarCursoAlPerfil(dni, curso):
    """Agrega el curso seleccionado al perfil del usuario en el archivo JSON en formato de matriz."""
    with open('usuarios.json', 'r') as archivo:
        usuarios = json.load(archivo)

    for usuario in usuarios:
        if usuario['dni'] == dni:
            if 'cursos_inscritos' not in usuario:
                usuario['cursos_inscritos'] = []
            # agregar el curso como una lista [nombre, costo]
            usuario['cursos_inscritos'].append([curso[0], curso[1]])
            break
    else:
        print("Usuario no encontrado.")
        return

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)

    print(f"El curso {curso[0]} ha sido agregado a tu perfil.")
