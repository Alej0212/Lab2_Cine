import sys

pantalla = 0
seleccion1 = -1
seleccion2 = -1
icons = []
fonts = []
salas = ["Sala 1", "Sala 2", "Sala 3"]
horarios = ["Manana", "Tarde", "Noche"]
horas1 = ["9 AM", "10 AM", "11 AM", "12 AM"]
horas2 = ["1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM"]
horas3 = ["7 PM", "8 PM", "9 PM", "10 PM", "11 PM", "12 PM"]
hora_actual1 = 0 
hora_actual2 = 0
hora_actual3 = 0
arrastrando1 = False
arrastrando2 = False
arrastrando3 = False
funcion_seleccionada = None
asientos_seleccionados = []




#Clases y listas
class Seat:
      def __init__(self, num = None, disponible  = None):
        self.num = num
        self.disponible = disponible
      
      def ocupar(self):
        self.disponible = False
      
      def desocupar(self):
        self.disponible = True





class Sala:
    def __init__(self, num_filas, num_asientos):
        self.num_filas = num_filas
        self.num_asientos = num_asientos
        self.ganancias = 0
        self.personas = 0
        self.asientos = []
        self.funciones = []
        self.crear_sala()


    def crear_sala(self):
      for i in range(self.num_filas * self.num_asientos):
        asiento = Seat(i + 1)
        self.asientos.append(asiento)
    
        
                
    def agregar_funcion(self, funcion):
        self.funciones.append(funcion)



    def mostrar_funciones(self):
        print("\n=== Funciones en esta sala ===")
        for funcion in self.funciones:
            print("\nPelícula: " + funcion.nombre)
            print("Género: " + funcion.genero)
            print("Duración: " + str(funcion.duracion) + " min")
            print("Horarios:")
            
            if funcion.horarios:
                for i in range(len(funcion.horarios)):
                    horario = funcion.horarios[i]
                    if i < len(funcion.asientos_horario):
                        disp = funcion.asientos_horario[i]
                    else:
                        disp = "N/A"
                    print("  - " + horario + " (Asientos disponibles: " + str(disp) + ")")
            else:
                print("  - No hay horarios registrados")
    
    
    
    def contener_funcion(self, funcion):
        return funcion in self.funciones        





class Funcion:
    def __init__(self, nombre, genero, duracion, precio):
        self.nombre = nombre
        self.genero = genero
        self.duracion = duracion
        self.precio = precio
        self.horarios = []
        self.asientos_horario = []

    def agregar_horario(self, horario, cantidad_asientos):
        self.horarios.append(horario)
        asientos = [Seat(i + 1) for i in range(cantidad_asientos)]
        self.asientos_horario.append(asientos)
        
    
    
    def mostrar_asientos(self, horario):
        if horario in self.horarios:
            indice = self.horarios.index(horario)
            asientos = self.asientos_horario[indice]
            print("Asientos para el horario: " + horario)
            for asiento in asientos:
                estado = "Disponible" if asiento.disponible else "Ocupado"
                print("Asiento: " + asiento.num + "estado")
        else:
            print("Horario no encontrado.")

    def ocupar_asiento(self, horario, numero_asiento):
        if horario in self.horarios:
            indice = self.horarios.index(horario)
            asientos = self.asientos_horario[indice]
            for asiento in asientos:
                if asiento.num == numero_asiento:
                    if asiento.disponible:
                        asiento.ocupar()
                        print("Asiento " + str(numero_asiento) + " ocupado en horario " + horario)
                        return
                    else:
                        print("Asiento " + str(numero_asiento) + " ya está ocupado")
                        return
            print("Asiento " + str(numero_asiento) + " no encontrado en el horario " + horario)
        else:
            print("Horario no encontrado.")

    def desocupar_asiento(self, horario, numero_asiento):
        if horario in self.horarios:
            indice = self.horarios.index(horario)
            asientos = self.asientos_horario[indice]
            for asiento in asientos:
                if asiento.num == numero_asiento:
                    if not asiento.disponible:
                        asiento.desocupar()
                        print("Asiento " + str(numero_asiento) + " desocupado en horario " + horario)
                        return
                    else:
                        print("Asiento " + str(numero_asiento) + " ya está dsiponible")
                        return
            print("Asiento " + str(numero_asiento) + " no encontrado en el horario " + horario)
        else:
            print("Horario no encontrado.")
    


    def asientos_disponibles(self, index_horario):
        asientos = self.asientos_horario[index_horario]
        return sum(1 for asiento in asientos if asiento.disponible)
    
    
    
    def asientos_ocupados(self, horario):
        if horario not in self.horarios:
            print("Horario no encontrado.")
            return []
        
        indice = self.horarios.index(horario)
        asientos = self.asientos_horario[indice]
    
        asientos_ocupados = []
        for asiento in asientos:
            if not asiento.disponible:
                asientos_ocupados.append(asiento.num)
    
        return asientos_ocupados
    
    
    
    

#Funciones archivos
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
                    _, nombre, genero, duracion, precio = lineas[i].strip().split(",")
                    duracion = int(duracion)
                    precio = int(precio)
                    funcion = Funcion(nombre, genero, duracion, precio)
                    i += 1

                    while i < len(lineas) and lineas[i].startswith("HORARIO"):
                        _, horario = lineas[i].strip().split(",")
                        i += 1
                        asientos_plano = []
                        
                        for fila in range(8):
                            linea_asientos = lineas[i].strip()
                            for col, c in enumerate(linea_asientos):
                                num = fila * len(linea_asientos) + col + 1
                                disponible = (c == "0")
                                asientos_plano.append(Seat(num=num, disponible=disponible))
                            i += 1
                        
                        funcion.horarios.append(horario)
                        funcion.asientos_horario.append(asientos_plano)

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



def ganancias():
    for sala in [sala1, sala2, sala3]:
        sala.personas = 0
        sala.ganancias = 0.0
    for sala in [sala1, sala2, sala3]:
        for funcion in sala.funciones:
            for i, horario in enumerate(funcion.horarios):
                asientos = funcion.asientos_horario[i]
                for asiento in asientos:
                    if asiento.disponible == False:
                        sala.personas = sala.personas + 1
                        #print(sala.personas)
                        sala.ganancias = sala.ganancias + funcion.precio
                        #print(sala.ganancias)





#Funciones Processing
def setup():
    fullScreen()
    global icons
    global fonts
    global sala1, sala2, sala3
    icons.append(loadImage("icon3.png"))
    icons.append(loadImage("icon8.png"))
    icons.append(loadImage("icon9.png"))
    icons.append(loadImage("icon10.png"))
    icons.append(loadImage("icon12.png"))
    icons.append(loadImage("icon13.png"))
    
    fonts.append(createFont("font3.ttf", 28))
    fonts.append(createFont("font2.ttf", 60))
    fonts.append(createFont("font4.ttf", 28))
    
    sala1 = Sala(10, 8)
    sala2 = Sala(10, 8)
    sala3 = Sala(10, 8)
    cargar_informacion("Informacion.txt")




def draw():
    if pantalla == 0:
        inicio()
    elif pantalla == 1:
        cartelera()
    elif pantalla == 2:
        entradas()
    elif pantalla == 3:
        informacion()


    


#Pantallas
def inicio():
    background(180, 8, 0)
    fill(0)
    noStroke()
    rect(0 , 0, width, height*0.125)
    rect(0, height*0.875, width, height*0.125)
    
    icons[0] = resize_img(icons[0], 100)
    icons[1] = resize_img(icons[1], 725)
    image(icons[0], 0, 10)
    image(icons[1], 0, height*0.12)
    
    stroke(0)
    fill(255, 255, 255)
    textFont(fonts[0])
    textSize(28)
    text("About", width*0.75, height*0.075)
    text("Home", width*0.83, height*0.075)
    text("Contact", width*0.91, height*0.075)
    
    textFont(fonts[1])
    textSize(60)
    text("Cine Cultural", width*0.75, height*0.25)
    text("Barranquilla", width*0.8, height*0.36)
    
    boton("CARTELERA", width*0.63, height*0.55, 360, 60)
    #boton("ENTRADAS", width*0.63, height*0.55, 360, 60)
    boton("INFORMACION", width*0.63, height*0.65, 360, 60)
    
    icons[5] = resize_img(icons[5], 70)
    image(icons[5], width*0.94, height*0.78)
    


def cartelera():
    background(180, 8, 0)
    stroke(0)
    fill(255, 255, 255)
    textFont(fonts[0])
    textSize(60)
    text("CARTELERA", width*0.5, height*0.1)
    
    fill(220)
    stroke(200)
    strokeWeight(1)
    rect(width*0.025 , height*0.2, 300, 60)
    fill(0)
    textSize(30)
    text("FILTROS", width*0.135, height*0.24)
    
    stroke(0)
    strokeWeight(2)
    fill(255)
    rect(width*0.025, height*0.3, 300, 190)
    fill(0)
    noStroke()
    circle(width*0.05, height*0.33, 20)
    text("SALAS", width*0.1, height*0.33)
    radio_button(salas, width*0.08, height*0.38, 20, seleccion1)
    stroke(0)
    strokeWeight(2)
    fill(255)
    rect(width*0.025, height*0.3 + 170, 300, 235)
    fill(0)
    noStroke()
    circle(width*0.05, height*0.33 + 167, 20)
    textFont(fonts[0])
    text("HORARIO", width*0.1, height*0.55)
    radio_button(horarios, width*0.08, height*0.62, 20, seleccion2)
    if seleccion2 == 0:
        barra_horas(width*0.05, height*0.5 + 190, 230, 25, horas1, hora_actual1, arrastrando1)
    elif seleccion2 == 1: 
        barra_horas(width*0.05, height*0.5 + 190, 230, 25, horas2, hora_actual2, arrastrando2)
    elif seleccion2 == 2:
        barra_horas(width*0.05, height*0.5 + 190, 230, 25, horas3, hora_actual3, arrastrando3)
            
    if seleccion1 == 0:
        sala_mostrar = sala1
    elif seleccion1 == 1:
        sala_mostrar = sala2
    elif seleccion1 == 2:
        sala_mostrar = sala3
    else:
        sala_mostrar = None
    
    if seleccion2 != -1:
        if seleccion2 == 0:
            hora_minima = 9 + hora_actual1
        elif seleccion2 == 1:
            hora_minima = 13 + hora_actual2
        else:
            hora_minima = 19 + hora_actual3
    
    contador = 0
    for sala in [sala1, sala2, sala3]:
        if sala_mostrar is None or sala == sala_mostrar:
            for funcion in sala.funciones:
                cumple_horario = True
    
                if seleccion2 != -1:
                    cumple_horario = False
                    for horario in funcion.horarios:
                        hora_funcion = hora_24h(horario)
                        
                        if hora_funcion != -1 and hora_funcion >= hora_minima:
                            cumple_horario = True
                            break
                
                if cumple_horario:
                    x = width * 0.27 + (contador % 3) * 330
                    y = height * 0.2 + (contador // 3) * 280
                    disponibles = [funcion.asientos_disponibles(i) for i in range(len(funcion.horarios))]
                    cartel_pelicula(x, y, 300, 250, funcion.nombre, funcion.genero, 
                                    funcion.duracion, str([sala1, sala2, sala3].index(sala) + 1), 
                                    [str(h) for h in funcion.horarios], disponibles, funcion)
                    contador += 1


    
    icons[2] = resize_img(icons[2], 70)
    image(icons[2], width*0.94, height*0.89)
    
    
    
def entradas():
    background(238, 195, 72)
    stroke(0)
    fill(255)
    textFont(fonts[0])
    textSize(60)
    textAlign(CENTER, CENTER)
    text("ENTRADAS", width*0.5, height*0.1)
    noStroke()
    rect(width*0.05, height*0.2, width - width*0.1, 615, 10)
    fill(180, 8, 0)
    textSize(50)
    text(funcion_seleccionada.nombre, width*0.5, height*0.25)
    textFont(fonts[0])
    textAlign(LEFT)
    if funcion_seleccionada:
        sala = obtener_sala(funcion_seleccionada)
        if sala:
            num_sala = [sala1, sala2, sala3].index(sala) + 1
            text("Sala: " + str(num_sala), width*0.1, height*0.27)  
    disponibles = [funcion_seleccionada.asientos_disponibles(i) for i in range(len(funcion_seleccionada.horarios))]  
    asientos_texto = ", ".join(str(num) for num in disponibles)
    horarios_texto = join(funcion_seleccionada.horarios, ", ")
    textFont(fonts[2])
    fill(0)
    text("Asientos: ", width*0.1, height*0.34)
    text(asientos_texto, width*0.185, height*0.34)
    text("Precio: ", width*0.1, height*0.4)
    if asientos_seleccionados:
        precio_total = funcion_seleccionada.precio * len(asientos_seleccionados)
        text("$ " + str(precio_total), width*0.165, height*0.4)
    else:
        text("$ 0", width*0.165, height*0.4)
    text("Horario: ", width*0.1, height*0.46)
    text(horarios_texto, width*0.17, height*0.46)
    textAlign(CENTER, CENTER)
    
    textSize(20)
    stroke(10)
    fill(245, 245, 220)
    textAlign(LEFT)
    rect(width*0.1, height*0.6, 50, 50, 10)
    fill(0)
    text("Disponibles", width*0.15, height*0.64)
    fill(180, 8, 0)
    rect(width*0.1, height*0.7, 50, 50, 10)
    fill(0)
    text("Vendido", width*0.15, height*0.74)
    fill(238, 195, 72)
    rect(width*0.1, height*0.8, 50, 50, 10)
    fill(0)
    text("Seleccionado", width*0.15, height*0.84)
    
    asientos(550, 130, 50, 50, 10, 8)
    if len(asientos_seleccionados) > 0:
        fill(0)
        textAlign(LEFT)
        text("Asientos seleccionados: " + ", ".join(map(str, sorted(asientos_seleccionados))), 
             width*0.1, height*0.55)
    
    fill(0)
    rect(550, 705, 590, 60, 10)
    textAlign(CENTER, CENTER)
    fill(255)
    textSize(40)
    text("Pantalla", 855, 740)
    
    boton_entradas("Comprar", width * 0.1, height * 0.9, 360, 60)
    
    icons[2] = resize_img(icons[2], 70)
    image(icons[2], width*0.94, height*0.89)
    
    
    
def informacion():
    background(180, 8, 0)
    fill(255)
    rect(45, 50, width*0.11, height)
    rect(1165, 50, width*0.11, height)
    image(icons[3], 0, 50)
    image(icons[3], 1120, 50)
    fill(0)
    noStroke()
    rect(0 , 0, width, height*0.125)
    rect(0, height*0.875, width, height*0.125)   
    fill(255)
    textFont(fonts[0])
    textSize(60)
    textAlign(CENTER, CENTER)
    text("INFORMACION", width*0.5, height*0.2)
    
    fill(255)
    stroke(255)
    strokeWeight(5)
    rect(230, 200, width*0.2, height*0.07, 20)
    rect(545, 200, width*0.2, height*0.07, 20)
    rect(860, 200, width*0.2, height*0.07, 20)
    fill(180, 8, 0)
    textFont(fonts[2])
    textSize(30)
    text("Sala 1", width*0.27, height*0.295)
    text("Sala 2", width*0.27 + 315, height*0.295)
    text("Sala 3", width*0.27 + 630, height*0.295)
    icons[4] = resize_img(icons[4], 200)
    image(icons[4], 260, 255)
    image(icons[4], 575, 255)
    image(icons[4], 890, 255)
    fill(0)
    textFont(fonts[0])
    textSize(50)
    text("1", width*0.263, height*0.413)
    text("2", width*0.263 + 315, height*0.413)
    text("3", width*0.263 + 630, height*0.413)
    
    fill(180, 8, 0)
    stroke(255)
    strokeWeight(3)
    rect(230, 470, width*0.12, height*0.05, 10)
    rect(230, 530, width*0.12, height*0.05, 10)
    rect(545, 470, width*0.12, height*0.05, 10)
    rect(545, 530, width*0.12, height*0.05, 10)
    rect(860, 470, width*0.12, height*0.05, 10)
    rect(860, 530, width*0.12, height*0.05, 10)
    fill(255)
    textSize(20)
    text("Personas", width*0.23, height*0.6355)
    text("Ganancias", width*0.23, height*0.715)
    text(str(sala1.personas), width*0.24, height*0.6355)
    text("Personas", width*0.23 + 315, height*0.6355)
    text("Ganancias", width*0.23 + 315, height*0.715)
    #
    text("Personas", width*0.23 + 630, height*0.6355)
    text("Ganancias", width*0.23 + 630, height*0.715)
    #
    
    textFont(fonts[0])
    textSize(40)
    text("Total", width*0.4, height*0.82)
    fill(238, 195, 72)
    stroke(0)
    rect(width*0.4 + 60, height*0.795, 250, 40, 20)
    textSize(30)
    fill(0)
    text("$ ", width*0.47, height*0.82)
    #
    
    fill(180, 8, 0)
    rect(width*0.935, height*0.775, 85, 75)
    icons[2] = resize_img(icons[2], 70)
    image(icons[2], width*0.94, height*0.78)
    
    


#Funciones gráficas
def resize_img(imagen, ancho):
    copia = imagen.get()
    
    ratio = float(copia.height) / float(copia.width)
    alto = int(ancho * ratio)
    copia.resize(ancho, alto)
    
    return copia 



def boton(texto, x, y, ancho, alto):
    mouse = (mouseX > x and mouseX < x + ancho and 
             mouseY > y and mouseY < y + alto)
    if mouse:
        fill(220)
    else:
        fill(255) 
    stroke(200)
    strokeWeight(1)
    rect(x, y, ancho, alto, 8)
    
    fill(0)
    textSize(24)
    textFont(fonts[0])
    textAlign(CENTER, CENTER)
    text(texto, x + ancho/2, y + alto/2)
    
    return mouse



def boton_cartelera(texto, x, y, ancho, alto):
    mouse = (mouseX > x and mouseX < x + ancho and 
             mouseY > y and mouseY < y + alto)
    if mouse and mousePressed:
        return True
    if mouse:
        fill(220)
    else:
        fill(255) 
    stroke(200)
    strokeWeight(1)
    rect(x, y, ancho, alto, 8)
    
    fill(0)
    textFont(fonts[2])
    textSize(18)
    textAlign(CENTER, CENTER)
    text(texto, x + ancho/2, y + alto/2)
    
    return False



def boton_entradas(texto, x, y, ancho, alto):
    mouse = (mouseX > x and mouseX < x + ancho and 
             mouseY > y and mouseY < y + alto)
    if mouse:
        fill(180, 8, 0)
        #fill(240, 60, 40)

    else:
        fill(255)
    stroke(200)
    strokeWeight(1)
    rect(x, y, ancho, alto, 8)
    
    fill(0)
    textSize(24)
    textFont(fonts[0])
    textAlign(CENTER, CENTER)
    text(texto, x + ancho/2, y + alto/2)
    
    return mouse


                
def radio_button(textos, x, y, diametro, seleccion_actual):
    spacing = 40
    
    for i, texto in enumerate(textos):
        mouse = (mouseX > x and mouseX < x + diametro + textWidth(texto) + 10
                and mouseY > y + i*spacing - diametro/2 
                and mouseY < y + i*spacing + diametro/2)
        
        fill(255)
        stroke(100)
        strokeWeight(1)
        ellipse(x, y + i*spacing, diametro, diametro)
        
        if i == seleccion_actual:
            fill(0)
            noStroke()
            ellipse(x, y + i*spacing, diametro/2, diametro/2)
        
        if mouse:
            fill(0)
        else:
            fill(80)
            
        textFont(fonts[2])
        text(texto, x + diametro + 40, y + i*spacing) 
        

            
def barra_horas(x, y, ancho, alto, horas, hora_sel, arrastrando):
    fill(255)
    stroke(0)
    strokeWeight(2)
    rect(x, y, ancho, alto, 5)
    
    seg_ancho = ancho / len(horas)
    
    textFont(fonts[2])
    textSize(14)
    textAlign(CENTER)
    for i in range(len(horas)):
        if i <= hora_sel:
            fill(lerpColor(color(255, 100, 100), color(100, 100, 255), i/len(horas)))
        else:
            fill(220)
        rect(x + i*seg_ancho, y, seg_ancho, alto)
        
        fill(0)
        textFont(fonts[2])
        textSize(14)
        text(horas[i], x + i*seg_ancho + seg_ancho/2, y + alto + 20)
    
    selector_x = x + hora_sel*seg_ancho + seg_ancho/2
    if arrastrando:
        fill(238, 195, 72)
    else:
        fill(255)
    stroke(0)
    strokeWeight(2)
    circle(selector_x, y + alto/2, 30)
    
    stroke(0, 150, 255, 150)
    strokeWeight(4)
    
    
    
def cartel_pelicula(x, y, ancho, alto, titulo, genero, duracion, sala, horarios, disponibles, funcion):
    global funcion_seleccionada, pantalla
    fill(240)
    stroke(0)
    strokeWeight(1)
    rect(x, y, ancho, alto, 10)
    
    fill(238, 195, 72)
    noStroke()
    rect(x, y, ancho, 50, 10, 10, 0, 0) 
    
    fill(255)
    textFont(fonts[2])
    textSize(20)
    textAlign(CENTER, CENTER)
    text(titulo, x + ancho/2, y + 25)
    
    fill(80)
    textAlign(LEFT, TOP)
    textSize(14)
    
    text("Genero: " + genero, x + 15, y + 60)
    text("Duracion: " + str(duracion) + " min", x + 15, y + 85)
    text("Sala: " + sala, x + 15, y + 110)
    
    stroke(200)
    line(x + 10, y + 140, x + ancho - 10, y + 140)
    
    fill(0)
    textSize(16)
    text("Horarios disponibles:", x + 15, y + 150)
    
    textSize(14)
    for i in range(len(horarios)):
        fill(50, 100, 200) 
        text("- " + horarios[i], x + 30, y + 180 + i*30)
        
        fill(100)
        text(str(disponibles[i]) + " sillas", x + 120, y + 180 + i*30)
        
        if disponibles[i] > 0:
            fill(0, 200, 0)
        else:
            fill(200, 0, 0)
            
        noStroke()
        circle(x + 200, y + 180 + i*30 + 5, 10)
        boton_entradas = boton_cartelera("Entradas", x + 15, y + alto - 45, ancho - 30, 30)
        return boton_entradas, funcion



def hora_24h(horario_str):
    try:
        hora_str, ampm = horario_str.split()
        hora = int(hora_str.split(':')[0])
        
        if ampm == 'PM' and hora != 12:
            return hora + 12
        elif ampm == 'AM' and hora == 12:
            return 0
        return hora
    except:
        return -1
    


def obtener_sala(funcion_buscada):
    for sala in [sala1, sala2, sala3]:
        if sala.contener_funcion(funcion_buscada):
            return sala
    return None
    
    
    
def asientos(xInicial, yInicial, ancho, alto, columnas, filas):
    global funcion_seleccionada, asientos_seleccionados
    rectMode(CORNER)
    textAlign(CENTER, CENTER)
    textSize(14)
    
    index_horario = 0
    asientos_horario = funcion_seleccionada.asientos_horario[index_horario]
    for fila in range(filas):
        for col in range(columnas):
            x = xInicial + col * (ancho + 10)
            y = yInicial + fila * (alto + 10) + 100
            num_asiento = fila * columnas + col + 1
            asiento = asientos_horario[num_asiento - 1]
        
            if num_asiento in asientos_seleccionados:
                fill(238, 195, 72) 
            elif asiento.disponible:
                fill(245, 245, 220) 
            else:
                fill(180, 8, 0) 
            
            stroke(40)
            rect(x, y, ancho, alto, 5)
            
            fill(0)
            text(str(fila * columnas + col + 1), x + ancho / 2, y + alto / 2)






def mousePressed():
    global pantalla, seleccion1, seleccion2
    global hora_actual1, hora_actual2, hora_actual3
    global funcion_seleccionada, asientos_seleccionados
    
    if pantalla == 0:
        if boton("CARTELERA", width*0.63, height*0.55, 360, 60):
            pantalla = 1
        if boton("INFORMACION", width*0.63, height*0.65, 360, 60):
            pantalla = 3
            
        if (width * 0.94 <= mouseX <= width * 0.94 + icons[5].width and height * 0.78 <= mouseY <= height * 0.78 + icons[5].height):
            print("hola")
            #exit()
         
               
    elif pantalla == 1:    
        for i in range(len(salas)):
            y_pos = height*0.38 + i*40
            if (dist(mouseX, mouseY, width*0.08, y_pos)) < 10:
                seleccion1 = i
                break
        
        seleccion_anterior = seleccion2       
        for j in range(len(horarios)):
            y_pos1 = height*0.62 + j*40
            if (dist(mouseX, mouseY, width*0.08, y_pos1)) < 10:
                seleccion2 = j
                if seleccion2 != seleccion_anterior:
                    hora_actual1 = 0
                    hora_actual2 = 0
                    hora_actual3 = 0
                break 
       
        if seleccion2 == 0:
            global arrastrando1, hora_actual1
            x1, y1, ancho1, alto1 = width*0.05, height*0.5 + 190, 230, 25
            seg_ancho1 = ancho1 / len(horas1)
        
            selector_x1 = x1 + hora_actual1*seg_ancho1 + seg_ancho1/2
            if dist(mouseX, mouseY, selector_x1, y1 + alto1/2) < 20:
                arrastrando1 = True
        
            elif (x1 < mouseX < x1 + ancho1 and y1 < mouseY < y1 + alto1):
                hora_actual1 = int((mouseX - x1) / seg_ancho1)
                hora_actual1 = constrain(hora_actual1, 0, len(horas1)-1)
                
        elif seleccion2 == 1:
            global arrastrando2, hora_actual2
            x2, y2, ancho2, alto2 = width*0.05, height*0.5 + 190, 230, 25
            seg_ancho2 = ancho2 / len(horas2)
        
            selector_x2 = x2 + hora_actual2*seg_ancho2 + seg_ancho2/2
            if dist(mouseX, mouseY, selector_x2, y2 + alto2/2) < 20:
                arrastrando2 = True
        
            elif (x2 < mouseX < x2 + ancho2 and y2 < mouseY < y2 + alto2):
                hora_actual2 = int((mouseX - x2) / seg_ancho2)
                hora_actual2 = constrain(hora_actual2, 0, len(horas2)-1) 
         
        elif seleccion2 == 2:   
            global arrastrando3, hora_actual3
            x3, y3, ancho3, alto3 = width*0.05, height*0.5 + 190, 230, 25
            seg_ancho3 = ancho3 / len(horas3)
        
            selector_x3 = x3 + hora_actual3*seg_ancho3 + seg_ancho3/2
            if dist(mouseX, mouseY, selector_x3, y3 + alto3/2) < 20:
                arrastrando3 = True
        
            elif (x3 < mouseX < x3 + ancho3 and y3 < mouseY < y3 + alto3):
                hora_actual3 = int((mouseX - x3) / seg_ancho3)
                hora_actual3 = constrain(hora_actual3, 0, len(horas3)-1)
                
        contador = 0
        for sala in [sala1, sala2, sala3]:
            if seleccion1 == -1 or sala == [sala1, sala2, sala3][seleccion1]:
                for funcion in sala.funciones:
                    x = width * 0.27 + (contador % 3) * 330
                    y = height * 0.2 + (contador // 3) * 280
                    
                    btn_x = x + 15
                    btn_y = y + 250 - 45
                    btn_ancho = 300 - 30
                    btn_alto = 30
                    
                    if (btn_x < mouseX < btn_x + btn_ancho and 
                        btn_y < mouseY < btn_y + btn_alto):
                        funcion_seleccionada = funcion
                        pantalla = 2
                        return 
                    
                    contador += 1
            
        if (width * 0.94 <= mouseX <= width * 0.94 + icons[2].width and height * 0.89 <= mouseY <= height * 0.89 + icons[2].height):
            seleccion1 = -1
            seleccion2 = -1
            hora_actual1 = 0
            hora_actual2 = 0
            hora_actual3 = 0
            arrastrando1 = False
            arrastrando2 = False
            arrastrando3 = False
            pantalla = 0
    
    
    elif pantalla == 2:
        if boton_entradas("Comprar", width * 0.1, height * 0.9, 360, 60):
            if len(asientos_seleccionados) > 0:
                for num_asiento in asientos_seleccionados:
                    if num_asiento - 1 < len(funcion_seleccionada.asientos_horario[0]):
                        funcion_seleccionada.asientos_horario[0][num_asiento - 1].ocupar()
                
                ganancias()
                guardar_informacion("Informacion.txt")
                asientos_seleccionados = []
        else:
            xInicial, yInicial = 550, 130
            ancho, alto = 50, 50
            columnas, filas = 10, 8
            
            for fila in range(filas):
                for col in range(columnas):
                    x = xInicial + col * (ancho + 10)
                    y = yInicial + fila * (alto + 10) + 100
                    num_asiento = fila * columnas + col + 1
                    
                    if (x < mouseX < x + ancho and y < mouseY < y + alto):
                        for horario in funcion_seleccionada.horarios:
                            if num_asiento not in funcion_seleccionada.asientos_ocupados(horario):
                                if num_asiento in asientos_seleccionados:
                                    asientos_seleccionados.remove(num_asiento)
                                else:
                                    asientos_seleccionados.append(num_asiento)
                            return
                    
                    
        if (width * 0.94 <= mouseX <= width * 0.94 + icons[2].width and height * 0.89 <= mouseY <= height * 0.89 + icons[2].height):
            seleccion1 = -1
            seleccion2 = -1
            hora_actual1 = 0
            hora_actual2 = 0
            hora_actual3 = 0
            arrastrando1 = False
            arrastrando2 = False
            arrastrando3 = False
            pantalla = 0
            funcion_seleccionada = None
            asientos_seleccionados = []
            
            
            
    elif pantalla == 3:
        if (width * 0.94 <= mouseX <= width * 0.94 + icons[2].width and height * 0.78 <= mouseY <= height * 0.78 + icons[2].height):
            pantalla = 0
            
    


def mouseDragged():
    global hora_actual1, hora_actual2, hora_actual3
    if seleccion2 == 0:
        if arrastrando1:
            x1, ancho1 = width*0.05, 200
            seg_ancho1 = ancho1 / len(horas1)
            hora_actual1 = int((mouseX - x1) / seg_ancho1)
            hora_actual1 = constrain(hora_actual1, 0, len(horas1)-1)
    elif seleccion2 == 1:
        if arrastrando2:
            x2, ancho2 = width*0.05, 200
            seg_ancho2 = ancho2 / len(horas2)
            hora_actual2 = int((mouseX - x2) / seg_ancho2)
            hora_actual2 = constrain(hora_actual2, 0, len(horas2)-1)
    elif seleccion2 == 2:
        if arrastrando3:
            x3, ancho3 = width*0.05, 200
            seg_ancho3 = ancho3 / len(horas3)
            hora_actual3 = int((mouseX - x3) / seg_ancho3)
            hora_actual3 = constrain(hora_actual3, 0, len(horas3)-1)
            
                      
                                          
def mouseReleased():
    global arrastrando1, arrastrando2, arrastrando3
    if seleccion2 == 0:
        arrastrando1 = False
    elif seleccion2 == 1:
        arrastrando2 = False
    elif seleccion2 == 2:
        arrastrando3 = False
