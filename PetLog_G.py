from datetime import datetime
"""
--------------------------------------------------------------------------------------------------------
  Funciones para Eliminar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
def eliminar_duenio_o_mascota(duenios, mascotas):
    print("""¿Qué desea eliminar?
    1: Mascota
    2: Dueñx""")
    opcion = input("Ingrese el número de la opción: ").strip()

    if opcion == "1":
        id_mascota = input("Ingrese el ID de la mascota a eliminar: ").strip()
        while not id_mascota.isdigit():
            id_mascota = input("ID inválido. Ingrese un número: ").strip()
        id_mascota = int(id_mascota)
        eliminar_mascota(mascotas, id_mascota)

    elif opcion == "2":
        id_duenio = input("Ingrese el ID del dueñx a eliminar: ").strip()
        while not id_duenio.isdigit():
            id_duenio = input("ID inválido. Ingrese un número: ").strip()
        id_duenio = int(id_duenio)
        eliminar_duenio(duenios, mascotas,id_duenio)

    else:
        print("Opción inválida. No se realizó ninguna acción.")

def eliminar_mascota(mascotas, id_mascota):
    for mascota in mascotas:
        if mascota['id'] == id_mascota:
            mascotas.remove(mascota)
            print(f"Mascota con ID {id_mascota} eliminada exitosamente.")
            return
    print(f"No se encontró una mascota con ID {id_mascota}.")
def eliminar_duenio(duenios, mascotas, id_duenio):
    for duenio in duenios:
        if duenio['id'] == id_duenio:
            duenios.remove(duenio)
            print(f"Dueñx con ID {id_duenio} eliminado exitosamente.")
            break
    else:
        print(f"No se encontró un dueñx con ID {id_duenio}.")
        return
    
    for mascota in mascotas:
        if id_duenio in mascota['dueños']:
            mascota['dueños'].remove(id_duenio)
            print(f"Se quitó el dueñx {id_duenio} de la mascota '{mascota['nombre']}'.")

            if not mascota['dueños']:      # Si la mascota se quedó sin dueños
                print(f"La mascota '{mascota['nombre']}' se quedó sin dueñx.")
                nuevo_duenio = agregarDuenio(duenios)  
                mascota['dueños'].append(nuevo_duenio['id'])
                print(f"Se asignó un nuevo dueñx a '{mascota['nombre']}'.")

"""
--------------------------------------------------------------------------------------------------------
  Funciones para añadir visita médica
--------------------------------------------------------------------------------------------------------
"""
def registrarVisita(mascotas):
    #Solicitamos al usuario que ingrese el ID de la mascota
    mascota_id = input("Ingrese el ID de la mascota: ").strip()
    while not mascota_id.isdigit():
        print("El ID ingresado no es un ID váido")
        mascota_id = input("Ingrese el ID de la mascota: ").strip()

    #Una vez verificamos que lo ingresado es un dígito lo convertimos a entero
    mascota_id = int(mascota_id)

    #Registramos la nueva visita médica
    for mascota in mascotas:
        if mascota["id"] == mascota_id:
            visita = []
            fecha_actual = datetime.now().strftime("%d/%m/%Y")# Fecha automática

            motivo = input("Ingrese el motivo de la consulta: ").strip().lower()
            while not motivo:
                print("El motivo ingresado no es válido")
                motivo = input("Ingrese el motivo de la consulta: ").strip().lower()

            diagnostico = input("Ingrese el diagnóstico: ").strip()
            while not diagnostico:
                print("El diagnóstico no puede estar vacío.")
                diagnostico = input("Ingrese el diagnóstico: ").strip()

            tratamiento = input("Ingrese el tratamiento indicado: ").strip()
            while not tratamiento:
                print("El tratamiento no puede estar vacío.")
                tratamiento = input("Ingrese el tratamiento indicado: ").strip()

            visita = [fecha_actual, motivo, diagnostico, tratamiento]
            mascota['historial'].append(visita)
            print(f"Visita registrada exitosamente para {mascota['nombre'].capitalize()}.")
            return

"""
--------------------------------------------------------------------------------------------------------
  Funciones para agregar Mascotas y/o Dueñxs
--------------------------------------------------------------------------------------------------------
"""
#Menú para agregar Macota / Dueñx
def agregarMascotaODuenio(mascotas,duenios, tiposMascotas):
    while True:

        #Imprimimos el menú de opciones de Altas
        print("""\n--- Menú Agregar Mascotas y/o Dueñxs ---
                1: Agregar un nuevo dueñx
                2: Agregar una nueva mascota
                3: Volver al menú principal""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregarDuenio(duenios)
        elif opcion == "2":
            agregarMascota(mascotas, tiposMascotas)
        elif opcion == "3":
            return  # Volver al menú principal
        else:
            print("No se ha ingresado una opción válida, intente nuevamente.")

#Función donde generamos el id a asignarle a la nueva Mascota/Dueñx
def generarId(lista):
    if not lista: #En caso de que la lista este vacía le asignamos el id 1
        return 1
    else:
        #Recorremos la lista para buscar el id más alto y le sumamos 1
        return max(item["id"] for item in lista) + 1

#Funcion para agregar dueñx
def agregarDuenio(duenios):
    nuevo_id = generarId(duenios) #Generamos un nuevo ID para este duenio

    nombre = input("Nombre del dueño: ").strip()
    while not nombre:
        print("Por favor Ingrese un nombre")
        nombre = input("Nombre del dueño: ").strip()

    telefono = input("Teléfono: ").strip()
    while not telefono.isdigit():
        print("El teléfono debe contener solo valores numericos")
        telefono = input("Teléfono: ").strip()
    
    email = input("Correo electrónico: ").strip()
    while "@" not in email or "." not in email:
        print("El correo electrónico ingresado no esválido")
        email = input("Correo electrónico: ").strip()


    duenio = {
        "id": nuevo_id, 
        "nombre": nombre, 
        "telefono": telefono,
        "mail": email
        }
    duenios.append(duenio)
    print(f"El Dueñx {nombre} fue agregado con el ID {nuevo_id}.")
    
    
    print("\n¿Desea asociar este nuevo dueño a una mascota?")
    print("1: Sí")
    print("2: No")
    
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        asociarDuenioAMascotaExistente(nuevo_id)
    else:
        print("No se realizó ninguna asociación.")

    return duenio

#Función para buscar a las mascotas por el ID
def buscarMascotaPorId(id_mascota):
    for mascota in mascotas:
        if mascota["id"] == id_mascota:
            return mascota
    return None

#Funcion para asociar el dueño a la mascota
def asociarDuenioAMascotaExistente(nuevo_id):

    if not mascotas: #Verificamos si la lista de diccionarios está vacía (Devuelve falso si está vacía)
        print("No hay mascotas registradas.") #En caso de que este vacía mostramos por pantalla que no hay mascotas registradas
        return

    #Solicitamos al usuario que ingrese el ID de masocta al que queremos asociar
    mascota_id = input("Ingrese el ID de la mascota a asociar: ").strip()
    while not mascota_id.isdigit():
        print("El ID ingresado no es un ID váido")
        mascota_id = input("Ingrese el ID de la mascota a asociar: ").strip()

    mascota = buscarMascotaPorId(int(mascota_id))
    #Si se encuentra la mascota procedemos a agregar al dueño a la mascota
    if mascota:
        mascota["dueños"].append(nuevo_id)
        print(f"Dueño asociado correctamente a {mascota['nombre']}.")
        return
    else:
        print("No existe una mascota con el ID ingresado")
        return

#Función para agregar mascota
def agregarMascota(mascotas, tiposMascotas):
    nuevo_id = generarId(mascotas) #Generamos un nuevo ID para esta mascota

    nombre = input("Nombre de la mascota: ").strip()
    while not nombre:
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre de la mascota: ").strip()


    tipo = input("Ingrese el tipo de mascota: ").strip().title()
    while tipo not in tiposMascotas:
        print("El tipo de mascota es inválido, por faavor seleccionar un tipo de mascota permitido")
        print(f"Tipos válidos: ", ".join(tiposMascotas)")
        tipo = input("Ingrese el tipo de mascota: ").strip().lower()
    
    edad = input("Ingrese la edad de la mascota ").strip()
    while not edad.isdigit():
        print("E")
        edad = input("La edad solo puede ser un valor numérico").strip()

    mascota = {
        "id": nuevo_id, 
        "nombre": nombre, 
        "tipo": tipo,
        "edad": edad,
        "dueños" : [],
        "historial" : []
        }
    mascotas.append(mascota)

    print(f"La mascota {nombre} fue agregada con el ID {nuevo_id}.")
    
    print("\n¿Desea asociar esta nueva mascota a un dueño existente?")
    print("1: Sí")
    print("2: No")
    
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        asociarMascotaADuenioExistente(nuevo_id)
    else:
        print("No se realizó ninguna asociación.")

    return

def buscarDuenioPorId(id_duenio):
    for duenio in duenios:
        if duenio["id"] == id_duenio:
            return duenio
    return None

def asociarMascotaADuenioExistente(nuevo_id):
    if not duenios:
        print("No hay dueños registrados.")
        return

    print("Dueños disponibles:")
    for d in duenios:
        print(f"ID {d['id']}: {d['nombre']}")

    dueno_id = input("Ingrese el ID del dueño a asociar: ").strip()
    if not dueno_id.isdigit():
        print("ID inválido.")
        return

    duenio = buscarDuenioPorId(int(dueno_id))
    mascota = buscarMascotaPorId(nuevo_id)
    if duenio and mascota:
        mascota["dueños"].append(int(dueno_id))
        print(f"Mascota asociada correctamente a {duenio['nombre']}.")
    else:
        print("No se encontró dueño o mascota.")

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
            #Utilizamos un booleano para corroborar que el dueño exista
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
        listaIdUsuarios=[]
        for usuario in datosUsuarios:
            listaIdUsuarios.append( usuario["id"])

        if nuevoId not in listaIdUsuarios:
            individuo["id"] = nuevoId
            flag = True
            return individuo
#reutilizacion cambio nombre

def cambioNombre(individuo):
    nuevoNombre = input("ingresar nombre: ")
    while not nuevoNombre.isalpha(): # en caso de tener caracter numerico vuelve solicitar el nombre
        print("Nombre inválido: solo letras")
        nuevoNombre = input("ingresar nombre valido: ")
    individuo["nombre"] = nuevoNombre.title()
    return individuo



# se podria usar lambda
def muestraDatosMascota(mascota):
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


# ae podria usar lambda
def muestraDatosDuenios(duenio):
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

#Crear Usuario o inicio sesion

#Log In
def crearUsuario():
    try:
        usuario=input("Ingresar nombre de usuario: ")
        usuario.replace(" ","")
        while not usuario.isalpha(): # en caso de tener caracter numerico vuelve solicitar el nombre
            print("Nombre inválido: solo letras")
            usuario=input("Ingresar Usuario correctamente: ")
        
        contrasenia=input("Ingresar contrasenia: ")
        while contrasenia.length() <8 and contrasenia.length() >10 and not contrasenia.isalnum():
            contrasenia=input("Ingresar contrasenia correcta: ") 
        usuario.title()

        sesion=(usuario,contrasenia)

        while flag!=True:
            if sesion not in usuariosRegistrados:
                usuariosRegistrados.append(sesion)
                print(f"Bievenido {usuario}!!!")
                flag =True
    except(IOError):
        print("Error, reinicie el programa")

def inicioDeSesion():
    try:
        flag=False
        usuario=input("Ingresar Usuario: ")
        contrasenia=input("Ingresar contrasenia: ")
        sesion=(usuario,contrasenia)

        while flag!=True:
            if sesion in usuariosRegistrados:
                print(f"Bievenido {usuario}!!!")
                flag =True
            else:
                print("Error en usuario o contrasenia, ingrese nuevamente los datos")
                usuario=input("Ingresar Usuario: ")
                contrasenia=input("Ingresar contrasenia: ")
    except(IOError):
        print("Error, reinicie el programa")

    return flag


            


print("Seleccione 1 si desea Iniciar Sesion")
print("Seleccione 2 si desea registrarse")
print("Seleccione 3 si desea Cerra el programa")

try:
        
    usuariosRegistrados=[("Pepito","1234"),("Juanito","juan23"),("Alejandro","dortmund11")]
    opcion=int(input("ingresar opcion deseada: "))

    while True:
        if opcion ==1:
            inicioDeSesion()
            break
        if opcion==2:
            crearUsuario()
            break
        if opcion ==0:
            print("Hasta la proxima!!!")
            break

        opcion=int(input("ingresar nueva opcion: "))

except(IOError):
    print("Error, reinicie el programa")





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
        eliminar_duenio_o_mascota(duenios,mascotas)
    
    elif opcion == 5:
        print("Ha seleccionado registrar una nueva visita médica") 
        registrarVisita(mascotas)
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