import re
import json
from datetime import datetime
import unicodedata #normalizar texto

"""
--------------------------------------------------------------------------------------------------------
    Rutas de archivos
--------------------------------------------------------------------------------------------------------
"""
# Ruta del archivo con los usuarios
ruta_usuarios = "Archivos/Usuarios/Usuarios.json"
# Ruta del archivo con las mascotas 
ruta_mascotas = "Archivos/Mascotas/Mascotas.json"
# Ruta del archivo con los dueños
ruta_duenios = "Archivos/Duenios/Duenios.json"
# Ruta del archivo con el log de auditoria
ruta_log_auditoria = "Archivos/Log/LogAuditoria.txt"
# Ruta del archivo con el calendario
ruta_calendario = "Archivos/Calendario/Calendario.json"
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
calendario = cargar_datos_json(ruta_calendario)

"""
--------------------------------------------------------------------------------------------------------
  Datos Globales
--------------------------------------------------------------------------------------------------------
"""
#Tupla con los tipos de mascotas
tiposMascotas = ("Perro" , "Gato", "Ave", "Reptil", "Roedor", "Pez", "Otro")
#Tupla con los tipos de usuarios
roles_validos = ("Gerente", "Recepcionista", "Veterinario")
usuario_actual = None
#Tupla con los días de la semana que trabaja la veterinaria
dias_validos = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado")

# --------------------------------------------------------------------------------------------------------
# Funciones de validación y normalización 
# --------------------------------------------------------------------------------------------------------
def validar_usuario(usuarios):
    while True:
        usuario = input("Ingrese un nombre de usuario: ").strip()
        if not any(u["usuario"] == usuario for u in usuarios):
            return usuario
        else:
            print("Usuario existente. Intente otra vez.")

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

def validar_nombre():
    while True:
        nombre = input("Ingrese su nombre y apellido: ").strip()
        partes = nombre.split()
        if len(partes) < 2:
            print("Debe ingresar al menos nombre y apellido.")
            continue
        if all(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$", p) for p in partes):
            return nombre.title()
        else:
            print("El nombre solo debe contener letras (sin números ni símbolos).")

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

def validar_correo():
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$"
    while True:
        correo = input("Ingrese su correo electrónico: ").strip()
        if re.match(patron, correo):
            return correo.lower()
        else:
            print("Correo electrónico inválido. Intente nuevamente.")

def validar_rol():
    global roles_validos
    while True:
        print("Roles disponibles:", ", ".join(roles_validos))
        rol = input("Ingrese su rol: ")
        rol_limpio = limpiar_texto(rol)
        if rol_limpio in  roles_validos:
            return rol_limpio
        else:
            print("Rol inválido. Intente nuevamente.")

def limpiar_texto(texto):

    texto_limpio = texto.strip().lower()
    texto_limpio = ''.join(c for c in unicodedata.normalize('NFD', texto_limpio) if unicodedata.category(c) != 'Mn')#normalize  á => a ´ , category limpia y solo deja las letras
    return texto_limpio.title()
    
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

"""
--------------------------------------------------------------------------------------------------------
  Funciones auxiliares y validación
--------------------------------------------------------------------------------------------------------
"""

def muestraDatosMascota(mascota):
    nombresDuenios = [duenio["nombre"] for duenio in duenios if duenio["id"] in mascota["dueños"]]

    print(f"ID: {mascota['id']}")
    print(f"Nombre: {mascota['nombre']}")
    print(f"Tipo: {mascota['tipo']}")
    print(f"Edad: {mascota['edad']} años")
    print(f"Dueñx/s: {' - '.join(nombresDuenios)}")
    print("----------------------------------")


# ae podria usar lambda
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
        print("----------------------------------")

def input_id_valido(identificador):
    while True:
        try:
            entrada = identificador.strip()
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

def input_email_valido(mensaje):
    while True:
        email = input(mensaje).strip()
        if "@" in email and "." in email:
            return email
        print("Correo electrónico inválido.")

def input_nombre_valido(mensaje):
    patron = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
    while True:
        nombre = input(mensaje).strip()
        if patron.fullmatch(nombre):
            return nombre
        print("Nombre inválido. Solo letras y espacios son permitidos.")

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
            log.write(f"{fechaYhora} - {usuario}: {accion}\n")
    except Exception as e:
        print(f"Error al registrar en el log de auditoría: {e}")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Eliminar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_eliminar(duenios, mascotas,usuario_logueado):
    print("""¿Qué desea eliminar?
    1: Mascota
    2: Dueñx""")
    opcion = input("Ingrese el número de la opción: ").strip()

    if opcion == "1":
        id_mascota = input("Ingrese el ID de la mascota a eliminar: ")
        id_mascota = input_id_valido(id_mascota)
        eliminar_mascota_por_id(mascotas, id_mascota, usuario_logueado)
        guardar_datos_json(ruta_mascotas, mascotas)

    elif opcion == "2":
        id_duenio = input("Ingrese el ID del dueñx a eliminar: ")
        id_duenio = input_id_valido(id_duenio)
        if eliminar_duenio_por_id(duenios, id_duenio, usuario_logueado):
            actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
    else:
        print("Opción inválida. No se realizó ninguna acción.")

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

def actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios):
    for mascota in mascotas:
        if id_duenio in mascota["dueños"]:
            mascota["dueños"].remove(id_duenio)
            print(f"Se quitó el dueñx {id_duenio} de la mascota '{mascota['nombre']}'.")

            if not mascota["dueños"]:
                print(f"La mascota '{mascota['nombre']}' se quedó sin dueñx.")
                nuevo_duenio = agregar_duenio(duenios, mascotas)
                mascota["dueños"].append(nuevo_duenio["id"])
                print(f"Se asignó un nuevo dueñx a '{mascota['nombre']}'.")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para añadir visita médica
--------------------------------------------------------------------------------------------------------
"""
def registrar_visita(mascotas, usuario_logueado):
    try:
        id_valido = False
        while not id_valido:
            id_input = input("Ingrese el ID de la mascota (0 para ver lista de IDs): ").strip()
            id_mascota = input_id_valido(id_input)
            if id_mascota == 0:
                mostrar_ids_mascotas(mascotas)
            else:
                id_valido = True

        mascota = buscar_por_id(mascotas, id_mascota)
        if mascota:
            visita = crear_visita(usuario_logueado)
            mascota.setdefault("historial", []).append(visita)
            guardar_datos_json(ruta_mascotas, mascotas)
            print(f"Visita registrada exitosamente para {mascota['nombre']}.\n")
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
        f"Veterinario: {usuario_logueado}"
    ]
            
"""
--------------------------------------------------------------------------------------------------------
  Funciones para agregar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_agregar(mascotas, duenios, tipos_mascotas,usuario_logueado):
    while True:
        print("""\n--- Menú Agregar ---
                1: Agregar dueñx
                2: Agregar mascota
                3: Volver al menú principal""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_duenio(duenios, mascotas,usuario_logueado)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        elif opcion == "2":
            agregar_mascota(mascotas, duenios, tipos_mascotas,usuario_logueado)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        elif opcion == "3":
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

    nombre = input_nombre_valido("Nombre del dueñx: ").title()
    telefono = input_numero_entero("Teléfono (solo números): ")
    email = input_email_valido("Correo electrónico: ")


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
        opcion = input("¿Desea asociar este nuevo dueñx a una mascota? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            asociar_duenio_a_mascota(nuevo_id, mascotas)

    return duenio

def agregar_mascota(mascotas, duenios, tipos_mascotas,usuario_logueado):
    nuevo_id = generar_id(mascotas)

    nombre = input_texto_obligatorio("Nombre de la mascota: ").title()
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

    id_mascota = input_numero_entero("Ingrese el ID de la mascota a asociar: ")
    mascota = buscar_por_id(mascotas, id_mascota)

    if mascota:
        mascota["dueños"].append(id_duenio)
        print(f"Dueñx asociado correctamente a la mascota '{mascota['nombre']}'.")
    else:
        print("Mascota no encontrada.")

def asociar_mascota_a_duenio(id_mascota, duenios, mascotas):
    if not duenios:
        print("No hay dueñxs registrados.")
        return

    print("Dueñxs disponibles:")
    for d in duenios:
        print(f"ID {d['id']}: {d['nombre']}")

    id_duenio = input_numero_entero("Ingrese el ID del dueñx a asociar: ")
    duenio = buscar_por_id(duenios, id_duenio)
    mascota = buscar_por_id(mascotas, id_mascota)

    if duenio and mascota:
        mascota["dueños"].append(id_duenio)
        print(f"Mascota asociada correctamente a {duenio['nombre']}.")
    else:
        print("Dueñx o mascota no encontrados.")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Modificar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
#reutilizacion de cambio de ID
def cambioDeId(individuo, datosUsuarios):
    flag = False
    while flag !=True:
        nuevoId=int(input("seleccione nuevo ID: "))
        while not str(nuevoId).isnumeric():
            nuevoId= int(input("Ingrese el ID correctamente:"))
        setIdUsuarios=set(map(lambda x:x["id"],datosUsuarios))

        if nuevoId not in setIdUsuarios:
            individuo["id"] = nuevoId
            flag = True
            return individuo

def seleccionar_elemento_por_id(lista, mostrar_func):
    mostrar_func(lista)
    id_valido = input_id_valido(input("Ingrese el ID: "))
    elemento = buscar_por_id(lista, id_valido)
    if not elemento:
        print("ID no encontrado.")
    return elemento

def modificarInformacion(mascotas, duenios, usuario_logueado):
    while True:
        print("""\n--- Modificar Información ---\n
1: Modificar datos de mascota
2: Modificar datos de dueñx
3: Volver al menú principal""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            editar_mascota(mascotas, usuario_logueado)
        elif opcion == "2":
            editar_duenio(duenios, usuario_logueado)
        elif opcion == "3":
            return
        else:
            print("Opción inválida.")

def editar_mascota(mascotas, usuario_logueado):
    mascota = seleccionar_elemento_por_id(mascotas, mostrar_ids_mascotas)
    if not mascota:
        return

    while True:
        opcion = menu_edicion_mascota(mascota)
        if opcion == "0":
            break
        procesar_opcion_edicion_mascota(opcion, mascota, mascotas)

    guardar_datos_json(ruta_mascotas, mascotas)
    registrar_log_auditoria(usuario_logueado, f"Modificó mascota ID {mascota['id']}")
    print("Cambios guardados.")

def menu_edicion_mascota(mascota):
    print(f"""\n--- Editar Mascota: {mascota['nombre']} ---
1: Cambiar ID
2: Cambiar nombre
3: Cambiar tipo
4: Cambiar edad
0: Finalizar edición""")
    return input("Seleccione una opción: ").strip()

def procesar_opcion_edicion_mascota(opcion, mascota, mascotas):
    if opcion == "1":
        cambioDeId(mascota, mascotas)
    elif opcion == "2":
        mascota["nombre"] = input_nombre_valido("Nuevo nombre: ").title()
    elif opcion == "3":
        mascota["tipo"] = input_tipo_mascota("Nuevo tipo: ", tiposMascotas)
    elif opcion == "4":
        mascota["edad"] = input_numero_entero("Nueva edad: ")
    else:
        print("Opción inválida.")

def editar_duenio(duenios, usuario_logueado):
    duenio = seleccionar_elemento_por_id(duenios, mostrar_ids_duenios)
    if not duenio:
        return

    while True:
        opcion = menu_edicion_duenio(duenio)
        if opcion == "0":
            break
        procesar_opcion_edicion_duenio(opcion, duenio)

    guardar_datos_json(ruta_duenios, duenios)
    registrar_log_auditoria(usuario_logueado, f"Modificó dueñx ID {duenio['id']}")
    print("Cambios guardados.")


def menu_edicion_duenio(duenio):
    print(f"""\n--- Editar Dueñx: {duenio['nombre']} ---
1: Cambiar ID
2: Cambiar nombre
3: Cambiar teléfono
4: Cambiar mail
0: Finalizar edición""")
    return input("Seleccione una opción: ").strip()


def procesar_opcion_edicion_duenio(opcion, duenio):
    if opcion == "1":
        cambioDeId(duenio, duenios)
    elif opcion == "2":
        duenio["nombre"] = input_nombre_valido("Nuevo nombre: ").title()
    elif opcion == "3":
        duenio["telefono"] = input_numero_entero("Nuevo teléfono: ")
    elif opcion == "4":
        duenio["mail"] = input_email_valido("Nuevo mail: ")
    else:
        print("Opción inválida.")

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
                6: Ver mascotas por tipo\n
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
            mostrarMascotasPorTipo(mascotas)
        elif opcionConsulta == "7":
            return # Volvemos al menú principal
        else:
            print("Opción inválida. Intente nuevamente.")

#Función mostrar todas las mascotas en la lista de mascotas
def mostrarTodasLasMascotas(mascotas, duenios):

    if not mascotas: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay mascotas registradas.") #En caso de que este vacía mostramos por pantalla que no hay mascotas registradas
        return
    for mascota in mascotas: #Recorremos cada mascota en la lista de diccionarios "mascotas"
        muestraDatosMascota(mascota)
        

#Función para mostrar todos los dueños de la lista de diccionarios "duenios"
def mostrarTodosLosDuenios(mascotas, duenios):
    if not duenios: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay dueños registrados.") #En caso de que este vacía mostramos por pantalla que no hay dueños registrados
        return

    for duenio in duenios: #Recorremos cada dueño en la lista de diccionarios "duenios"
        muestraDatosDuenios(duenio)
        

#Función para buscar las mascotas por nombre (Devuelve todas las coincidencias con ese nombre)
def buscarMascotaPorNombre(mascotas, duenios):
    nombreMascota = input("Ingrese el nombre de la mascota a buscar: ").lower()
    listaMascotaEncontrada = []  # Inicializamos una lista vacía para guardar las coincidencias de mascotas encontradas

    for mascota in mascotas: #Recorremos todas las mascotas en la lista de diccionarios "mascotas"
        if nombreMascota in mascota["nombre"].lower(): #Si el nombre ingresado conincide con alguno de la lista de diccionarios lo agregamos a "listaMascotaEncontrada"
            listaMascotaEncontrada.append(mascota)

    if not listaMascotaEncontrada: #Verificamos si la lista donde almacenamos las mascotas encontradas está vacía (Devuelve falso si está vacía)
        print("No se encontraron mascotas con ese nombre.")
    else:
        for mascota in listaMascotaEncontrada:
            nombres_duenios = [duenio['nombre'] for duenio in duenios if duenio['id'] in mascota['dueños']] #Recorremos todas las mascotas encontradas
            muestraDatosMascota(mascota)

            for fila in mascota['historial']:
                print(" - ".join(fila))
            print("--- Dueñx/s ---")
            print(f"Dueñx/s: {' - '.join(nombres_duenios)}")

#Función para buscar los dueños por nombre (Devuelve todas las coincidencias con ese nombre)
def buscarDuenioPorNombre(mascotas, duenios):
    nombreDuenio = input("Ingrese el nombre del dueñx a buscar: ").lower()
    listaDueniosEncontrados = []

     
    for duenio in duenios: # Recorremos todos los dueños de la lista de diccionarios "duenios"
        if nombreDuenio == duenio["nombre"].lower(): #Si el nombre ingresado conincide con alguno de la lista de diccionarios "duenios" lo agregamos a "listaDueniosEncontrados"
            listaDueniosEncontrados.append(duenio)


    if not listaDueniosEncontrados: #Verificamos si la lista donde almacenamos los dueños encontrados está vacía (Devuelve falso si está vacía)
        print("No se encontraron dueñxs con ese nombre.")
    else:
        for duenio in listaDueniosEncontrados: #Recorremos todos los dueños encontrados
            muestraDatosDuenios(duenio)
            

#mostrar mascotas por tipo 6
def mostrarMascotasPorTipo(mascotas):
    tipoAnimal= input("ingrese el tipo de mascota: ")
    if tipoAnimal.title() not in tiposMascotas:
        print("Error, tipo animal no encontrado")
        return
    listaTipo=list(filter(lambda x:x["tipo"]== tipoAnimal.title(),mascotas))
    for mascota in listaTipo:
        muestraDatosMascota(mascota)
    return

def MenuHistorialMascota(mascotas):
    while True:
        print("""\n--- Consultar Historial ---\n
                1: Ver todo el historial de la mascota\n
                2: Ver últimas 10 visitas a la veterinaria\n
                3: Volver al menú principal""")


        opcionHistorial = int(input("Seleccione una opción: "))

        if opcionHistorial == 1:
            mostrarHistorialMascota(mascotas)
        elif opcionHistorial == 2:
            mostrarUltimasDiezVisitas(mascotas)
        elif opcionHistorial == 3:
            return
        else:
            print("Opción inválida. Intente nuevamente.")

#Función para buscar el historial médico de la mascota
def mostrarHistorialMascota(mascotas):
    
    if not mascotas: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay mascotas registradas.") #En caso de que este vacía mostramos por pantalla que no hay mascotas registradas
        return

    #Solicitamos al usuario que ingrese el ID de masocta al que queremos buscar
    mascota_id = input("Ingrese el ID de la mascota: ").strip()
    while not mascota_id.isdigit():
        print("El ID ingresado no es un ID váido")
        mascota_id = input("Ingrese el ID de la mascota: ").strip()
    
    mascota_id = int(mascota_id)

    print("\nHistorial Mascota: ")
    for mascota in mascotas:
        if mascota["id"] == mascota_id:
            for fila in mascota['historial']:
                print(" - ".join(fila))

#Función para buscar las últimas 10 visitas médicas de la mascota
def mostrarUltimasDiezVisitas(mascotas):
    if not mascotas: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay mascotas registradas.") #En caso de que este vacía mostramos por pantalla que no hay mascotas registradas
        return

    #Solicitamos al usuario que ingrese el ID de masocta al que queremos buscar
    mascota_id = input("Ingrese el ID de la mascota: ").strip()
    while not mascota_id.isdigit():
        print("El ID ingresado no es un ID váido")
        mascota_id = input("Ingrese el ID de la mascota: ").strip()

    mascota_id = int(mascota_id)

    print("\nHistorial Mascota: ")
    for mascota in mascotas:
        if mascota["id"] == mascota_id:
            historial = mascota["historial"]

            ultimasDiezVisitas = historial[-10:]
            for fila in ultimasDiezVisitas:
                print(" - ".join(fila))
"""
--------------------------------------------------------------------------------------------------------
Menu Mi Perfil
--------------------------------------------------------------------------------------------------------
"""
def menu_perfil():
    while True:
        print("""
              --- Mi Perfil ---
              1. Ver mis datos
              2. Modificar mis datos
              0. Volver al Menú Principal
                """)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("Ha seleccionado Ver mis datos")
            ver_usuario(usuario_actual)
        elif opcion == "2":
            print("Ha seleccionado Modificar mis datos")
            modificar_datos_usuario(usuario_actual)
        elif opcion == "0":
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
def ver_usuario(usuario_actual):
    if usuario_actual:
        print("\n--- Datos del Usuario Actual ---")
        print(f"Usuario: {usuario_actual['usuario']}")
        print(f"Contraseña: {usuario_actual['clave']}")
        print(f"Nombre: {usuario_actual['nombre']}")
        print(f"Teléfono: {usuario_actual['telefono']}")
        print(f"Correo: {usuario_actual['correo']}")
        print(f"Rol: {usuario_actual['rol']}")
        print("Disponibilidad:")
        for dia, horarios in usuario_actual["disponibilidad"].items():
            if horarios:
                print(f"{dia}: {', '.join(horarios)}")
            else:
                print(f"{dia}: No disponible")
    else:
        print("No hay usuario actual.")    

def modificar_datos_usuario(usuario_actual):
    while True:
        print("""
              --- Modificar Mis Datos ---
              1. Modificar nombre y apellido
              2. Modificar nombre de usuario
              3. Modificar contraseña
              4. Modificar teléfono
              5. Modificar correo
              6. Modificar rol
              7. Modificar disponibilidad    
              0. Volver al Menú de Perfil
          """)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nuevo_nombre = validar_nombre()
            usuario_actual["nombre"] = nuevo_nombre
            print("Nombre modificado exitosamente.")
        elif opcion == "2":
            nuevo_usuario = validar_usuario(usuarios)
            usuario_actual["usuario"] = nuevo_usuario
            print("Nombre de usuario modificado exitosamente.")
        elif opcion == "3":
            nueva_clave = validar_contrasenia()
            usuario_actual["clave"] = nueva_clave
            print("Contraseña modificada exitosamente.")
        elif opcion == "4":
            nuevo_telefono = validar_telefono()
            usuario_actual["telefono"] = nuevo_telefono
            print("Teléfono modificado exitosamente.")  
        elif opcion == "5":
            nuevo_correo = validar_correo()
            usuario_actual["correo"] = nuevo_correo
            print("Correo modificado exitosamente.")
        elif opcion == "6":
            nuevo_rol = validar_rol()
            usuario_actual["rol"] = nuevo_rol
            print("Rol modificado exitosamente.")
        elif opcion == "7":
            usuario_actual["disponibilidad"] = ingresar_disponibilidad(dias_validos)
            print("Disponibilidad modificada exitosamente.")
        elif opcion == "0":
            print("Volviendo al Menú de Perfil...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
        

"""
--------------------------------------------------------------------------------------------------------
Funciones de Log In y Sign Up
--------------------------------------------------------------------------------------------------------
"""
def iniciar_sesion(usuarios):
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
        dia= input("Día (ej. lunes): ")
        if dia == "":
            break
        texto_limpio = limpiar_texto(dia)
        if texto_limpio not in dias_validos:
            print("Día inválido. Intente nuevamente.")
            continue
        rangos_validos = disponibilidad.get(texto_limpio, []).copy()
        print(f"Ingrese los horarios (ej. 08:00(INICIO)-12:00(FIN),14:00(INICIO)-18:00(FIN))")
        print("Presione Enter para finalizar.")
        while True:
            horarios_ingresados = input(f"Horarios para {dia}: ")
            rangos = [h.strip() for h in horarios_ingresados.split(",") if h.strip()] #separa los horarios_ingresaros ","
            if horarios_ingresados == "":
                break
            for r in rangos:
                if validar_rango_horario(r, rangos_validos):
                    rangos_validos.append(r)
                    disponibilidad[texto_limpio] = ordenar_rangos(rangos_validos)

                else:
                    print(f"Rango inválido o solapado: {r}. No se agregó.")
    return ordenar_disponibilidad(disponibilidad)
    

def crear_usuario(usuarios):
    print("\nCrear nuevo usuario")
    nuevo_usuario = {}
    nuevo_usuario["usuario"] = validar_usuario(usuarios)
    nuevo_usuario["clave"] = validar_contrasenia()
    nuevo_usuario["nombre"] = validar_nombre()
    nuevo_usuario["telefono"] = validar_telefono()
    nuevo_usuario["correo"] = validar_correo()
    nuevo_usuario["rol"] = validar_rol()
    nuevo_usuario["disponibilidad"] = ingresar_disponibilidad(dias_validos)
    usuarios.append(nuevo_usuario)
    guardar_datos_json(ruta_usuarios, usuarios)
    print("Usuario creado exitosamente.")
    print(json.dumps(nuevo_usuario, indent=4, ensure_ascii=False)) #mostrar nuevo usuario


"""
--------------------------------------------------------------------------------------------------------
MENU - Dueños y Mascotas
--------------------------------------------------------------------------------------------------------
"""
def menu_duenios_mascotas(mascotas, duenios, tiposMascotas, usuario_logueado):
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
                modificarInformacion(mascotas, duenios, usuario_logueado)
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

#  --------------------------------------------------------------------------------------------------------
# Menu Gestión de Visitas Médicas 
# --------------------------------------------------------------------------------------------------------
        
def menu_visitas_medicas():
    while True:
        print("""
              --- Gestión de Turnos ---
              1. Ver disponibilidad de veterinarios
              2. Agendar nuevo turno
              3. Ver calendario de turnos
              4. Modificar turno programado
              5. Eliminar turno programado
              0. Volver al Menú Principal
                """)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("Ha seleccionado Ver disponibilidad de veterinarios")
            consultar_disponibilidad(usuarios)
        elif opcion == "2":
            print("Ha seleccionado Agendar nuevo turno")
            registrar_turno(mascotas, usuario_actual,calendario)
        elif opcion == "3":
            print("Ha seleccionado Ver calendario de turnos")
            consultar_turno(mascotas)
        elif opcion == "4":
            print("Ha seleccionado Modificar turno programado")
            modificar_turno(mascotas)
        elif opcion == "5":
            print("Ha seleccionado Eliminar turno programado")
            eliminar_turno(mascotas)
        elif opcion == "0":
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")       
def consultar_disponibilidad(usuarios):
    print("\n--- Disponibilidad de Veterinarios ---")
    for usuario in usuarios:
        if usuario["rol"] == "Veterinario":
            print(f"\nNombre: {usuario['nombre']}")
            print("Disponibilidad:")
            for dia, horarios in usuario["disponibilidad"].items():
                if horarios:
                    print(f"{dia}: {', '.join(horarios)}")
                else:
                    print(f"{dia}: No disponible")

def registrar_turno(mascotas, usuario_actual, calendario):
    if not mascotas:
        print("No hay mascotas registradas. Por favor, registre una mascota primero.")
        return menuPrincipal()
    mascota = input("Ingrese el nombre de la mascota: ").strip()

"""
--------------------------------------------------------------------------------------------------------
MENU - PROGRAMA PRINCIPAL
--------------------------------------------------------------------------------------------------------
"""
def menuPrincipal():
    while True:
        print("""
              --- Menú Principal ---
              1. Gestión de Mascotas y Dueñxs
              2. Visitas Médicas
              3. Mi Perfil
              0. Finalizar Sesión
                """)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_duenios_mascotas()
        elif opcion == "2":
            menu_visitas_medicas()
        elif opcion == "3":
            menu_perfil()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Por favor, intente nuevamente.")

"""
--------------------------------------------------------------------------------------------------------
MENU - Log In / Sign Up
--------------------------------------------------------------------------------------------------------
"""
def menu_inicio(ruta_usuarios):

    usuarios = cargar_datos_json(ruta_usuarios)
    global usuario_actual

    print("""--- ¡Bienvenido! ---\n
1. Iniciar sesión\n
2. Registrarse\n
3. Cambiar contraseña\n
0. Salir\n""")

    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == "1":
                if not usuarios:
                    print("No hay usuarios registrados. ¿Desea crear uno? (s/n)")
                    respuesta = input().strip().lower()
                    if respuesta == "s":
                        crear_usuario(usuarios)
                        usuarios = cargar_datos_json(ruta_usuarios)
                        continue
                    elif respuesta == "n":
                        print("¡Hasta luego!")
                        break
                usuario_actual = iniciar_sesion(usuarios)
                menuPrincipal(mascotas, duenios, tiposMascotas, usuario_actual)
            elif opcion == "2":
                crear_usuario(usuarios)
                usuarios = cargar_datos_json(ruta_usuarios)
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
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
menu_inicio(ruta_usuarios)