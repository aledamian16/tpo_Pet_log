import re
import os
from datetime import datetime

"""
--------------------------------------------------------------------------------------------------------
  Funciones auxiliares y validación
--------------------------------------------------------------------------------------------------------
"""
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

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Eliminar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_eliminar(duenios, mascotas):
    print("""¿Qué desea eliminar?
    1: Mascota
    2: Dueñx""")
    opcion = input("Ingrese el número de la opción: ").strip()

    if opcion == "1":
        id_mascota = input("Ingrese el ID de la mascota a eliminar: ")
        id_mascota = input_id_valido(id_mascota)
        eliminar_mascota_por_id(mascotas, id_mascota)

    elif opcion == "2":
        id_duenio = input("Ingrese el ID del dueñx a eliminar: ")
        id_duenio = input_id_valido(id_duenio)
        if eliminar_duenio_por_id(duenios, id_duenio):
            actualizar_mascotas_por_duenio_eliminado(mascotas, id_duenio, duenios)
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
                nuevo_duenio = agregarDuenio(duenios, mascotas)
                mascota["dueños"].append(nuevo_duenio["id"])
                print(f"Se asignó un nuevo dueñx a '{mascota['nombre']}'.")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para añadir visita médica
--------------------------------------------------------------------------------------------------------
"""
def registrar_visita(mascotas):
    try:
        id_mascota = input("Ingrese el ID de la mascota: ")
        id_mascota = input_id_valido(id_mascota)
        mascota = buscar_por_id(mascotas, id_mascota)
        if mascota:
            visita = crear_visita()
            mascota["historial"].append(visita)
            print(f"Visita registrada exitosamente para {mascota['nombre'].capitalize()}.")
        else:
            print("No se encontró una mascota con ese ID.")
    except Exception as e:
        print(f"Ocurrió un error al registrar la visita: {e}")

def crear_visita():
    fecha = datetime.now().strftime("%d/%m/%Y")
    motivo = input_texto_obligatorio("Ingrese el motivo de la consulta: ").lower()
    diagnostico = input_texto_obligatorio("Ingrese el diagnóstico: ")
    tratamiento = input_texto_obligatorio("Ingrese el tratamiento indicado: ")
    return [fecha, motivo, diagnostico, tratamiento]
            
"""
--------------------------------------------------------------------------------------------------------
  Funciones para agregar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def menu_agregar(mascotas, duenios, tipos_mascotas):
    while True:
        print("""\n--- Menú Agregar ---
                1: Agregar dueñx
                2: Agregar mascota
                3: Volver al menú principal""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_duenio(duenios, mascotas)
        elif opcion == "2":
            agregar_mascota(mascotas, duenios, tipos_mascotas)
        elif opcion == "3":
            return # Volver al menú principal
        else:
            print("Opción inválida.")

#Función donde generamos el id a asignarle a la nueva Mascota/Dueñx
def generarId(lista):
    if not lista: #En caso de que la lista este vacía le asignamos el id 1
        return 1
    else:
        #Recorremos la lista para buscar el id más alto y le sumamos 1
        return max(item["id"] for item in lista) + 1
    
def agregar_duenio(duenios, mascotas):
    nuevo_id = generar_id(duenios)

    nombre = input_texto_obligatorio("Nombre del dueñx: ")
    telefono = input_texto_obligatorio("Teléfono: ")
    while not telefono.isdigit():
        print("El teléfono debe contener solo números.")
        telefono = input_texto_obligatorio("Teléfono: ")

    email = input_texto_obligatorio("Correo electrónico: ")
    while "@" not in email or "." not in email:
        print("Correo electrónico inválido.")
        email = input_texto_obligatorio("Correo electrónico: ")

    duenio = {
        "id": nuevo_id,
        "nombre": nombre,
        "telefono": telefono,
        "mail": email
    }
    duenios.append(duenio)
    print(f"Dueñx '{nombre}' agregado con ID {nuevo_id}.")

    # Asociar a mascota
    if mascotas:
        opcion = input("¿Desea asociar este nuevo dueñx a una mascota? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            asociar_duenio_a_mascota(nuevo_id, mascotas)

    return duenio

def agregar_mascota(mascotas, duenios, tipos_mascotas):
    nuevo_id = generar_id(mascotas)

    nombre = input_texto_obligatorio("Nombre de la mascota: ")

    tipo = input("Tipo de mascota: ").strip().title()
    while tipo not in tipos_mascotas:
        print(f"Tipo inválido. Tipos válidos: {', '.join(tipos_mascotas)}")
        tipo = input("Tipo de mascota: ").strip().title()

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

"""
--------------------------------------------------------------------------------------------------------
  Funciones para Modificar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
#funciones reutilizables


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

#Función mostrar todas las mascotas en la lista de mascotas
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

#Función para mostrar todos los dueños de la lista de diccionarios "duenios"
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
MENU - PROGRAMA PRINCIPAL
--------------------------------------------------------------------------------------------------------
"""
'''
#Print del Menú
print("¡Bienvenido!\n")
print("""--- Seleccione una opción: ---\n
  1: Consultar Mascota y/o Dueñx\n
  2: Modificar Mascota y/o Dueñx\n
  3: Agregar Mascota y/o Dueñx\n
  4: Eliminar Mascota y/o Dueñx\n
  5: Registrar nueva visita médica\n
  0: Finalizar Sesión""")

opcion = int(input("\nOpción: "))


#Tupla con los tipos de mascotas
tiposMascotas = ("Perro" , "Gato", "Ave", "Reptil", "Roedor", "Otro")

#Lista de mascotas
mascotas = [
    {
        "id": 1,
        "nombre": "parda",
        "tipo": "Perro",
        "edad": 5,
        "dueños": [1, 2],  # Referencia a ID de dueños
        "historial": [["12/04/2001" , "Vacuna" ,"Recibida", "La mascota fue vacunada con una antirabica"] ,["12/05/2012" , "Control" ,"Recibida", "Control de mascota, peso 15kg"]]
    },
    {
        "id": 2,
        "nombre": "sasha",
        "tipo": "Gato",
        "edad": 7,
        "dueños": [3],
        "historial": [["12/04/2001" , "Vacuna","Recibida" , "La mascota fue vacunada con una antirabica"] ,["12/05/2012" , "Control" ,"Recibida", "Control de mascota, peso 15kg"]]
    },
    {
        "id": 3,
        "nombre": "bulma",
        "tipo": "Perro",
        "edad": 12,
        "dueños": [2],
        "historial": [["12/04/2001" , "Vacuna" , "Recibida" ,"La mascota fue vacunada con una antirabica"] ,["13/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["14/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["15/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["16/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["17/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["18/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["19/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["20/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["21/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["22/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["23/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["24/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["25/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],["26/05/2012" , "Control" ,"Recibida" , "Control de mascota, peso 15kg"],]
    }
    ]

#Lista de dueños
duenios = [
    {
        "id": 1,  #ID del dueño
        "nombre": "jorge rodriguez",
        "telefono": "5490862451",
        "mail": "pepe@gmail.com"
    },
    {
        "id": 2,
        "nombre": "bautista rojas",
        "telefono": "1146376425",
        "mail": "laurojas@uade.edu.ar"
    },
    {
        "id": 3,
        "nombre": "maria eugenia cobas",
        "telefono": "1556788892",
        "mail": "mecobas@hotmail.com"
    }

]


#Bucle para selección de Opción y terminación de sesión
while opcion != 0:
    if opcion == 1:
        print("Ha seleccionado Consultar Mascota y/o Dueñx")
        consultarInformacion(mascotas, duenios)
        
    elif opcion == 2:
        print("Ha seleccionado Modificar Mascota y/o Dueñx")
        modificarInformacion(mascotas, duenios)
    elif opcion == 3:
        print("Ha seleccionado Agregar Nueva Mascota y/o Dueñx")
        agregarMascotaODuenio(mascotas, duenios, tiposMascotas)

    elif opcion == 4:
        print("Ha seleccionado Eliminar Mascota y/o Dueñx")
        menu_eliminar(duenios,mascotas)
    
    elif opcion == 5:
        print("Ha seleccionado registrar una nueva visita médica") 
        registrar_visita(mascotas)
    else:
        print("No ingreso una opción válida. Por favor volver a ingresar una opción del listado.")

    print("""\n--- Seleccione una opción: ---\n
        1: Consultar Mascota y/o Dueñx\n
        2: Modificar Mascota y/o Dueñx\n
        3: Agregar Mascota y/o Dueñx\n
        4: Eliminar Mascota y/o Dueñx\n
        5: Registrar nueva visita médica\n
        0: Finalizar Sesión""")

    opcion = int(input("Opción: "))
print("\nSesión Finalizada")

'''
"""
--------------------------------------------------------------------------------------------------------
  Menú y Funciones de Log In y Sign Up
--------------------------------------------------------------------------------------------------------
"""
# Ruta del archivo con los usuarios registrados
ruta_usuarios = "Archivos/Usuarios/usuariosRegistrados.txt"

# Función para cargar usuarios desde el archivo
def cargar_usuarios(ruta_usuarios):
    usuarios = {}
    try:
        archivo = open(ruta_usuarios, "r", encoding="utf-8")
        for linea in archivo:
            if "," in linea:
                usuario, contrasenia = linea.strip().split(",", 1)
                usuarios[usuario] = contrasenia
        archivo.close()
    except FileNotFoundError:
        print("Archivo de usuarios no encontrado. Se iniciará vacío.")
    return usuarios

# Función para guardar un nuevo usuario
def guardar_nuevo_usuario(usuario, contrasenia, ruta):
    try:
        archivo = open(ruta, "a", encoding="utf-8")
        archivo.write(f"{usuario},{contrasenia}\n")
        archivo.close()
    except Exception as e:
        print(f"No se pudo guardar el usuario: {e}")

def validacionNombreUsuario():
    while True:
        usuario = input("Ingresar nombre de usuario (0 para cancelar): ").strip()
        if usuario:
            return usuario
        print("El nombre de usuario no puede estar vacío.")

def validacionContrasenia():
    while True:
        contrasenia = input("Ingresar contraseña (mínimo 8 caracteres alfanuméricos, 0 para cancelar): ").strip()
        if contrasenia == "0":
            return "0"
        if len(contrasenia) >= 8 and contrasenia.isalnum():
            return contrasenia
        print("La contraseña debe tener al menos 8 caracteres y contener solo letras o números.")

def crear_usuario(usuarios, ruta_usuarios):
    print("\n--- Registro de nuevo usuario (Ingrese 0 para volver al menú) ---")
    
    usuario_valido = False
    while not usuario_valido:
        usuario = validacionNombreUsuario()
        if usuario == "0":
            print("Registro de usuario cancelado\n")
            return
        
        if usuario in usuarios:
            print(f"\nEl nombre de usuario '{usuario}' ya existe. Por favor intente con otro nombre de usuario.")
        else:
            usuario_valido = True  #No existe un usuario con ese nombre

    contrasenia = validacionContrasenia()
    if contrasenia == "0":
        print("Registro de usuario cancelado\n")
        return
    
    usuarios[usuario] = contrasenia
    guardar_nuevo_usuario(usuario, contrasenia, ruta_usuarios)
    print(f"¡Usuario '{usuario}' registrado correctamente!")

def inicio_sesion(usuarios):
    print("\n--- Inicio de sesión (Ingrese 0 para volver al menú) ---")
    while True:
        usuario = input("Usuario: ").strip()
        if usuario == "0":
            print("Inicio de sesión cancelado\n")
            return False

        contrasenia = input("Contraseña: ").strip()
        if contrasenia == "0":
            print("Inicio de sesión cancelado\n")
            return False
        
        if usuarios.get(usuario) == contrasenia:
            print(f"¡Bienvenido, {usuario}!")
            return True
        else:
            print("Usuario o contraseña incorrectos. Intente nuevamente.")

def menu_inicio(ruta_usuarios):
    usuariosRegistrados = cargar_usuarios(ruta_usuarios)

    print("""--- ¡Bienvenido! ---\n
1. Iniciar sesión\n
2. Registrarse\n
0. Salir\n""")

    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                if inicio_sesion(usuariosRegistrados):
                    return True
            elif opcion == 2:
                crear_usuario(usuariosRegistrados,ruta_usuarios)
                usuariosRegistrados = cargar_usuarios(ruta_usuarios)  #recargar usuarios después de registrar
            elif opcion == 0:
                print("Sesión Finalizada.")
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
menu_inicio(ruta_usuarios)