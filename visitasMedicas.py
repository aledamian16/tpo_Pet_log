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
            consultar_disponibilidad()
        elif opcion == "2":
            print("Ha seleccionado Agendar nuevo turno")
            registrar_turno()
        elif opcion == "3":
            print("Ha seleccionado Ver turnos")
            consultar_turno()
        elif opcion == "4":
            print("Ha seleccionado Modificar turno programado")
            modificar_turno()
        elif opcion == "5":
            print("Ha seleccionado Eliminar turno programado")
            eliminar_turno()
        elif opcion == "0":
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")       
def consultar_disponibilidad():
    print("\n--- Consultar Disponibilidad de Veterinarios ---")

    dia_input = input("Ingrese el día (ej: Lunes): ").strip()
    dia = limpiar_texto(dia_input)

    if dia not in dias_validos:
        print("Día inválido. Intente nuevamente.")
        return

    veterinarios = [u for u in usuarios if u["rol"] == "Veterinario"]
    if not veterinarios:
        print("No hay veterinarios registrados.")
        return

    print(f"\nDisponibilidad para el día {dia.title()}:\n")
    alguno_disponible = False
    for vet in veterinarios:
        disponibilidad = vet.get("disponibilidad", {})
        rangos = disponibilidad.get(dia, [])
        if rangos:
            alguno_disponible = True
            print(f"{vet['nombre']}: {', '.join(ordenar_rangos(rangos))}")
        else:
            print(f"{vet['nombre']}: No disponible")

    if not alguno_disponible:
        print("Ningún veterinario tiene disponibilidad registrada para ese día.")
def veterinario_ya_ocupado(veterinario, fecha, hora):
    for turno in turnos:
        if (turno["veterinario"] == veterinario and 
            turno["fecha"] == fecha and 
            turno["hora"] == hora):
            return True
    return False

def registrar_turno():
    if not mascotas:
        print("No hay mascotas registradas.")
        return

    print("\n--- Mascotas Registradas ---")
    for mascota in mascotas:
        print(f"ID {mascota['id']}: {mascota['nombre']}")
    print("----------------------------")

    id_mascota = input_numero_entero("Ingrese el ID de la mascota: ")
    mascota = buscar_por_id(mascotas, id_mascota)
    if not mascota:
        print("Mascota no encontrada.")
        return

    # Ingreso de fecha con validación
    while True:
        fecha = input("Ingrese la fecha del turno (AAAA-MM-DD): ").strip()
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_obj.year >= 2025:
                break
            else:
                print("El año debe ser 2025 o mayor.")
        except ValueError:
            print("Formato de fecha inválido.")

    # Ingreso de hora con validación
    while True:
        hora = input("Ingrese la hora (HH:MM, entre 08:00 y 17:59): ").strip()
        if re.match(r"^(0[8-9]|1[0-7]):[0-5][0-9]$", hora):
            break
        else:
            print("Hora inválida. Debe estar entre 08:00 y 17:59.")

    # Día de la semana traducido (inglés a español)
    dias_ingles_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miercoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sabado"
    }
    dia_ingles = fecha_obj.strftime("%A")
    dia_semana = dias_ingles_espanol.get(dia_ingles, "")

    # Filtrar veterinarios disponibles
    veterinarios_disponibles = []
    for usuario in usuarios:
        if usuario["rol"] == "Veterinario":
            disponibilidad = usuario.get("disponibilidad", {})
            rangos = disponibilidad.get(dia_semana, [])
            for rango in rangos:
                inicio, fin = rango.split("-")
                if inicio <= hora <= fin:
                    veterinarios_disponibles.append(usuario)
                    break

    if not veterinarios_disponibles:
        print("No hay veterinarios disponibles en ese día y horario.")
        return

    print("\nVeterinarios disponibles:")
    for i, vet in enumerate(veterinarios_disponibles):
        print(f"{i+1}. {vet['nombre']}")

    opcion = input_numero_entero("Seleccione un veterinario por número: ")
    if not (1 <= opcion <= len(veterinarios_disponibles)):
        print("Opción inválida.")
        return
    if veterinario_ya_ocupado(veterinarios_disponibles[opcion - 1]["nombre"], fecha, hora):
        print(f"El veterinario {veterinarios_disponibles[opcion - 1]['nombre']} ya tiene un turno asignado en esa fecha y hora.")
        return

    veterinario = veterinarios_disponibles[opcion - 1]["nombre"]

    motivo = input_texto_obligatorio("Ingrese el motivo de la consulta: ")

    nuevo_turno = {
        "paciente": mascota["nombre"],
        "id": id_mascota,
        "fecha": fecha,
        "hora": hora,
        "veterinario": veterinario,
        "motivo": motivo
    }

    turnos.append(nuevo_turno)
    guardar_datos_json(ruta_turnos, turnos)
    print(f"\nTurno reservado exitosamente para {mascota['nombre']} con {veterinario} el {fecha} a las {hora}.")

def consultar_turno():
    if not turnos:
        print("No hay turnos registrados.")
        return

    print("""
    --- Consultar Turnos ---
    1. Ver todos los turnos
    2. Filtrar por nombre de mascota
    3. Filtrar por nombre de veterinario
    4. Filtrar por fecha
    0. Volver
    """)

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        mostrar_todos_los_turnos(turnos)
    elif opcion == "2":
        nombre = input("Ingrese el nombre de la mascota: ")
        filtrar_turnos(nombre, "paciente")
    elif opcion == "3":
        nombre_vet = input("Ingrese el nombre del veterinario: ")
        filtrar_turnos(nombre_vet, "veterinario")
    elif opcion == "4":
        fecha = input("Ingrese la fecha (AAAA-MM-DD): ").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("Formato de fecha inválido.")
            return
        filtrar_turnos(fecha, "fecha")
    elif opcion == "0":
        return
    else:
        print("Opción inválida.")

def filtrar_turnos(valor, clave):
    valor = limpiar_texto(valor)
    resultados = [t for t in turnos if limpiar_texto(str(t.get(clave, ""))) == valor]

    if resultados:
        mostrar_todos_los_turnos(resultados)
    else:
        print("No se encontraron turnos con ese criterio.")
def mostrar_todos_los_turnos(lista_turnos):
    print("\n--- Lista de Turnos ---")
    for turno in lista_turnos:
        print(f"Mascota: {turno['paciente']}")
        print(f"ID Mascota: {turno['id']}")
        print(f"Fecha: {turno['fecha']}")
        print(f"Hora: {turno['hora']}")
        print(f"Veterinario: {turno['veterinario']}")
        print(f"Motivo: {turno['motivo']}")
        print("---------------------------")

def modificar_turno():
    print("\n--- Modificar Turno ---")
    if not turnos:
        print("No hay turnos para modificar.")
        return

    idx = seleccionar_turno()
    if idx is None:
        return

    turno_original = turnos[idx]
    turno_editado = turno_original.copy()

    modificar_campos_turno(turno_editado)

    if not es_turno_valido(turno_editado, idx):
        return

    if confirmar_guardado():
        turnos[idx] = turno_editado
        guardar_datos_json(ruta_turnos, turnos)
        print("Turno modificado exitosamente.")
    else:
        print("Cambios cancelados.")


def seleccionar_turno():
    for i, turno in enumerate(turnos):
        print(f"{i}. {turno['fecha']} {turno['hora']} - {turno['paciente']} con {turno['veterinario']}")
    idx = input_numero_entero("Seleccione el número de turno a modificar: ")
    if 0 <= idx < len(turnos):
        return idx
    print("Índice inválido.")
    return None


def modificar_campos_turno(turno):
    # Fecha
    nueva_fecha = input("Nueva fecha (AAAA-MM-DD): ").strip()
    if nueva_fecha:
        try:
            fecha_obj = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
            if fecha_obj.year >= 2025:
                turno["fecha"] = nueva_fecha
            else:
                print("El año debe ser 2025 o superior. Se mantiene la fecha anterior.")
        except ValueError:
            print("Formato inválido. Se mantiene la fecha anterior.")

    # Hora
    nueva_hora = input(f"Nueva hora (HH:MM, actual: {turno['hora']}): ").strip()
    if nueva_hora and re.match(r"^(0[8-9]|1[0-7]):[0-5][0-9]$", nueva_hora):
        turno["hora"] = nueva_hora

    # Motivo
    nuevo_motivo = input(f"Nuevo motivo (actual: {turno['motivo']}): ").strip()
    if nuevo_motivo:
        turno["motivo"] = nuevo_motivo

    # Cambiar veterinario
    if input("¿Desea cambiar el veterinario? (s/n): ").strip().lower() == "s":
        veterinarios = [u["nombre"] for u in usuarios if u["rol"] == "Veterinario"]
        for i, v in enumerate(veterinarios):
            print(f"{i + 1}. {v}")
        idx_vet = input_numero_entero("Seleccione el número del nuevo veterinario: ")
        if 1 <= idx_vet <= len(veterinarios):
            turno["veterinario"] = veterinarios[idx_vet - 1]


def es_turno_valido(turno, idx_original):
    fecha = turno["fecha"]
    hora = turno["hora"]
    vet_nombre = turno["veterinario"]
    dia_semana = obtener_dia_semana(fecha)

    vet = next((u for u in usuarios if u["nombre"] == vet_nombre and u["rol"] == "Veterinario"), None)
    if not vet:
        print("Veterinario no encontrado.")
        return False

    disponibilidad = vet.get("disponibilidad", {}).get(dia_semana, [])
    if not any(inicio <= hora <= fin for inicio, fin in (r.split("-") for r in disponibilidad)):
        print(f"❌ {vet_nombre} no está disponible el {dia_semana} a las {hora}.")
        return False

    conflicto = any(
        i != idx_original and t["veterinario"] == vet_nombre and t["fecha"] == fecha and t["hora"] == hora
        for i, t in enumerate(turnos)
    )
    if conflicto:
        print(f"❌ {vet_nombre} ya tiene un turno asignado ese día y hora.")
        return False

    return True


def obtener_dia_semana(fecha_str):
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    return dias[fecha.isoweekday() - 1]


def confirmar_guardado():
    return input("¿Desea guardar los cambios? (s/n): ").strip().lower() == "s"

def eliminar_turno():
    print("\n--- Eliminar Turno ---")
    if not turnos:
        print("No hay turnos registrados.")
        return

    # Mostrar todos los turnos numerados
    for i, turno in enumerate(turnos):
        print(f"{i}. {turno['fecha']} {turno['hora']} - {turno['paciente']} con {turno['veterinario']}")

    # Seleccionar turno por índice
    idx = input_numero_entero("Seleccione el número de turno a eliminar: ")
    if 0 <= idx < len(turnos):
        turno = turnos[idx]

        print("\n--- Turno seleccionado ---")
        print(f"Mascota: {turno['paciente']}")
        print(f"Fecha: {turno['fecha']}")
        print(f"Hora: {turno['hora']}")
        print(f"Veterinario: {turno['veterinario']}")
        print(f"Motivo: {turno['motivo']}")

        confirmar = input("¿Confirma que desea eliminar este turno? (s/n): ").strip().lower()
        if confirmar == "s":
            turnos.pop(idx)
            guardar_datos_json(ruta_turnos, turnos)
            print("Turno eliminado exitosamente.")
        else:
            print("Eliminación cancelada.")
    else:
        print("Índice inválido.")
