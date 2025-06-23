import re
import json
from datetime import datetime

"""
--------------------------------------------------------------------------------------------------------
    Rutas de archivos
--------------------------------------------------------------------------------------------------------
"""
# Ruta del archivo con los usuarios registrados
ruta_usuarios = "Archivos/Usuarios/usuariosRegistrados.json"
# Ruta del archivo con las mascotas 
ruta_mascotas = "Archivos/Mascotas/Mascotas.json"
# Ruta del archivo con los dueños
ruta_duenios = "Archivos/Duenios/Duenios.json"
# Ruta del archivo con el log de auditoria
ruta_log_auditoria = "Archivos/Log/LogAuditoria.txt"
"""
--------------------------------------------------------------------------------------------------------
    Funciones para cargar y guardar los archivos JSON
--------------------------------------------------------------------------------------------------------
"""
def cargar_datos_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

mascotas = cargar_datos_json(ruta_mascotas)
duenios = cargar_datos_json(ruta_duenios)
usuarios = cargar_datos_json(ruta_usuarios)

"""
--------------------------------------------------------------------------------------------------------
    Datos Globales
--------------------------------------------------------------------------------------------------------
"""
#Tupla con los tipos de mascotas
tiposMascotas = ("Perro" , "Gato", "Ave", "Reptil", "Roedor", "Pez", "Otro")
#Tupla con los tipos de usuarios
roles_validos = ("Gerente", "Recepcionista", "Veterinario")
#Tupla con los días de la semana que trabaja la veterinaria
dias_validos = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado")

"""
--------------------------------------------------------------------------------------------------------
    Funciones de validación y normalización 
--------------------------------------------------------------------------------------------------------
"""
def validar_usuario(usuarios):
    while True:
        usuario = input("Ingrese un nombre de usuario: ").strip()
        
        if not usuario:
            print("El nombre de usuario no puede estar vacío.")
            continue
        
        if any(u["usuario"] == usuario for u in usuarios):
            print("Usuario existente. Intente otra vez.")
            continue

        return usuario

def validar_contrasenia():
    while True:
        contrasenia = input("Ingrese una contraseña: ").strip()
        if len(contrasenia) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            continue
        if not re.search(r"[A-Z]", contrasenia):
            print("La contraseña debe contener al menos una letra mayúscula.")
            continue
        if not re.search(r"[a-z]", contrasenia):
            print("La contraseña debe contener al menos una letra minúscula.")
            continue
        if not re.search(r"\d", contrasenia):
            print("La contraseña debe contener al menos un número.")
            continue
        if not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~\\-]", contrasenia):
            print("La contraseña debe contener al menos un símbolo.")
            continue
        return contrasenia

def validar_telefono():
    while True:
        telefono = input("Ingrese su número de teléfono: ").strip()
        solo_digitos = re.sub(r"[^\d]", "", telefono)
        if not re.match(r"^\+?[\d\s\-()]+$", telefono):
            print("El teléfono contiene caracteres inválidos.")
            continue
        if len(solo_digitos) < 8 or len(solo_digitos) > 15:
            print("El número de teléfono debe tener entre 8 y 15 dígitos.")
            continue
        return telefono

def validar_rol(roles_validos):
    while True:
        print("Roles disponibles:", ", ".join(roles_validos))
        rol = input("Ingrese su rol: ")
        if rol.title() in  roles_validos:
            return rol
        else:
            print("Rol inválido. Intente nuevamente.")
    
def validar_rango_horario(rango, rangos_existentes):
    patron = r"^(0[8-9]|1[0-7]):[0-5]\d-(0[8-9]|1[0-7]|18):[0-5]\d$"
    if not re.match(patron, rango):
        return False

    formato = "%H:%M"
    inicio, fin = (datetime.strptime(h, formato) for h in rango.split("-"))

    # Validar que inicio < fin
    if inicio >= fin:
        return False

    # Validar que no se superponga con rangos existentes
    for existente in rangos_existentes:
        ini_existente, fin_existente = (datetime.strptime(h, formato) for h in existente.split("-"))
        if inicio < fin_existente and fin > ini_existente:
            return False

    return True

def ordenar_rangos(rangos):
    return sorted(rangos, key=lambda r: datetime.strptime(r.split("-")[0], "%H:%M"))

def ordenar_disponibilidad(disponibilidad):

    return {dia: disponibilidad[dia] for dia in dias_validos if dia in disponibilidad}

def normalizar_dia(dia):
    tildes = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
    return dia.translate(tildes).strip().capitalize()

def validar_dia(dia, dias_validos):
    return normalizar_dia(dia) in dias_validos


"""
--------------------------------------------------------------------------------------------------------
  Funciones auxiliares y validación
--------------------------------------------------------------------------------------------------------
"""
def input_id_valido(identificador):
    while True:
        try:
            entrada = input(identificador).strip()
            if not entrada.isdigit():
                raise ValueError("Debe ingresar un número.")
            return int(entrada)
        except ValueError as e:
            print(f"Error: {e}")

def buscar_por_id(lista, id_busqueda):
    for item in lista:
        if item["id"] == id_busqueda:
            return item
    return None

def mostrar_ids_mascotas(mascotas):
    """
    Imprime en pantalla cada mascota con su ID y nombre.
    """
    if not mascotas:
        print("No hay mascotas registradas.")
        return

    print("\n--- Mascotas Registradas ---")
    for mascota in mascotas:
        print(f"ID {mascota['id']}: {mascota['nombre'].capitalize()}")
    print("----------------------------")

def mostrar_ids_duenios(duenios):
    """
    Imprime en pantalla cada dueñx con su ID y nombre.
    """
    if not duenios:
        print("No hay dueñxs registrados.")
        return
    print("\n--- Dueñxs Registrados ---")
    for d in duenios:
        print(f"ID {d['id']}: {d['nombre']}")
    print("--------------------------\n")

def input_texto_obligatorio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Este campo no puede estar vacío.")

def input_numero_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("Debe ingresar un número válido.")

def validar_correo(mensaje):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$"
    while True:
        correo = input(mensaje).strip()
        if re.match(patron, correo):
            return correo.lower()
        else:
            print("Correo electrónico inválido. Intente nuevamente.")


def validar_nombre(mensaje):
    patron = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
    while True:
        nombre = input(mensaje).strip()
        if patron.fullmatch(nombre):
            return nombre.title()
        print("Nombre inválido. Solo se permiten letras y espacios.")


def input_tipo_mascota(mensaje, tipos):
    while True:
        tipo = input(mensaje).strip().title()
        if tipo in tipos:
            return tipo
        print(f"Tipo inválido. Tipos válidos: {', '.join(tipos)}")

"""
--------------------------------------------------------------------------------------------------------
  Funciones Log Auditoría
--------------------------------------------------------------------------------------------------------
"""      
#Acá irían las funciones para que quede un registro de lo que realizan los usuarios, debería quedar guardado en el archivo de logAuditoria
def registrar_log_auditoria(usuario, accion):
    """
    Registra una línea de auditoría en el archivo LogAuditoria.txt con:
    Fecha,hora, usuario y acción realizada.
    """
    try:
        with open(ruta_log_auditoria, "a", encoding="utf-8") as log:
            fechaYhora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"{fechaYhora} - Usuario: {usuario['usuario']}: {accion}\n")
    except Exception as e:
        print(f"Error al registrar en el log de auditoría: {e}")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Eliminar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_eliminar(duenios, mascotas, usuario_logueado):
    print("""¿Qué desea eliminar?
1: Mascota
2: Dueñx""")
    opcion = input("Ingrese el número de la opción: ").strip()

    if opcion == "1":
        eliminar_mascota(mascotas, usuario_logueado)
    elif opcion == "2":
        eliminar_duenio(duenios, mascotas, usuario_logueado)
    else:
        print("Opción inválida. No se realizó ninguna acción.")
    return


def eliminar_mascota(mascotas, usuario_logueado):
    while True:
        opcion = input("Ingrese el ID de la mascota a eliminar (0 para ver la lista de mascotas): ").strip()
        if opcion == "0":
            mostrar_ids_mascotas(mascotas)
            continue
        if not opcion.isdigit():
            print("Debe ingresar un número.")
            continue

        id_mascota = int(opcion)
        eliminar_mascota_por_id(mascotas, id_mascota, usuario_logueado)
        guardar_datos_json(ruta_mascotas, mascotas)
        return


def eliminar_duenio(duenios, mascotas, usuario_logueado):
    while True:
        opcion = input("Ingrese el ID del dueñx a eliminar (0 para ver lista): ").strip()
        if opcion == "0":
            mostrar_ids_duenios(duenios)
            continue
        if not opcion.isdigit():
            print("Debe ingresar un número.")
            continue

        id_duenio = int(opcion)
        if eliminar_duenio_por_id(duenios, id_duenio, usuario_logueado):
            actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios, usuario_logueado)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        return

def eliminar_mascota_por_id(mascotas, id_mascota, usuario_logueado):
    try:
        mascota = buscar_por_id(mascotas, id_mascota)
        if mascota:
            mascotas.remove(mascota)
            print(f"La mascota {mascota['nombre']} con ID {id_mascota} ha sido eliminada exitosamente.")
            registrar_log_auditoria(usuario_logueado, f"Eliminó una mascota: {mascota['nombre']} - ID: {id_mascota}")
        else:
            print(f"No se encontró una mascota con ID {id_mascota}.")
    except Exception as e:
        print(f"Error al eliminar la mascota: {e}")

def eliminar_duenio_por_id(duenios, id_duenio, usuario_logueado):
    duenio = buscar_por_id(duenios, id_duenio)
    if duenio:
        duenios.remove(duenio)
        print(f"Dueñx {duenio['nombre']} con ID {id_duenio} ha sido eliminado exitosamente.")
        registrar_log_auditoria(usuario_logueado, f"Eliminó al dueño: {duenio['nombre']} - ID: {id_duenio}")
        return True
    else:
        print(f"No se encontró un dueñx con ID {id_duenio}.")
        return False

def actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios,usuario_logueado):
    for mascota in mascotas:
        if id_duenio in mascota["dueños"]:
            mascota["dueños"].remove(id_duenio)
            print(f"Se quitó el dueñx {id_duenio} de la mascota '{mascota['nombre']}'.")

            if not mascota["dueños"]:
                resultado = mascota_sin_duenio(mascota, mascotas, duenios, usuario_logueado)
                if resultado == "eliminada":
                    continue  # Saltea esta mascota, ya fue eliminada


def mascota_sin_duenio(mascota, mascotas, duenios, usuario_logueado):
    print(f"\nADVERTENCIA - La mascota '{mascota['nombre']}' se quedó sin dueñx.")
    print("¿Qué desea hacer?")
    print("1: Eliminar la mascota")
    print("2: Asignar nuevo dueñx")

    while True:
        opcion = input("Seleccione una opción (1 o 2): ").strip()
        if opcion == "1":
            eliminar_mascota_por_id(mascotas, mascota["id"], usuario_logueado)
            return "\nMascota eliminada"
        elif opcion == "2":
            nuevo_duenio = agregar_duenio(duenios, mascotas, usuario_logueado)
            mascota["dueños"].append(nuevo_duenio["id"])
            print(f"Se asignó un nuevo dueñx a '{mascota['nombre']}'.")
            return
        else:
            print("Opción inválida. Intente nuevamente.")
"""
--------------------------------------------------------------------------------------------------------
  Funciones para añadir visita médica
--------------------------------------------------------------------------------------------------------
"""
def registrar_visita(mascotas, usuario_logueado):
    try:
        while True:
            id_mascota = input_id_valido("Ingrese el ID de la mascota (0 para ver lista de IDs): ")
            if id_mascota == 0:
                mostrar_ids_mascotas(mascotas)
                continue
            break  # ID válido distinto de 0

        mascota = buscar_por_id(mascotas, id_mascota)
        if mascota:
            visita = crear_visita(usuario_logueado)
            mascota.setdefault("historial", []).append(visita)
            guardar_datos_json(ruta_mascotas, mascotas)
            print(f"\n=== Visita registrada exitosamente para {mascota['nombre']}. ===\n")
        else:
            print("No se encontró una mascota con ese ID.\n")

    except Exception as e:
        print(f"Ocurrió un error al registrar la visita: {e}\n")


def crear_visita(usuario_logueado):
    fecha = datetime.now().strftime("%d/%m/%Y")
    motivo = input_texto_obligatorio("Ingrese el motivo de la consulta: ").title()
    diagnostico = input_texto_obligatorio("Ingrese el diagnóstico: ").title()
    tratamiento = input_texto_obligatorio("Ingrese el tratamiento indicado: ").title()
    return [
        f"Fecha: {fecha}",
        f"Motivo: {motivo}",
        f"Diagnóstico: {diagnostico}",
        f"Tratamiento: {tratamiento}",
        f"Empleado: {usuario_logueado['nombre']}",
        f"Rol: {usuario_logueado['rol']}"
    ]
            
"""
--------------------------------------------------------------------------------------------------------
  Funciones para agregar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_agregar(mascotas, duenios, tipos_mascotas,usuario_logueado):
    print("""\n--- Menú Agregar ---
                1: Agregar dueñx
                2: Agregar mascota
                3: Volver al menú principal""")
    
    while True:
        try:
            opcion = int(input("MENÚ AGREGAR - Seleccione una opción: "))
        except ValueError:
            print("Debe ingresar un número válido.")
            continue

        if opcion == 1:
            agregar_duenio(duenios, mascotas,usuario_logueado)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        elif opcion == 2:
            agregar_mascota(mascotas, duenios, tipos_mascotas,usuario_logueado)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        elif opcion == 3:
            return # Volver al menú principal
        else:
            print("Opción inválida.")

#Función donde generamos el id a asignarle a la nueva Mascota/Dueñx
def generar_id(lista):
    if not lista: #En caso de que la lista este vacía le asignamos el id 1
        return 1
    else:
        #Recorremos la lista para buscar el id más alto y le sumamos 1
        return max(item["id"] for item in lista) + 1
    
def agregar_duenio(duenios, mascotas,usuario_logueado):
    nuevo_id = generar_id(duenios)
    print("\n=== Agregar Dueñx ===")
    nombre = validar_nombre("Nombre del dueñx: ").title()
    telefono = input_numero_entero("Teléfono (solo números): ")
    email = validar_correo("Correo electrónico: ")


    duenio = {
        "id": nuevo_id,
        "nombre": nombre,
        "telefono": telefono,
        "mail": email
    }
    duenios.append(duenio)
    print(f"Dueñx '{nombre}' agregado con ID {nuevo_id}.\n")
    registrar_log_auditoria(usuario_logueado, f"Agregó un nuevo dueñx: {nombre} - ID: {nuevo_id}")
    # Asociar a mascota
    if mascotas:
        opcion = input("¿Desea asociar este nuevo dueñx a una mascota existente? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            asociar_duenio_a_mascota(nuevo_id, mascotas)

    return duenio

def agregar_mascota(mascotas, duenios, tipos_mascotas,usuario_logueado):
    nuevo_id = generar_id(mascotas)
    print("\n=== Agregar Mascota ===")
    nombre = validar_nombre("Nombre de la mascota: ").title()
    tipo = input_tipo_mascota("Tipo de mascota: ", tipos_mascotas)
    edad = input_numero_entero("Edad de la mascota: ")

    mascota = {
        "id": nuevo_id,
        "nombre": nombre,
        "tipo": tipo,
        "edad": edad,
        "dueños": [],
        "historial": []
    }
    mascotas.append(mascota)
    print(f"Mascota '{nombre}' agregada con ID {nuevo_id}.")
    registrar_log_auditoria(usuario_logueado, f"Agregó una nueva mascota: {nombre} - ID: {nuevo_id}")

    # Asociar a dueñx
    if duenios:
        opcion = input("¿Desea asociar esta mascota a un dueñx existente? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            asociar_mascota_a_duenio(nuevo_id, duenios, mascotas)

    return mascota

def asociar_duenio_a_mascota(id_duenio, mascotas):
    if not mascotas:
        print("No hay mascotas registradas.")
        return

    while True:
        id_input = input("Ingrese el ID de la mascota a asociar (0 para ver lista): ").strip()
        if id_input == "0":
            mostrar_ids_mascotas(mascotas)
            continue
        if not id_input.isdigit():
            print("Debe ingresar un número válido.")
            continue
        
        id_mascota = int(id_input)
        mascota = buscar_por_id(mascotas, id_mascota)

        if mascota:
            mascota["dueños"].append(id_duenio)
            print(f"Dueñx asociado correctamente a la mascota '{mascota['nombre']}'.")
            return
        else:
            print("Mascota no encontrada.")

def asociar_mascota_a_duenio(id_mascota, duenios, mascotas):
    if not duenios:
        print("No hay dueñxs registrados.")
        return

    while True:
        id_input = input("Ingrese el ID del dueñx a asociar (0 para ver lista): ").strip()
        if id_input == "0":
            mostrar_ids_duenios(duenios)
            continue
        if not id_input.isdigit():
            print("Debe ingresar un número válido.")
            continue

        id_duenio = int(id_input)
        duenio = buscar_por_id(duenios, id_duenio)
        mascota = buscar_por_id(mascotas, id_mascota)

        if duenio and mascota:
            if id_duenio not in mascota["dueños"]:
                mascota["dueños"].append(id_duenio)
                print(f"Mascota asociada correctamente a {duenio['nombre']}.")
            else:
                print(f"La mascota ya está asociada al dueñx {duenio['nombre']}.")
            return
        else:
            print("Dueñx o mascota no encontrados.")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Modificar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""

#Función para realizar la búsqueda de ID (Sirve tanto para Mascotas como para Dueñxs)
def busqueda_de_id(datosUsuarios):
    if not datosUsuarios:
        print("No hay registros disponibles.")
        return None

    while True:
        entrada = input("Ingrese el ID del individuo a editar (0 para ver lista): ").strip()

        if entrada == "0":
            if "tipo" in datosUsuarios[0]:
                mostrar_ids_mascotas(datosUsuarios)
            else:
                mostrar_ids_duenios(datosUsuarios)
            continue

        if not entrada.isdigit():
            print("Debe ingresar un número válido.")
            continue

        id_buscado = int(entrada)

        for individuo in datosUsuarios:
            if individuo["id"] == id_buscado:
                return id_buscado

        print("ID no encontrado. Intente nuevamente.")


#Función para realizar el cambio de ID (Sirve tanto para Mascotas como para Dueñxs)
def cambio_de_id(individuo, datosUsuarios):
    ids_existentes = set(map(lambda x: x["id"], datosUsuarios))

    while True:
        try:
            nuevo_id = int(input("Seleccione nuevo ID: "))
        except ValueError:
            print("Debe ingresar un número válido.")
            continue

        if nuevo_id == individuo["id"]:
            print("El nuevo ID es igual al actual. Ingrese uno diferente.")
            continue

        if nuevo_id in ids_existentes:
            print("Ese ID ya está en uso. Intente con otro.")
        else:
            individuo["id"] = nuevo_id
            print("ID actualizado correctamente.")
            return

#Función para realizar el cambio de nombre
def cambioNombre(individuo):
    nuevoNombre = input("ingresar nombre: ")
    nombreSinEspacios=nuevoNombre.replace(" ","") 
    while not nombreSinEspacios.isalpha(): # en caso de tener caracter numerico vuelve solicitar el nombre
        print("Nombre inválido: solo letras")
        nuevoNombre = input("ingresar nombre valido: ")
        nombreSinEspacios=nuevoNombre.replace(" ","")
    individuo["nombre"] = nuevoNombre.title()
    return individuo

#Función para mostrar los datos de una mascota
def muestraDatosMascota(mascota):
    nombresDuenios = [duenio["nombre"] for duenio in duenios if duenio["id"] in mascota["dueños"]]

    print(f"ID: {mascota['id']}")
    print(f"Nombre: {mascota['nombre']}")
    print(f"Tipo: {mascota['tipo']}")
    print(f"Edad: {mascota['edad']} años")
    print(f"Dueñx/s: {' - '.join(nombresDuenios)}")
    print("----------------------------------------")

#Función para mostrar los datos de un dueño
def muestraDatosDuenios(duenio):
        mascotasDuenio = [mascota["nombre"] for mascota in mascotas if duenio["id"] in mascota["dueños"]]
        
        print("--- Persona ---")
        print(f"ID: {duenio['id']}")
        print(f"Nombre: {duenio['nombre']}")
        print("--- Contacto ---")
        print(f"Teléfono: {duenio['telefono']}")
        print(f"Mail: {duenio['mail']}")
        print("--- Mascotas ---")
        print(f"Mascotas: {' - '.join(mascotasDuenio)}")
        print("----------------------------------------")

#Menú modificar información: Mascota y/o Dueñx
def  modificarInformacion(mascotas, duenios, usuario_logueado, tiposMascotas,ruta_mascotas, ruta_duenios):
    while True:
        print("""\n--- Consultar Información ---\n
1: Modificar datos mascotas\n
2: Modificar datos dueños\n
3: Volver al menú principal""")
        opcion = int(input("\nIngresar opción deseada: "))

        if opcion == 1:
            editarDatosMascotas(mascotas, usuario_logueado, tiposMascotas, ruta_mascotas)
        if opcion == 2:
            editarDatosDuenio(duenios, usuario_logueado,ruta_duenios)
        if opcion == 3:
            #volver al menu principal
            return True

#Función para modificar los datos de las mascotas     
def editarDatosMascotas(mascotas, usuario_logueado,tiposMascotas,ruta_mascotas):

    idMascotaEncontrada = busqueda_de_id(mascotas)
    mascota = buscar_por_id(mascotas, idMascotaEncontrada)

    if not mascota:
        print("Mascota no encontrada.")
        return
    
    print("----------------------------------------")
    print("\n--- Datos de la mascota seleccionada ---")
    muestraDatosMascota(mascota)
    print("----------------------------------------")

    while True:
        print("""--- Seleccione atributo a editar: ---\n
1: ID\n
2: Nombre\n
3: Tipo\n
4: Edad\n
0: Finalizar Sesión
--------------------------------------""")
        try:
            opcion =int(input("Seleccione opcion: "))
        except ValueError:
            print("Error - Debe ingresar una opción válida (1, 2, 3, 4 o 0).")
            continue
            
        if opcion == 0:
            print("Edición finalizada.")
            break

        elif opcion == 1:
            cambio_de_id(mascota, mascotas)
                        
        elif opcion == 2:
            cambioNombre(mascota)
        elif opcion == 3:
            editar_tipo_mascota(mascota, tiposMascotas)
            
        elif opcion == 4:
            editar_edad_mascota(mascota)
        
        else:
            print("Opción inválida.")
            continue
    
        muestraDatosMascota(mascota)

    guardar_datos_json(ruta_mascotas, mascotas)
    registrar_log_auditoria(usuario_logueado, f"Modificó datos de la mascota '{mascota['nombre']}' (ID {mascota['id']})")
    return

#Función para editar el tipo de mascota
def editar_tipo_mascota(mascota,tiposMascotas):
    
    print("\n--- Tipos de mascotas disponibles ---")
    for tipo in tiposMascotas:
        print(f"- {tipo}")
    print("------------------------------------\n")

    tipo = input_tipo_mascota("Nuevo tipo: ", tiposMascotas)
    mascota["tipo"] = tipo
    print("Tipo actualizado correctamente.")

#Función para editar la edad de la mascota
def editar_edad_mascota(mascota):
    edad = input_numero_entero("Nueva edad: ")
    mascota["edad"] = edad
    print("Edad actualizada correctamente.")

#Función para modificar los datos de los dueños 
def editarDatosDuenio(duenios, usuario_logueado, ruta_duenios):
    idDuenioEncontrado = busqueda_de_id(duenios)
    duenio = buscar_por_id(duenios, idDuenioEncontrado)
    if not duenio:
        print("Dueñx no encontrado.")
        return
    print("----------------------------------------")
    print("\n--- Datos del dueñx seleccionado ---")
    muestraDatosDuenios(duenio)
    print("----------------------------------------")
    
    while True:
        print("""--- Seleccione atributo a editar: ---\n
1: ID\n
2: Nombre\n
3: Teléfono\n
4: Mail\n
0: Finalizar Sesión\n
--------------------------------------""")
        try:
            opcion =int(input("Seleccione opcion: "))
        except ValueError:
            print("Error - Debe ingresar una opción válida (1, 2, 3, 4 o 0).")
            continue

        if opcion == 0:
            print("Edición finalizada.")
            break

        elif opcion == 1: #para cambiar el id se corrobora que no se encuentre entre los existentes
            cambio_de_id(duenio, duenios)    
        
        elif opcion == 2:
            cambioNombre(duenio)
        
        elif opcion == 3:
            duenio["telefono"] = validar_telefono()
            print("Teléfono actualizado correctamente.")
        #cambio mail
        elif opcion == 4:
            duenio["mail"] = validar_correo("Nuevo correo: ")
            print("Correo actualizado correctamente.")
        else:
            print("Opción inválida. Intente nuevamente.")
                                        
        #mascotasDuenio = [mascota["nombre"] for mascota in mascotas if duenio["id"] in mascota["dueños"]]#utilizamos listas por comprension para mostras nombres de las mascotas
        muestraDatosDuenios(duenio)

    guardar_datos_json(ruta_duenios, duenios)
    registrar_log_auditoria(usuario_logueado, f"Modificó datos del dueñx '{duenio['nombre']}' (ID {duenio['id']})")
    return


"""
--------------------------------------------------------------------------------------------------------
  Funciones de Consulta
--------------------------------------------------------------------------------------------------------
"""
#Menú de consulta de Información
def consultarInformacion(mascotas, duenios):
    while True:
        print("""\n--- Consultar Información ---\n
1: Ver todas las mascotas\n
2: Ver todos los dueños\n
3: Buscar mascota por nombre\n
4: Buscar dueño por nombre\n
5: Ver Historial de mascota\n
6: Buscar en historial de mascota\n
7: Volver al menú principal""")


        opcionConsulta = input("Seleccione una opción: ")

        if opcionConsulta == "1":
            mostrarTodasLasMascotas(mascotas, duenios)
        elif opcionConsulta == "2":
            mostrarTodosLosDuenios(mascotas, duenios)
        elif opcionConsulta == "3":
            buscarMascotaPorNombre(mascotas, duenios)
        elif opcionConsulta == "4":
            buscarDuenioPorNombre(mascotas, duenios)
        elif opcionConsulta == "5":
            MenuHistorialMascota(mascotas)
        elif opcionConsulta == "6":
            busqueda_en_historial(mascotas)
        elif opcionConsulta == "7":
            return # Volvemos al menú principal
        else:
            print("Opción inválida. Intente nuevamente.")

#Función mostrar todas las mascotas en la lista de mascotas
def mostrarTodasLasMascotas(mascotas, duenios):
    """
    Lista todas las mascotas con sus datos y dueñxs.
    """
    if not mascotas:
        print("No hay mascotas registradas.")
        return
    print("\n--- Lista de Todas las Mascotas ---")
    for mascota in mascotas:
        nombres_duenio = [duenio['nombre'] for duenio in duenios if duenio['id'] in mascota['dueños']]
        print(f"ID: {mascota['id']}")
        print(f"Nombre: {mascota['nombre']}")
        print(f"Tipo: {mascota['tipo']}")
        print(f"Edad: {mascota['edad']} años")
        print(f"Dueñx/s: {' - '.join(nombres_duenio)}")
        print("----------------------------------")

#Función para mostrar todos los dueños de la lista de diccionarios "duenios"
def mostrarTodosLosDuenios(mascotas, duenios):
    """
    Lista todos los dueñxs con sus datos y mascotas asociadas.
    """
    if not duenios:
        print("No hay dueñxs registrados.")
        return
    print("\n--- Lista de Todos los Dueñxs ---")
    for duenio in duenios:
        mascotas_duenio = [mascota['nombre'] for mascota in mascotas if duenio['id'] in mascota['dueños']]
        print(f"ID: {duenio['id']}")
        print(f"Nombre: {duenio['nombre']}")
        print(f"Teléfono: {duenio['telefono']}")
        print(f"Mail: {duenio['mail']}")
        print(f"Mascotas: {' - '.join(mascotas_duenio)}")
        print("----------------------------------")


#Función para buscar las mascotas por nombre (Devuelve todas las coincidencias con ese nombre)
def buscarMascotaPorNombre(mascotas, duenios):
    """
    Busca mascotas cuyo nombre contenga el criterio.
    Muestra sus datos y todo el historial.
    """
    criterio = input_texto_obligatorio("Ingrese el nombre de la mascota a buscar: ").title()
    mascotas_encontradas = [m for m in mascotas if criterio in m['nombre'].title()]
    if not mascotas_encontradas:
        print("No se encontraron mascotas con ese nombre.")
        return
    for mascota in mascotas_encontradas:
        nombres_duenios = [duenio['nombre'] for duenio in duenios if duenio['id'] in mascota['dueños']]
        print("\n--- Mascota ---")
        print(f"ID: {mascota['id']}")
        print(f"Nombre: {mascota['nombre']}")
        print(f"Tipo: {mascota['tipo']}")
        print(f"Edad: {mascota['edad']} años")
        print("Historial Médico:")
        for fila in mascota['historial']:
            print(" - ".join(fila))
        print(f"Dueñx/s: {' - '.join(nombres_duenios)}")
        print("----------------------------------")

#Función para buscar los dueños por nombre (Devuelve todas las coincidencias con ese nombre)
def buscarDuenioPorNombre(mascotas, duenios):
    """
    Busca dueñx por nombre exacto.
    Muestra sus datos y mascotas asociadas.
    """
    criterio = input_texto_obligatorio("Ingrese el nombre del dueñx a buscar: ").title()
    duenios_encontrados = [duenio for duenio in duenios if criterio == duenio['nombre'].title()]
    if not duenios_encontrados:
        print("No se encontraron dueñxs con ese nombre.")
        return
    for duenio in duenios_encontrados:
        mascotas_duenio = [mascota['nombre'] for mascota in mascotas if duenio['id'] in mascota['dueños']]
        print("\n--- Dueñx ---")
        print(f"ID: {duenio['id']}")
        print(f"Nombre: {duenio['nombre']}")
        print(f"Teléfono: {duenio['telefono']}")
        print(f"Mail: {duenio['mail']}")
        print(f"Mascotas: {' - '.join(mascotas_duenio)}")
        print("----------------------------------")

def MenuHistorialMascota(mascotas):
    """
    Menú para ver historial completo o últimas 10 visitas.
    """
    while True:
        print("""
--- Consultar Historial ---
1: Ver todo el historial de la mascota
2: Ver últimas 10 visitas a la veterinaria
3: Volver al menú principal
""")
        opcion = input_numero_entero("Seleccione una opción: ")
        if opcion == 1:
            mostrarHistorialMascota(mascotas)
        elif opcion == 2:
            mostrarUltimasDiezVisitas(mascotas)
        elif opcion == 3:
            return
        else:
            print("Opción inválida. Intente nuevamente.")


#Función para buscar el historial médico de la mascota
def mostrarHistorialMascota(mascotas):
    """
    Muestra todo el historial de una mascota dada su ID.
    0 muestra IDs disponibles.
    """
    if not mascotas:
        print("No hay mascotas registradas.")
        return
    
    while True:
        id_mascota = input_id_valido("Ingrese el ID de la mascota (0 para ver lista): ")
        if id_mascota == 0:
            mostrar_ids_mascotas(mascotas)
            continue
        break

    mascota = buscar_por_id(mascotas, id_mascota)
    if mascota:
        print(f"\nHistorial de {mascota['nombre']}:")
        if len(mascota["historial"]) > 0:
            for fila in mascota["historial"]:
                print(" - ".join(fila))
        else:
            print("Sin visitas registradas.")
        print()
    else:
        print("No se encontró la mascota.")

#Función para buscar las últimas 10 visitas médicas de la mascota
def mostrarUltimasDiezVisitas(mascotas):
    """
    Muestra las últimas 10 visitas de una mascota dada su ID.
    0 muestra IDs disponibles.
    """
    if not mascotas:
        print("No hay mascotas registradas.")
        return

    while True:
        id_mascota = input_id_valido("Ingrese el ID de la mascota (0 para ver lista): ")
        if id_mascota == 0:
            mostrar_ids_mascotas(mascotas)
            continue
        break

    mascota = buscar_por_id(mascotas, id_mascota)
    if mascota:
        print(f"\nÚltimas 10 visitas de {mascota['nombre']}:")
        if mascota["historial"]:
            ultimas = mascota["historial"][-10:]
            for fila in ultimas:
                print(" - ".join(fila))
        else:
            print("Sin visitas registradas.")
        print()
    else:
        print("No se encontró la mascota.")


#Filtros de historial médico de la mascota
def extraer_campo(fila, campo):
    return next(
        (item.split(":", 1)[1].strip() for item in fila if item.lower().startswith(campo.lower() + ":")),
        ""
    )

def filtrar_historial_por_motivo(historial):
    motivos_disponibles = sorted(set(extraer_campo(h, "Motivo") for h in historial))
    print("Motivos disponibles:", ", ".join(motivos_disponibles))
    motivo = input("Ingrese motivo exacto: ").strip().title()
    return list(filter(lambda h: extraer_campo(h, "Motivo") == motivo, historial))

def filtrar_historial_por_fecha(historial):
    fecha = input("Ingrese fecha (dd/mm/yyyy): ").strip()
    return list(filter(lambda h: extraer_campo(h, "Fecha") == fecha, historial))

def filtrar_historial_por_empleado(historial):
    nombres_disponibles = sorted(set(extraer_campo(h, "Empleado") for h in historial))
    print("Veterinarios disponibles:", ", ".join(nombres_disponibles))
    nombre = input("Ingrese nombre del veterinario: ").strip().title()
    return list(filter(lambda h: extraer_campo(h, "Empleado") == nombre, historial))

def busqueda_en_historial(mascotas):
    historial = [registro for mascota in mascotas for registro in mascota.get("historial", [])]
    if not historial:
        print("No hay historial registrado.")
        return

    filtros_usados = set()

    print("""\n--- Filtros disponibles ---
1: Por fecha
2: Por motivo
3: Por nombre de veterinario
0: Finalizar búsqueda
""")

    while len(filtros_usados) < 3:
        try:
            opcion = int(input("Seleccione una opción de filtro (0 para salir): "))
        except ValueError:
            print("Debe ingresar un número.")
            continue

        if opcion == 0:
            break
        if opcion in filtros_usados:
            print("Ese filtro ya fue usado. Elija otro.")
            continue

        if opcion == 1:
            historial = filtrar_historial_por_fecha(historial)
        elif opcion == 2:
            historial = filtrar_historial_por_motivo(historial)
        elif opcion == 3:
            historial = filtrar_historial_por_empleado(historial)
        else:
            print("Opción inválida.")
            continue

        filtros_usados.add(opcion)

        print(f"\nResultados actuales ({len(historial)}):")
        for fila in historial:
            print(" - ".join(fila))

    print("\n--- Fin de búsqueda ---")

"""
--------------------------------------------------------------------------------------------------------
Funciones de Log In y Sign Up
--------------------------------------------------------------------------------------------------------
"""
def iniciar_sesion(usuarios):
    print("\n--- Iniciar Sesión ---")
    intentos = 0
    while intentos < 3:
        usuario_input = input("\nUsuario: ").strip()
        clave_input = input("Contraseña: ").strip()
        for usuario in usuarios:
            if usuario["usuario"] == usuario_input and usuario["clave"] == clave_input:
                print(f"\nBienvenido, {usuario['nombre']} ({usuario['rol']})")
                return usuario
        intentos += 1
        print(f"Usuario o clave incorrectos. Intentos restantes: {3 - intentos}")
    print("\nAcceso denegado. Excediste el número de intentos.")
    return None


def ingresar_disponibilidad(dias_validos):
    print("Ingrese la disponibilidad del usuario (deje el día vacío para terminar).")
    disponibilidad = {}
    while True:
        dia = input("Día (ej. lunes): ").strip()
        if dia == "":
            break

        dia_normalizado = normalizar_dia(dia)

        if not validar_dia(dia, dias_validos):
            print("Día inválido. Intente nuevamente.")
            continue

        rangos_actuales = disponibilidad.get(dia_normalizado, [])
        disponibilidad[dia_normalizado] = pedir_rangos_para_dia(dia_normalizado, rangos_actuales)

    return ordenar_disponibilidad(disponibilidad)

def pedir_rangos_para_dia(dia, rangos_existentes):
    nuevos_rangos = []
    print(f"Ingrese los horarios para {dia} (ej. 08:00-12:00, 14:00-18:00). Enter para finalizar.")
    while True:
        entrada = input(f"Horarios para {dia}: ").strip()
        if entrada == "":
            break
        rangos = [r.strip() for r in entrada.split(",") if r.strip()]
        for r in rangos:
            if validar_rango_horario(r, rangos_existentes + nuevos_rangos):
                nuevos_rangos.append(r)
            else:
                print(f"Rango inválido o solapado: {r}")
    return ordenar_rangos(rangos_existentes + nuevos_rangos)


def crear_usuario(ruta_usuarios, usuarios, roles_validos):
    print("\n--- Registrar Nuevo Usuario ---")
    nuevo_usuario = {}
    nuevo_usuario["usuario"] = validar_usuario(usuarios)
    nuevo_usuario["clave"] = validar_contrasenia()
    nuevo_usuario["nombre"] = validar_nombre("Ingrese su nombre:")
    nuevo_usuario["telefono"] = validar_telefono()
    nuevo_usuario["correo"] = validar_correo("Correo electrónico: ")
    nuevo_usuario["rol"] = validar_rol(roles_validos)
    nuevo_usuario["disponibilidad"] = ingresar_disponibilidad(dias_validos)
    usuarios.append(nuevo_usuario)
    guardar_datos_json(ruta_usuarios, usuarios)
    print("Usuario creado exitosamente.")
    print(json.dumps(nuevo_usuario, indent=4, ensure_ascii=False)) #mostrar nuevo usuario

def buscar_usuario_por_nombre(usuarios):
    usuario_input = input("Ingrese su nombre de usuario: ").strip()
    for usuario in usuarios:
        if usuario["usuario"] == usuario_input:
            return usuario
    print("Usuario no encontrado.")
    return None

def cambiar_contrasenia(usuarios, ruta_usuarios):
    usuario = buscar_usuario_por_nombre(usuarios)

    if not usuario:
        print("Usuario no encontrado.")
        return

    intentos = 3
    while intentos > 0:
        actual = input("Ingrese su contraseña actual: ").strip()
        if actual == usuario["clave"]:
            nueva = validar_contrasenia()
            confirmar = input("Confirme la nueva contraseña: ").strip()
            if nueva == confirmar:
                usuario["clave"] = nueva
                guardar_datos_json(ruta_usuarios, usuarios)
                print("Contraseña actualizada exitosamente - Volviendo al menú de inicio\n")
                return
            else:
                print("Las contraseñas no coinciden. Intente nuevamente.")
                return
        else:
            intentos -= 1
            print(f"Contraseña incorrecta. Intentos restantes: {intentos}")

    print("Se superó el número de intentos permitidos - Volviendo al menú de inicio\n")
    return

"""
--------------------------------------------------------------------------------------------------------
MENU - PROGRAMA PRINCIPAL
--------------------------------------------------------------------------------------------------------
"""
def menuPrincipal(mascotas, duenios, tiposMascotas, usuario_logueado, ruta_mascotas, ruta_duenios):
    salir = False
    while not salir:
        print("\n=== Menú Principal ===")
        print("""--- Seleccione una opción: ---\n
  1: Consultar Mascota y/o Dueñx\n
  2: Modificar Mascota y/o Dueñx\n
  3: Agregar Mascota y/o Dueñx\n
  4: Eliminar Mascota y/o Dueñx\n
  5: Registrar nueva visita médica\n
  0: Finalizar Sesión\n""")

        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                print("Ha seleccionado Consultar Mascota y/o Dueñx")
                consultarInformacion(mascotas, duenios)
            elif opcion == 2:
                print("Ha seleccionado Modificar Mascota y/o Dueñx")
                modificarInformacion(mascotas, duenios, usuario_logueado, tiposMascotas, ruta_mascotas, ruta_duenios)
            elif opcion == 3:
                print("Ha seleccionado Agregar Nueva Mascota y/o Dueñx")
                menu_agregar(mascotas, duenios, tiposMascotas, usuario_logueado)
            elif opcion == 4:
                print("Ha seleccionado Eliminar Mascota y/o Dueñx")
                menu_eliminar(duenios, mascotas, usuario_logueado)
            elif opcion == 5:
                print("Ha seleccionado Registrar nueva visita médica")
                registrar_visita(mascotas,usuario_logueado)
            elif opcion == 0:
                print("Sesión Finalizada.")
                salir = True
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Error - Debe ingresar una opción válida (1 , 2, 3, 4, 5 o 0).")
"""
--------------------------------------------------------------------------------------------------------
MENU - Log In / Sign Up
--------------------------------------------------------------------------------------------------------
"""
def menu_inicio(mascotas , duenios, usuarios, tiposMascotas, roles_validos, ruta_usuarios , ruta_mascotas , ruta_duenios):

    print("""===== ¡Bienvenido! =====\n
1. Iniciar sesión\n
2. Registrarse\n
3. Cambiar contraseña\n
0. Salir\n""")

    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                usuario_logueado = iniciar_sesion(usuarios)
                if usuario_logueado:
                    menuPrincipal(mascotas, duenios, tiposMascotas, usuario_logueado,ruta_mascotas, ruta_duenios)
            elif opcion == 2:
                crear_usuario(ruta_usuarios, usuarios, roles_validos)
            elif opcion == 3:
                cambiar_contrasenia(usuarios, ruta_usuarios)
            elif opcion == 0:
                print("Cerrando programa.....")
                return False
            else:
                print("Opción inválida.")
        except ValueError:
            print("Debe ingresar un número.")


#Encabezado en ASCII PetLog
print(r"""
                  _____     _   _                   /^-----^\
       /\_/\     |  __ \   | | | |                  V  o o  V
  /\  / o o \    | |__) |__| |_| |     ___   __ _    |  Y  |
 //\\ \~(*)~/    |  ___/ _ \ __| |    / _ \ / _` |    \ Q /
 `  \/   ^ /     | |  |  __/ |_| |___| (_) | (_| |    / - \
    | \|| ||     |_|   \___|\__|______\___/ \__, |    |    \
    \ '|| ||                                 __/ |    |     \     )
     \)()-())                               |___/     || (___\====
""")
menu_inicio(mascotas , duenios, usuarios, tiposMascotas, roles_validos, ruta_usuarios , ruta_mascotas , ruta_duenios)