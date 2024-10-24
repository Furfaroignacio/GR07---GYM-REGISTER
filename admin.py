from datetime import datetime
import json

def registrarUsuario():
    nombre_valido = False
    apellido_valido = False
    dni_valido = False
    
    # Pedir el nombre
    nombre = input("Ingresa el nombre: ")
    validarTexto = lambda nombre: nombre.isalpha()
    while nombre_valido == False:
        if validarTexto(nombre) == False:
            print("Nombre inválido, debe contener solo letras.")
            nombre = input("Ingresa el nombre: ")
        else:
            nombre_valido = True

    # Pedir el apellido
    apellido = input("Ingresa el apellido: ")
    while apellido_valido == False:
        if validarTexto(apellido) == False:
            print("Apellido inválido, debe contener solo letras.")
            apellido = input("Ingresa el apellido: ")
        else:
            apellido_valido = True
    # Pedir el DNI y validar el formato
    dni = input("Ingresa el DNI: ")
    while dni_valido == False:
        try:
            if not dni.isdigit() and len(dni) != 8:
                raise ValueError("DNI inválido, debe contener solo números y tener 8 dígitos.")
            if not dni.isdigit():
                raise ValueError("DNI inválido, debe contener solo números.")
            if len(dni) != 8:
                raise ValueError("DNI inválido, debe tener 8 dígitos.")
            
            dni_valido = True
        except ValueError as e:
            print(e)
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
    for usuario in usuarioDiccionario:
        if usuario["dni"] == dni:
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
    if opcion == 's':
        return  # Vuelve al menú principal
    elif opcion == 'n':
        print("Registro finalizado. Adiós.")
        exit()  # Termina el programa
    else:
        print("Opción inválida. Volviendo al menú principal.")
        return  # Volver al menú si la opción es incorrecta
    

def borrarMiembro():
    dni = int(input("Ingresa el DNI del miembro a borrar: "))
    validarDni = lambda dni: len(str(dni)) == 8
    if validarDni(dni):
        # ABRIMOS EL ARCHIVO JSON igual que antes
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        # Buscamos el usuario por su dni y si lo encontramos lo borramos
        for usuario in usuarioDiccionario:
            if usuario["dni"] == dni:
                usuarioDiccionario.remove(usuario)
                print("Usuario eliminado con éxito.")
                break
        else:
            print("Usuario no encontrado.")

        # Guardar los datos 
        with open('usuarios.json', 'w') as archivo:
            json.dump(usuarioDiccionario, archivo, indent=4)
    else:
        print("DNI inválido, debe tener 8 dígitos.")

def listarMiembros():
    rolBuscar = int(input("Que rol quiere mostrar (1 user, 2 admin): "))

    # ABRIMOS EL ARCHIVO JSON
    try:
        with open('usuarios.json', 'r') as archivo:
            usuarioDiccionario = json.load(archivo)
    except FileNotFoundError:
        usuarioDiccionario = []


    # Mostramos los usuarios
    for usuario in usuarioDiccionario:
        if rolBuscar == usuario["rol"]:
            print("Nombre: ", usuario["nombre"])
            print("Apellido: ", usuario["apellido"])
            print("DNI: ", usuario["dni"])
            print("Fecha de registro: ", usuario["fecha_registro"])
            print(f"Rol: {'Usuario' if usuario['rol'] == 1 else 'Administrador'}")
            print("")

def buscarMiembro():
    dni = int(input("Ingresa el DNI del miembro a buscar: "))
    validarDni = lambda dni: len(str(dni)) == 8
    validarDni(dni)
    if validarDni(dni):
        # ABRIMOS EL ARCHIVO JSON igual que antes
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        # Buscamos el usuario por su dni igual que antes, si lo encontramos lo mostramos
        for usuario in usuarioDiccionario:
            if usuario["dni"] == dni:
                print("Nombre: ", usuario["nombre"])
                print("Apellido: ", usuario["apellido"])
                print("DNI: ", usuario["dni"])
                print("Fecha de registro: ", usuario["fecha_registro"])
                break
        else:
            print("Usuario no encontrado.")

        # Guardar los datos 
        with open('usuarios.json', 'w') as archivo:
            json.dump(usuarioDiccionario, archivo, indent=4)
    else:
        print("DNI inválido, debe tener 8 dígitos.")