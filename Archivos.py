def cargar_informacion(nombre_archivo):
    ruta = sketchPath(nombre_archivo)
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        if linea.startswith("SALA"):
            _, numero = linea.split(",")
            numero = int(numero)
            i += 1

            while i < len(lineas) and not lineas[i].startswith("---"):
                if lineas[i].startswith("FUNCION"):
                    # Leer datos de la función
                    _, nombre, genero, duracion, precio = lineas[i].strip().split(",")
                    duracion = int(duracion)
                    precio = int(precio)
                    funcion = Funcion(nombre, genero, duracion, precio)
                    i += 1

                    # Leer todos los horarios asociados
                    while i < len(lineas) and lineas[i].startswith("HORARIO"):
                        _, horario = lineas[i].strip().split(",")
                        i += 1
                        asientos_plano = []
                        
                        for fila in range(8):
                            linea_asientos = lineas[i].strip()
                            for col, c in enumerate(linea_asientos):
                                num = fila * len(linea_asientos) + col + 1
                                disponible = (c == "0")   # 0 → libre, 1 → ocupado
                                asientos_plano.append(Seat(num=num, disponible=disponible))
                            i += 1
                        
                        funcion.horarios.append(horario)
                        funcion.asientos_horario.append(asientos_plano)

                    # Asignar función a la sala correspondiente
                    if numero == 1:
                        sala1.agregar_funcion(funcion)
                    elif numero == 2:
                        sala2.agregar_funcion(funcion)
                    elif numero == 3:
                        sala3.agregar_funcion(funcion)
                else:
                    i += 1
        i += 1

def guardar_informacion(nombre_archivo):
    ruta = sketchPath(nombre_archivo)
    lineas = []
    for num, sala in enumerate([sala1, sala2, sala3], start=1):
        lineas.append("SALA,"+str(num)+"\n")
        for funcion in sala.funciones:
            lineas.append("FUNCION,"+str(funcion.nombre)+","+str(funcion.genero)+","+str(funcion.duracion)+","+str(funcion.precio)+"\n")
            for i, horario in enumerate(funcion.horarios):
                lineas.append("HORARIO,"+str(horario)+"\n")
                asientos = funcion.asientos_horario[i]
                columnas = len(asientos) // 8
                for fila in range(8):
                    inicio = fila * columnas
                    fin = inicio + columnas
                    filaar = "".join("0" if asiento.disponible else "1" for asiento in asientos[inicio:fin])
                    lineas.append(filaar + "\n")
        lineas.append("---\n")
    with open(ruta, "w") as f:
        f.writelines(lineas)