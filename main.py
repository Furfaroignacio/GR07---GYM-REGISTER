import json
from admin import registrarUsuario, listarMiembros, borrarMiembro, buscarMiembro, gestionarMiembro
from user import verPerfil, editarPerfil

def obtenerDNI():
    while True:
        dni_input = input("Iniciar sesión con DNI: ")
        if dni_input.isdigit() and len(dni_input) == 8:
            return int(dni_input)
        print("DNI inválido, debe contener 8 dígitos numéricos.")

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
    print("\nBienvenido al Gimnasio")
    while True:
        print("\nElige una opción:")
        print("1. Ver mi perfil")
        print("2. Editar mi perfil")
        print("0. Salir")

        opcion = input("Introduce una opción: ")
        if not opcion.isdigit():
            print("Selecciona una opción correcta.")
            continue
        
        opcion = int(opcion)
        if opcion == 1:
            verPerfil(dniRegistro)
        elif opcion == 2:
            editarPerfil(dniRegistro)
        elif opcion == 0:
            print("Hasta luego")
            break
        else:
            print("Selecciona una opción correcta.")

def menuAdministrador():
    print("\nBienvenido al sistema de registro de miembros")
    while True:
        print("\nElige una opción:")
        print("1. Registrarse")
        print("2. Lista de miembros")
        print("3. Borrar miembro")
        print("4. Buscar miembro")
        print("5. Gestionar miembros")
        print("0. Salir")

        opcion = input("Introduce una opción: ")
        if not opcion.isdigit():
            print("\nPor favor, introduce un valor numérico.")
            continue
        
        opcion = int(opcion)
        if opcion == 1:
            registrarUsuario()
        elif opcion == 2:
            listarMiembros()
        elif opcion == 3:
            borrarMiembro()
        elif opcion == 4:
            buscarMiembro()
        elif opcion == 5:
            gestionarMiembro()
        elif opcion == 0:
            print("Hasta luego")
            break
        else:
            print("Selecciona una opción correcta.")

def main():
    dniRegistro = obtenerDNI()
    rol = validarRol(dniRegistro)
    
    if rol is None:
        print("Usuario no encontrado.")
        return

    if rol == 1:
        menuUsuario(dniRegistro)
    elif rol == 2:
        menuAdministrador()
    else:
        print("Rol no reconocido.")

if __name__ == "__main__":
    main()
