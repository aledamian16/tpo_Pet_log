# Ruta del archivo con los usuarios registrados
ruta_usuarios = "Archivos/Usuarios/usuariosRegistrados.txt"

def mostrar_usuarios_registrados(ruta):
    try:
        archivo = open(ruta, "r", encoding="utf-8")
        print("\n--- Lista de Usuarios Registrados ---")
        lineas = archivo.readlines()
        if not lineas:
            print("No hay usuarios registrados.")
        else:
            for i, linea in enumerate(lineas, 1):
                usuario = linea.strip().split(",")[0]
                print(f"{i}. {usuario}")
        archivo.close()
    except FileNotFoundError:
        print("El archivo de usuarios no fue encontrado.")

mostrar_usuarios_registrados(ruta_usuarios)
