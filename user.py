from datetime import datetime
import json

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
