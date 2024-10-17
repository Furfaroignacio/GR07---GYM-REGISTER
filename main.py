from datetime import datetime
import json
def registrarUsuario():
    nombre = input("Ingresa el nombre: ")
    validarTexto = lambda nombre: nombre.isalpha()
    if validarTexto(nombre) == False:
        print("Nombre inválido, debe contener solo letras.")
        return
    apellido = input("Ingresa el apellido: ")
    if validarTexto(apellido) == False:
        print("Apellido inválido, debe contener solo letras.")
        return
    dni = int(input("Ingresa el DNI: "))
    fecha_actual = datetime.now().strftime("%d-%m-%Y")
    validarDni = lambda dni: len(str(dni)) == 8
    if validarDni(dni):
        # ABRIMOS EL ARCHIVO JSON
        try:
            with open('usuarios.json', 'r') as archivo:
                usuarioDiccionario = json.load(archivo)
        except FileNotFoundError:
            usuarioDiccionario = []

        # si el dni ya esta en nuestra lista de usuarios, no lo registramos
        for usuario in usuarioDiccionario:
            if usuario["dni"] == dni:
                print("El DNI ya está registrado.")
                return

        # Creamos diccionario usuario
        usuario = {
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "fecha_registro": fecha_actual,
            "rol": 1,
        }

        # lo metemos al json
        usuarioDiccionario.append(usuario)

        # Guardar los datos 
        with open('usuarios.json', 'w') as archivo:
            json.dump(usuarioDiccionario, archivo, indent=4)

        print("Usuario registrado con éxito.")
    else: 
        print("DNI inválido, debe tener 8 dígitos.")

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

def validarRol(dni):
    with open('usuarios.json', 'r') as archivo:
        usuarios = json.load(archivo)
        for usuario in usuarios:
            if usuario['dni'] == dni:
                return usuario['rol']
    return None

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
                break
        else:
            print("Usuario no encontrado.")

def editarPerfil(dni):
    with open('usuarios.json', 'r') as archivo:
        usuarios = json.load(archivo)
    
    for usuario in usuarios:
        if usuario['dni'] == dni:
            print("Editar perfil:")
            usuario['nombre'] = input(f"Nombre ({usuario['nombre']}): ") or usuario['nombre']
            usuario['apellido'] = input(f"Apellido ({usuario['apellido']}): ") or usuario['apellido']
            nuevo_dni = input(f"DNI ({usuario['dni']}): ")
            usuario['dni'] = int(nuevo_dni) if nuevo_dni else usuario['dni']
            break
    else:
        print("Usuario no encontrado.")
        return

    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)
    
    print("Perfil actualizado exitosamente.")    

def menuUsuario(dniRegistro):
    print("\nBienvenido al Gimnasio")
    opcion = -1 
    while opcion != 0:
        print("\nElige una opción")
        print("1. Ver mi perfil")
        print("2. Editar mi perfil")
        print("0. Salir")

        opcion = int(input("Introduce una opción: "))
        
        if opcion == 1:
            verPerfil(dniRegistro)
        elif opcion == 2:
            editarPerfil(dniRegistro)
        elif opcion == 0:
            print("Hasta luego")
        else:
            print("Selecciona una opción correcta")

def menuAdministrador():
    print("\nBienvenido al sistema de registro de miembros")
    opcion = -1 
    while opcion != 0:
        print("\nElige una opción")
        print("1. Registrar miembro")
        print("2. Lista de miembros")
        print("3. Borrar miembro")
        print("4. Buscar miembro")
        print("0. Salir")

        opcion = int(input("Introduce una opción: "))
        
        if opcion == 1:
            registrarUsuario()
        elif opcion == 2:
            listarMiembros()
        elif opcion == 3:
            borrarMiembro()
        elif opcion == 4:
            buscarMiembro()
        elif opcion == 0:
            print("Hasta luego")
        else:
            print("Selecciona una opción correcta")


def main():
    dniRegistro = int(input("Iniciar sesión con DNI: "))
    rol = validarRol(dniRegistro)
    if rol is None:
        print("Usuario no encontrado.")
        return

    if rol == 1:
        print("Menú de Usuario:")
        menuUsuario(dniRegistro)
    elif rol == 2:
        print("Menú de Administrador:")
        menuAdministrador()
    else:
        print("Rol no reconocido.")

main()