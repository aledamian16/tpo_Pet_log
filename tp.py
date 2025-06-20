import json
import re
from datetime import datetime
import unicodedata #normalizar texto

# --------------------------------------------------------------------------------------------------------
# Rutas de archivos
# --------------------------------------------------------------------------------------------------------
ruta_usuarios = r"C:\Users\Vanesa\OneDrive\Documentos\TP\Usuarios.json"
ruta_mascotas = r"C:\Users\Vanesa\OneDrive\Documentos\TP\Mascotas.json"
ruta_duenios = r"C:\Users\Vanesa\OneDrive\Documentos\TP\Duenios.json"
ruta_calendario = r"C:\Users\Vanesa\OneDrive\Documentos\TP\Calendario.json"


# --------------------------------------------------------------------------------------------------------
# Funciones para cargar y guardar los archivos JSON
# --------------------------------------------------------------------------------------------------------
def cargar_datos_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

usuarios = cargar_datos_json(ruta_usuarios)
mascotas = cargar_datos_json(ruta_mascotas)
duenios = cargar_datos_json(ruta_duenios)
calendario = cargar_datos_json(ruta_calendario)

# --------------------------------------------------------------------------------------------------------
# Datos Globales
# --------------------------------------------------------------------------------------------------------
roles_validos = ("Gerente", "Recepcionista", "Veterinario")
usuario_actual = None
dias_validos = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado")
tiposMascotas = ("Perro" , "Gato", "Ave", "Reptil", "Roedor", "Pez", "Otro")
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
# -----------------------------------------------------

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
    Útil para que el usuario identifique fácilmente qué ID corresponde a cada mascota.
    """
    if not mascotas:
        print("No hay mascotas registradas.")
        return

    print("\n--- Mascotas Registradas ---")
    for mascota in mascotas:
        print(f"ID {mascota['id']}: {mascota['nombre'].capitalize()}")
    print("----------------------------")

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

def input_tipo_mascota(mensaje, tipos):
    while True:
        tipo = input(mensaje).strip().title()
        if tipo in tipos:
            return tipo
        print(f"Tipo inválido. Tipos válidos: {', '.join(tipos)}")

#  --------------------------------------------------------------------------------------------------------
# Menu Principal 
# --------------------------------------------------------------------------------------------------------

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
            menu_mascotas_duenios()
        elif opcion == "2":
            menu_visitas_medicas()
        elif opcion == "3":
            menu_perfil()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Por favor, intente nuevamente.")
#  --------------------------------------------------------------------------------------------------------
# Menu Gestión de Mascotas y Dueñxs
# --------------------------------------------------------------------------------------------------------

def menu_mascotas_duenios():
    while True:
        print("""
              --- Gestión de Mascotas y Dueñxs ---
              1. Consultar Mascotas/Dueñxs
              2. Agregar Mascota/Dueñx
              3. Modificar Mascota/Dueñx
              4. Eliminar Mascota/Dueñx
              0. Volver al Menú Principal
                """)
        opcion = input("Seleccione una opción: ")
        if opcion == 1:
            print("Ha seleccionado Consultar Mascota y/o Dueñx")
            consultarInformacion(mascotas, duenios)
        elif opcion == 2:
            print("Ha seleccionado Agregar Nueva Mascota y/o Dueñx")
            menu_agregar(mascotas, duenios, tiposMascotas)
        elif opcion == 3:
            print("Ha seleccionado Modificar Mascota y/o Dueñx")
            modificarInformacion(mascotas, duenios)
        elif opcion == 4:
            print("Ha seleccionado Eliminar Mascota y/o Dueñx")
            menu_eliminar(duenios, mascotas)
        elif opcion == 5:
            print("Ha seleccionado Registrar nueva visita médica")
            registrar_visita(mascotas,usuario_actual)
        elif opcion == 0:
            print("Sesión Finalizada.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

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
        if opcion == "2":
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

#  --------------------------------------------------------------------------------------------------------
# Menu Gestión de Visitas Médicas 
# --------------------------------------------------------------------------------------------------------
def menu_mascotas_duenios():
    while True:
        print("""
              --- Gestión de Mascotas y Dueñxs ---
              1. Consultar Mascotas/Dueñxs
              2. Agregar Mascota/Dueñx
              3. Modificar Mascota/Dueñx
              4. Eliminar Mascota/Dueñx
              0. Volver al Menú Principal
                """)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("Ha seleccionado Consultar Mascota y/o Dueñx")
            consultarInformacion(mascotas, duenios)
        elif opcion == "2":
            print("Ha seleccionado Agregar Nueva Mascota y/o Dueñx")
            menu_agregar(mascotas, duenios, tiposMascotas)
        elif opcion == "3":
            print("Ha seleccionado Modificar Mascota y/o Dueñx")
            modificarInformacion(mascotas, duenios)
        elif opcion == "4":
            print("Ha seleccionado Eliminar Mascota y/o Dueñx")
            menu_eliminar(duenios, mascotas)
        elif opcion == "0":
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
#  --------------------------------------------------------------------------------------------------------
# Funcion consultar información de mascotas y dueños
# --------------------------------------------------------------------------------------------------------

def consultarInformacion(mascotas, duenios):
    while True:
        print("""\n--- Consultar Información ---\n
                1: Ver todas las mascotas\n
                2: Ver todos los dueños\n
                3: Buscar mascota por nombre\n
                4: Buscar dueño por nombre\n
                5: Ver historial médico de una mascota\n
                6: Volver al menú principal""")


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
            return # Volvemos al menú principal
        else:
            print("Opción inválida. Intente nuevamente.")
def mostrarTodasLasMascotas(mascotas, duenios):

    if not mascotas: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay mascotas registradas.") #En caso de que este vacía mostramos por pantalla que no hay mascotas registradas
        return
    for mascota in mascotas: #Recorremos cada mascota en la lista de diccionarios "mascotas"
        nombresDuenios = []  # En esta lista vacía vamos a ir guardando los nombres de los dueños de la mascota consultada

        for duenio in duenios:  # Por cada mascota que recorremos , recorremos todos los dueños de la lista de diccionarios "duenios"
            if duenio["id"] in mascota["dueños"]:  #Si el id de ese dueño está vinculado a la mascota procederemos a agregarlo a la lista "nombresDuenios"
                nombresDuenios.append(duenio["nombre"])

        print(f"ID: {mascota['id']}")
        print(f"Nombre: {mascota['nombre']}")
        print(f"Tipo: {mascota['tipo']}")
        print(f"Edad: {mascota['edad']} años")
        print(f"Dueñx/s: {' - '.join(nombresDuenios)}")
        print("----------------------------------")
def mostrarTodosLosDuenios(mascotas, duenios):
    if not duenios: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay dueños registrados.") #En caso de que este vacía mostramos por pantalla que no hay dueños registrados
        return

    for duenio in duenios: #Recorremos cada dueño en la lista de diccionarios "duenios"
        mascotasDuenio = [] # En esta lista vacía vamos a ir guardando los nombres de los dueños de la mascota consultada
        
        for mascota in mascotas: # Por cada dueño que recorremos , recorremos todas los mascotas de la lista de diccionarios "mascotas"
            if duenio["id"] in mascota["dueños"]: #Si el id de ese dueño está vinculado a la mascota procedemos a agregar la mascota a agregarlo a la lista "mascotasDuenio"
                mascotasDuenio.append(mascota["nombre"])

        print("--- Persona ---")
        print(f"ID: {duenio['id']}")
        print(f"Nombre: {duenio['nombre']}")
        print("--- Contacto ---")
        print(f"Teléfono: {duenio['telefono']}")
        print(f"Mail: {duenio['mail']}")
        print("--- Mascotas ---")
        print(f"Mascotas: {' - '.join(mascotasDuenio)}")
        print("----------------------------------")

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
        for mascota in listaMascotaEncontrada: #Recorremos todas las mascotas encontradas
            nombresDuenios = []  # Lista para los nombres de los dueños
            for duenio in duenios: #Recorremos todos los dueños de la lista de diccionarios "duenios"
                if duenio["id"] in mascota["dueños"]: #Si el id de ese dueño está vinculado a la mascota procedemos a agregar al dueño a la lista de dueños de las mascotas encontradas
                    nombresDuenios.append(duenio["nombre"])

            # Mostramos los datos de la mascota
            print("--- Mascota ---")
            print(f"ID: {mascota['id']}")
            print(f"Nombre: {mascota['nombre']}")
            print(f"Tipo: {mascota['tipo']}")
            print(f"Edad: {mascota['edad']} años")
            print("Historial Médico:")
            for fila in mascota['historial']:
                print(" - ".join(fila))
            print("--- Dueñx/s ---")
            print(f"Dueñx/s: {' - '.join(nombresDuenios)}")

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
            mascotasDelDuenio = [] #Lista para los nombres de las mascotas
            for mascota in mascotas: #Recorremos todas lass mascotas de la lista de diccionarios "mascotas"
                if duenio["id"] in mascota["dueños"]: #Si el id de ese dueño está vinculado a la mascota procedemos a agregar a la mascota a la lista de mascotas de los dueños encontrados
                    mascotasDelDuenio.append(mascota["nombre"])
            
            # Mostramos los datos de la persona
            print("--- Dueñx ---")
            print(f"ID: {duenio['id']}")
            print(f"Nombre: {duenio['nombre']}")
            print(f"Teléfono: {duenio['telefono']}")
            print("--- Mascota ---")
            print(f"Mascotas: {' - '.join(mascotasDelDuenio)}")
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

# --------------------------------------------------------------------------------------------------------
# Funciones para agregar nueva mascota y/o dueñx
# --------------------------------------------------------------------------------------------------------

def menu_agregar(mascotas, duenios, tipos_mascotas):
    while True:
        print("""\n--- Menú Agregar ---
                1: Agregar dueñx
                2: Agregar mascota
                3: Volver al menú principal""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_duenio(duenios, mascotas)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
        elif opcion == "2":
            agregar_mascota(mascotas, duenios, tipos_mascotas)
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
    
def agregar_duenio(duenios, mascotas):
    nuevo_id = generar_id(duenios)

    nombre = input("Nombre del dueñx: ")
    telefono = input("Teléfono (solo números): ")
    email = input("Correo electrónico: ")



    duenio = {
        "id": nuevo_id,
        "nombre": validar_nombre(nombre),
        "telefono": validar_telefono(telefono),
        "mail": validar_correo(email),
    }
    duenios.append(duenio)
    print(f"Dueñx '{nombre}' agregado con ID {nuevo_id}.\n")

    # Asociar a mascota
    if mascotas:
        opcion = input("¿Desea asociar este nuevo dueñx a una mascota? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            asociar_duenio_a_mascota(nuevo_id, mascotas)

    return duenio

def agregar_mascota(mascotas, duenios, tipos_mascotas):
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

# --------------------------------------------------------------------------------------------------------
# Funciones para modificar información de mascotas y dueños
# --------------------------------------------------------------------------------------------------------

def busquedaDeId(datosUsuarios):
    individuoEncontrado=False
    ingreseIdIndividuo =int(input("ingresar ID de Individuo a editar: "))
    while individuoEncontrado!= True:
        ingreseIdIndividuo =int(input("ingresar ID correctamente : "))#ingresar id de la mascota a editar
        while not str(ingreseIdIndividuo).isnumeric():
            ingreseIdIndividuo= input("Ingrese el ID correctamente:")#en caso de no ser caracter numerico vuelve a solicitarlo
            #Utilizamos un booleano para corroborar que el individuo exista
        for usuario in datosUsuarios:
            if  ingreseIdIndividuo == usuario['id']:
                individuoEncontrado=True
    
    return ingreseIdIndividuo

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
#reutilizacion cambio nombre

def cambioNombre(individuo):
    nuevoNombre = input("ingresar nombre: ")
    nombreSinEspacios=nuevoNombre.remplace(" ","") 
    while not nombreSinEspacios.isalpha(): # en caso de tener caracter numerico vuelve solicitar el nombre
        print("Nombre inválido: solo letras")
        nuevoNombre = input("ingresar nombre valido: ")
        nombreSinEspacios=nuevoNombre.remplace(" ","")
    individuo["nombre"] = nuevoNombre.title()
    return individuo

# se podria usar lambda
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


#Funciones de  2: Modificar Mascota y/o Dueñx
def  modificarInformacion(mascotas, duenios):
    while True:
        print("""\n--- Consultar Información ---\n
                1: modificar datos mascotas\n
                2: modificar datos dueños\n
                3: Volver al menú principal""")
        opcion = int(input("ingresar opcion deseada: "))

        if opcion == 1:
            editarDatosMascotas(mascotas)
        if opcion == 2:
            editarDatosDuenio(duenios)
        if opcion == 3:
            #volver al menu principal
            return True

   #1: modificar datos mascotas     

def editarDatosMascotas(mascotas):

    idMascotaEncontrada= busquedaDeId(mascotas)

    for mascota in mascotas:
        if idMascotaEncontrada == mascota["id"]:
            print (mascota)# se muestran los datos de la mascota para corroborar que es la correcto
            print("""--- Seleccione atributo a editar: ---\n
                1: ID\n
                2: nombre\n
                3: Tipo\n
                4: Edad\n
                0: Finalizar Sesión
                --------------------------------------""")
            opcion =int(input("seleccione opcion: "))
            
            if opcion == 0:
                return True

            if opcion == 1:#para cambiar el id se corrobora que no se encuentre entre los existentes
                cambioDeId(mascota, mascotas)
                            
            if opcion == 2:
                cambioNombre(mascota)
            if opcion == 3:
                cambioTipoMascota = input("ingrese el tipo de mascota: ")
                while not cambioTipoMascota.isalpha(): #solicita nuevamente si no es caracter alfabetico 
                    print("Tipo inválido: solo letras")
                    cambioTipoMascota = input("ingrese un tipo de mascota valido: ")
                if cambioTipoMascota.title() in tiposMascotas: # busca que el tipo este en la tupla
                    mascota["tipo"] = cambioTipoMascota.title()# lo transforma a titulo para no crear un posible error
                else:
                    return False # en caso de no existir el tipo devuelve al menu
            if opcion == 4:
                cambioEdadMascota = input("ingrese edad a modificar: ")
                while not str(cambioEdadMascota).isnumeric():
                    cambioEdadMascota= input("Ingrese la edad correctamente:")# en caso de no ser numerico volvemos a solicitar el numero
                mascota["edad"] = int(cambioEdadMascota) 
            
            #nombresDuenios = [duenio["nombre"] for duenio in duenios if duenio["id"] in mascota["dueños"]] #lista por comprension para retornar el nombre de los dueños en una lista
        
            muestraDatosMascota(mascota)
            return False
      
#2: modificar datos dueños
def editarDatosDuenio(duenios):
    idDuenioEncontrado = busquedaDeId(duenios)
        
    for duenio in duenios:
        if idDuenioEncontrado == duenio["id"]:
            print (duenio)# se muestran los datos del dueño para corroborar que es el correcto
            print("""--- Seleccione atributo a editar: ---\n
                1: ID\n
                2: nombre\n
                3: Telefono\n
                4: mail\n
                0: Finalizar Sesión
                --------------------------------------""")
            opcion =int(input("seleccione opcion: "))

            if opcion == 0:
                return True

            if opcion == 1: #para cambiar el id se corrobora que no se encuentre entre los existentes
                cambioDeId(duenio, duenios)    
            
            if opcion == 2:
                cambioNombre(duenio)
            
            if opcion == 3:
                nuevoTelefono = input("ingresar nuevo telefono: ")
                while not nuevoTelefono.isnumeric():# se asegura que todos los caracteres sean numericos
                        nuevoTelefono= input("Ingrese el telefono correctamente:")
                duenio["telefono"] = nuevoTelefono
            #cambio mail
            if opcion == 4:
                obligatorio=["@gmail.com", "@yahoo.com","@hotmail.com","@uade.edu.ar"]
                nuevoMail=input("ingresar nuevo mail: ")# realizamos un filtro para asegurar de que el mail sea correcto
                flag2=False # booleano como condicion para salir del bucle
                while flag2!=True:
                    for i in range(len(nuevoMail)):
                        if nuevoMail[i]=="@":
                            if nuevoMail[i:] in obligatorio:#Compara los caracteres desde el @ hasta el final 
                                duenio["mail"]= nuevoMail# en caso de ser un tipo de mail valido realiza la modificacion
                                print("el mail es correcto!!")
                                flag2=True
                    if flag2==False:
                        nuevoMail = input("ingresar un mail valido: ")
                                               
            #mascotasDuenio = [mascota["nombre"] for mascota in mascotas if duenio["id"] in mascota["dueños"]]#utilizamos listas por comprension para mostras nombres de las mascotas
            muestraDatosDuenios(duenio)
            return False

#  --------------------------------------------------------------------------------------------------------
# Funcion eliminar Mascota y/o Dueñx
# --------------------------------------------------------------------------------------------------------

def menu_eliminar(duenios, mascotas):
    print("""¿Qué desea eliminar?
    1: Mascota
    2: Dueñx""")
    opcion = input("Ingrese el número de la opción: ").strip()

    if opcion == "1":
        id_mascota = input("Ingrese el ID de la mascota a eliminar: ")
        id_mascota = input_id_valido(id_mascota)
        eliminar_mascota_por_id(mascotas, id_mascota)
        guardar_datos_json(ruta_mascotas, mascotas)

    elif opcion == "2":
        id_duenio = input("Ingrese el ID del dueñx a eliminar: ")
        id_duenio = input_id_valido(id_duenio)
        if eliminar_duenio_por_id(duenios, id_duenio):
            actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios)
            guardar_datos_json(ruta_duenios, duenios)
            guardar_datos_json(ruta_mascotas, mascotas)
    else:
        print("Opción inválida. No se realizó ninguna acción.")

def eliminar_mascota_por_id(mascotas, id_mascota):
    try:
        mascota = buscar_por_id(mascotas, id_mascota)
        if mascota:
            mascotas.remove(mascota)
            print(f"La mascota {mascota['nombre']} con ID {id_mascota} ha sido eliminada exitosamente.")
        else:
            print(f"No se encontró una mascota con ID {id_mascota}.")
    except Exception as e:
        print(f"Error al eliminar la mascota: {e}")

def eliminar_duenio_por_id(duenios, id_duenio):
    duenio = buscar_por_id(duenios, id_duenio)
    if duenio:
        duenios.remove(duenio)
        print(f"Dueñx {duenio['nombre']} con ID {id_duenio} ha sido eliminado exitosamente.")
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

# --------------------------------------------------------------------------------------------------------
# Funciones para registrar visita médica
# --------------------------------------------------------------------------------------------------------

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




#  --------------------------------------------------------------------------------------------------------
# Menu Mi Perfil 
# --------------------------------------------------------------------------------------------------------
          
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
        


# --------------------------------------------------------------------------------------------------------
# Funciones de inicio de sesión y creación de usuario       
# --------------------------------------------------------------------------------------------------------

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

def menu_inicio():
    global usuarios
    global usuario_actual 
    try:
        while True:
            print("\nBienvenido al sistema de la veterinaria")
            print("1. Iniciar sesión")
            print("2. Crear nuevo usuario")
            print("0. Salir")
            opcion = input("Seleccione una opción: ").strip()
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
                menuPrincipal()
            elif opcion == "2":
                crear_usuario(usuarios)
                usuarios = cargar_datos_json(ruta_usuarios)
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario. Saliendo...")
    return usuario_actual
menu_inicio()
