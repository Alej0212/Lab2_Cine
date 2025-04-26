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




#Clases y listas
class Sala:
  def __init__(self, num_filas, num_asientos):
    self.num_filas = num_filas
    self.num_asientos = num_asientos
    self.asientos = []
    self.funciones = []
    self.crear_sala()


  def crear_sala(self):
      for i in range(self.num_filas * self.num_asientos):
        asiento = Seat(i + 1)
        self.asientos.append(asiento)



  def mostar_asientos(self):
      for asiento in self.asientos:
        if asiento.disponible:
            print("Asiento {} disponible".format(asiento.num))
        else:
            print("Asiento {} ocupado".format(asiento.num))



  def ocupar_asiento(self, num_fila, num_asiento):
       for asiento in self.asientos:
            if asiento.num == num_asiento and asiento.disponible:
                asiento.ocupar()
                print("Asiento {} ha sido ocupado".format(num_asiento))
                return
                print("Asiento {} no esta disponible".format(num_asiento))



  def desocupar_asiento(self,  num_asiento):
       for asiento in self.asientos :
         if asiento.num == num_asiento and not asiento.disponible:
           asiento.desocupar()
           print("Asiento {} ha sido desocupado".format(num_asiento))


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
                if i < len(funcion.asientos_disponibles):
                    disp = funcion.asientos_disponibles[i]
                else:
                    disp = "N/A"
                print("  - " + horario + " (Asientos disponibles: " + str(disp) + ")")
        else:
            print("  - No hay horarios registrados")



class Seat:
      def __init__(self, num = None, disponible  = True):
        self.num = num
        self.disponible = True
      def ocupar(self):
        self.disponible = False
      def desocupar(self):
        self.disponible = True



class Funcion:
    def __init__(self, nombre, genero, duracion, precio):
        self.nombre = nombre
        self.genero = genero
        self.duracion = duracion
        self.precio = precio
        self.horarios = []
        self.asientos_disponibles = []

    def agregar_horario(self, horario, disponibles):
        self.horarios.append(horario)
        self.asientos_disponibles.append(disponibles)




#Funciones Processing
def setup():
    fullScreen()
    global icons
    global fonts
    global sala1, sala2, sala3
    icons.append(loadImage("icon3.png"))
    icons.append(loadImage("icon8.png"))
    icons.append(loadImage("icon9.png"))
    
    fonts.append(createFont("font3.ttf", 28))
    fonts.append(createFont("font2.ttf", 60))
    fonts.append(createFont("font4.ttf", 28))
    
    sala1 = Sala(10, 8)
    sala2 = Sala(10, 8)
    sala3 = Sala(10, 8)
    
    avengers = Funcion("Avengers", "Ficcion", 180, 10000)
    avengers.agregar_horario("9:00 AM", 5)
    sala1.agregar_funcion(avengers)
    
    rey_leon = Funcion("Rey Leon", "Aventura", 118, 9000)
    rey_leon.agregar_horario("4:00 PM", 0)
    sala2.agregar_funcion(rey_leon)
    
    frozen = Funcion("Frozen", "Animacion", 180, 8000)
    frozen.agregar_horario("7:00 PM", 10)
    sala3.agregar_funcion(frozen)
    
    while_you_were_spleeping = Funcion("While you were spleeping", "Romance", 180, 10000)
    while_you_were_spleeping.agregar_horario("10:00 AM", 5)
    sala1.agregar_funci<on(while_you_were_spleeping)   

    wish_list = Funcion("Wish list", "Romance", 185, 15000)
    wish_list.agregar_horario("9:00 PM", 0)
    sala2.agregar_funcion(wish_list)



def draw():
    if pantalla == 0:
        inicio()
    elif pantalla == 1:
        cartelera()
    elif pantalla == 2:
        entradas()
    

    


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
    
    boton("CARTELERA", width*0.63, height*0.45, 360, 60)
    boton("ENTRADAS", width*0.63, height*0.55, 360, 60)
    boton("ADMINISTRADOR", width*0.63, height*0.65, 360, 60)
    


def cartelera():
    background(180, 8, 0)
    stroke(0)
    fill(255, 255, 255)
    textFont(fonts[0])
    textSize(60)
    text("CARTELERA", width*0.5, height*0.15)
    
    fill(220)
    stroke(200)
    strokeWeight(1)
    rect(width*0.025 , height*0.2, 300, 60)
    fill(0)
    textSize(30)
    text("FILTROS", width*0.105, height*0.23)
    
    stroke(0)
    strokeWeight(2)
    fill(255)
    rect(width*0.025, height*0.3, 300, 190)
    fill(0)
    noStroke()
    circle(width*0.05, height*0.33, 20)
    text("SALAS", width*0.07, height*0.315)
    radio_button(salas, width*0.08, height*0.39, 20, seleccion1)
    stroke(0)
    strokeWeight(2)
    fill(255)
    rect(width*0.025, height*0.3 + 170, 300, 235)
    fill(0)
    noStroke()
    circle(width*0.05, height*0.33 + 167, 20)
    textFont(fonts[0])
    text("HORARIO", width*0.07, height*0.535)
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
                    cartel_pelicula(x, y, 300, 250, funcion.nombre, funcion.genero, 
                                    funcion.duracion, str([sala1, sala2, sala3].index(sala) + 1), 
                                    [str(h) for h in funcion.horarios], funcion.asientos_disponibles)
                    contador += 1


    
    icons[2] = resize_img(icons[2], 70)
    image(icons[2], width*0.94, height*0.89)
    
    
    
def entradas():
    background(180, 8, 0)




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
        text(texto, x + diametro, y + i*spacing - 7.5) 
        

            
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
    
    
    
def cartel_pelicula(x, y, ancho, alto, titulo, genero, duracion, sala, horarios, disponibles):
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
        boton_cartelera("Entradas", x + 15, y + alto - 45, ancho - 30, 30)



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





def mousePressed():
    global pantalla, seleccion1, seleccion2
    global hora_actual1, hora_actual2, hora_actual3
    
    if pantalla == 0:
        if boton("CARTELERA", width*0.63, height*0.45, 360, 60):
            pantalla = 1
        if boton("ENTRADAS", width*0.63, height*0.55, 360, 60):
            pantalla = 2
            
    elif pantalla == 1:    
        for i in range(len(salas)):
            y_pos = height*0.39 + i*40
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
    
    
    
    
    
