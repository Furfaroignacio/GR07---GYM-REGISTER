import json
from datetime import datetime

def validarTexto(texto):
    """Valida que el texto contenga solo letras."""
    return texto.isalpha()

def validarDNI(dni):
    """Valida que el DNI sea un número de 8 dígitos."""
    return str(dni).isdigit() and len(str(dni)) == 8

def registrarUsuario():
    nombre = input("Ingresa el nombre: ")
    while not validarTexto(nombre):
        print("Nombre inválido, debe contener solo letras.")
        nombre = input("Ingresa el nombre: ")

    apellido = input("Ingresa el apellido: ")
    while not validarTexto(apellido):
        print("Apellido inválido, debe contener solo letras.")
        apellido = input("Ingresa el apellido: ")

    dni = input("Ingresa el DNI: ")
    while not validarDNI(dni):
        print("DNI inválido, debe contener solo números y tener 8 dígitos.")
        dni = input("Ingresa el DNI: ")
    dni = int(dni)

    # Registrar la fecha actual
    fecha_actual = datetime.now().strftime("%d-%m-%Y")

    # Abrir el archivo JSON o crear uno si no existe
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarioDiccionario = json.load(archivo)
    except FileNotFoundError:
        usuarioDiccionario = []

    # Verificar si el DNI ya está registrado
    if any(usuario["dni"] == dni for usuario in usuarioDiccionario):
        print("El DNI ya está registrado.")
        return  # Salir de la función si ya existe el DNI

    # Crear el diccionario del usuario
    usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "fecha_registro": fecha_actual,
        "rol": 1,  # Asignar rol por defecto como usuario
    }

    # Agregar el nuevo usuario al diccionario
    usuarioDiccionario.append(usuario)

    # Guardar los datos en el archivo JSON
    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarioDiccionario, archivo, indent=4)

    print("Usuario registrado con éxito.")

    # Ofrecer la opción de volver al menú o finalizar
    opcion = input("¿Deseas volver al menú principal? (s/n): ").lower()
    if opcion == 'n':
        print("Registro finalizado. Adiós.")
        exit()  # Termina el programa
    else:
        print("Volviendo al menú principal...")

def borrarMiembro():
    dni = input("Ingresa el DNI del miembro a borrar: ")
    if not validarDNI(dni):
        print("DNI inválido, debe tener 8 dígitos.")
        return
    dni = int(dni)

    try:
        with open('usuarios.json', 'r') as archivo:
            usuarioDiccionario = json.load(archivo)
    except FileNotFoundError:
        usuarioDiccionario = []

    for usuario in usuarioDiccionario:
        if usuario["dni"] == dni:
            usuarioDiccionario.remove(usuario)
            print("Usuario eliminado con éxito.")
            break
    else:
        print("Usuario no encontrado.")

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarioDiccionario, archivo, indent=4)

def listarMiembros():
    rolBuscar = input("¿Qué rol quieres mostrar (1 para usuario, 2 para admin)? ")
    if not rolBuscar.isdigit() or rolBuscar not in ['1', '2']:
        print("Rol inválido. Debe ser 1 o 2.")
        return

    rolBuscar = int(rolBuscar)

    try:
        with open('usuarios.json', 'r') as archivo:
            usuarioDiccionario = json.load(archivo)
    except FileNotFoundError:
        usuarioDiccionario = []

    for usuario in usuarioDiccionario:
        if rolBuscar == usuario["rol"]:
            print("Nombre: ", usuario["nombre"])
            print("Apellido: ", usuario["apellido"])
            print("DNI: ", usuario["dni"])
            print("Fecha de registro: ", usuario["fecha_registro"])
            print(f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}")
            print("")

def buscarMiembro():
    dni = input("Ingresa el DNI del miembro a buscar: ")
    if not validarDNI(dni):
        print("DNI inválido, debe tener 8 dígitos.")
        return
    dni = int(dni)

    try:
        with open('usuarios.json', 'r') as archivo:
            usuarioDiccionario = json.load(archivo)
    except FileNotFoundError:
        usuarioDiccionario = []

    for usuario in usuarioDiccionario:
        if usuario["dni"] == dni:
            print("Nombre: ", usuario["nombre"])
            print("Apellido: ", usuario["apellido"])
            print("DNI: ", usuario["dni"])
            print("Fecha de registro: ", usuario["fecha_registro"])
            break
    else:
        print("Usuario no encontrado.")
