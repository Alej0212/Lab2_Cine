from datetime import datetime
from datetime import datetime, timedelta

class Cine:
  def __init__(self, nombre):
    self.nombre = nombre
    self.salas = []
    self.funciones_en_salas = []
    self.usuarios = []

  def agregar_sala(self, sala):
     self.salas.append(sala)
  
  def registrar_usuario(self, usuario):
      self.usuarios.append(usuario)
      print(f"{usuario.nombre} ha sido registrado en la base de datos del cine {self.nombre}.")   # Agregar un archivo de usuarios y boletas para cada uno

  def mostrar_salas(self):
      print(f"Cine: {self.nombre}")
      for sala in self.salas:
        print(f"Sala  {sala.nombre} con {sala.aisentosdisponibles} asientos disponibles")
        for fila in range(sala.num_filas):
          fila_asientos = sala.asientos[fila * sala.num_asientos:(fila + 1) * sala.num_asientos]
          print(" ".join(["[ ]" if asiento.disponible else "[X]" for asiento in fila_asientos]))
        print()

  def mostrar_una_sala(self, sala_nombre):
      for sala in self.salas:
        if sala.nombre == sala_nombre:
          print(f"Sala {sala.nombre} con {sala.aisentosdisponibles} asientos disponibles")
          for fila in range(sala.num_filas):
            fila_asientos = sala.asientos[fila * sala.num_asientos:(fila + 1) * sala.num_asientos]
            print(" ".join(["[ ]" if asiento.disponible else "[X]" for asiento in fila_asientos]))
          return
      print(f"Sala {sala_nombre} no encontrada.")

  def agregar_funcion_en_sala(self, funcion):
     self.funciones_en_salas.append(funcion)

  def mostrar_funciones_en_salas(self):
    for funcion in self.funciones_en_salas:
      print(funcion)
  
  def ocupar_asiento(self, sala_nombre, num_asiento, usuario, funcion):
    for funcion in self.funciones_en_salas:
      if funcion.sala.nombre == sala_nombre and funcion.sala.aisentosdisponibles > 0:
        for asiento in funcion.sala.asientos:
          if asiento.num == num_asiento and asiento.disponible:
            asiento.ocupar()
            funcion.sala.aisentosdisponibles -= 1
            boleta = Boleta(funcion, asiento, funcion.precio, funcion.sala)
            usuario.boletas.append(boleta)
            print(f"{usuario.nombre} ha comprado una boleta para la función '{funcion.movie.nombre}' en el asiento {num_asiento}.")
            return
    print(f"El asiento {num_asiento} no está disponible o no existe en la sala {sala_nombre}.")
  
  def desocupar_asiento(self, sala_numero, num_asiento):
    for sala in self.salas:
       if sala.numero == sala_numero:
          sala.desocupar_asiento(num_asiento)
          return
    print(f"Sala {sala_numero} no encontrada.")
      

  def mirar_ganancias (self):   # Idea: colocarle funciones 
    total_ganancias = 0
    for funcion in self.funciones:
      total_ganancias += funcion.precio * len([asiento for asiento in funcion.sala.asientos if not asiento.disponible]) # Suponiendo que cada asiento tiene un precio fijo
    print(f"Ganancias totales: ${total_ganancias}")

  def cargar_informacion(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()

    cine = None
    salas = {}
    for linea in lineas:
      linea = linea.strip()
      if linea.startswith("CINE"):
        _, nombre_cine = linea.split(",")
        cine = Cine(nombre_cine)
      elif linea.startswith("SALA"):
        _, numero, filas, asientos = linea.split(",")
        sala = Sala(int(filas), int(asientos))
        sala.numero = int(numero)
        salas[sala.numero] = sala
        cine.agregar_sala(sala)
      elif linea.startswith("FUNCION"):
        _, pelicula, horario, precio, sala_numero = linea.split(",")
        sala_numero = int(sala_numero)
        if sala_numero in salas:
          sala = salas[sala_numero]
          funcion = Funcion(Movie(pelicula, "Desconocido", "Duración desconocida"), sala, int(precio), cine, Horario(horario, horario))
          cine.agregar_funcion(funcion)
          sala.agregar_funcion(funcion)
    return cine
    

class Sala:
  def __init__(self, nombre :int, num_filas: int, num_asientos: int):
    self.aisentosdisponibles = 80 
    self.nombre = nombre
    self.num_filas = num_filas
    self.num_asientos = num_asientos
    self.asientos = []
    self.funciones = []
    self.crear_sala()
    self.usuarios = []


  def crear_sala(self):
      for i in range(self.num_filas * self.num_asientos):
        asiento = Seat(i + 1)
        self.asientos.append(asiento)


  def mostar_asientos(self):
      for asiento in self.asientos:
        if asiento.disponible:                      #  print(f"Asiento {asiento.num}: {'Disponible' if asiento.disponible else 'Ocupado'}")
          print(f"Asiento {asiento.num} disponible")
        else:
          print(f"Asiento {asiento.num} ocupado")



  def ocupar_asiento(self, num_fila: int, num_asiento: int):
       for asiento in self.asientos:
            if asiento.num == num_asiento and asiento.disponible:
                asiento.ocupar()
                self.aisentosdisponibles -= 1
                print(f"Asiento {num_asiento} ha sido ocupado.")
                return
                print(f"Asiento {num_asiento} no está disponible o no existe.") 



  def desocupar_asiento(self,  num_asiento : int):
       for asiento in self.asientos :
         if asiento.num == num_asiento and not asiento.disponible:
           asiento.desocupar()
           self.aisentosdisponibles += 1
           print(f"Asiento {num_asiento} ha sido desocupado.")

  def agregar_funcion(self, funcion):
      self.funciones.append(funcion)

  def mostrar_funciones(self):
        for funcion in self.funciones:
            print(funcion)

  def __str__(self):
        return f"Sala {self.nombre} - {self.num_filas} filas, {self.num_asientos} asientos por fila"




class Seat:
      def __init__(self, num: int = None, disponible: bool  = True):
        self.num = num
        self.disponible = True
      def ocupar(self):
       # self.num = num
        self.disponible = False
      def desocupar(self):
        #self.num = None
        self.disponible = True




class Movie:
  def __init__(self, nombre: str, genero: str, duracion: datetime):
    self.nombre = nombre
    self.genero = genero
    self.duracion = duracion

  def __str__(self):
        return f"{self.nombre} ({self.genero}) - Duración: {self.duracion}"



class Horario:
  def __init__(self, horaInicio: datetime, horaFin: datetime,):
    self.horaInicio = horaInicio
    self.horaFin = horaFin

  def __str__(self):
        return f"{self.horaInicio.strftime('%H:%M')} - {self.horaFin.strftime('%H:%M')}"
  


  
class Funcion:
  def __init__(self, movie: Movie, sala: Sala,  precio: int, cine:Cine, horario: Horario):
    self.movie = movie
    self.precio = precio
    self.horario =  horario
    self.sala = sala
    self.cine = cine 
    #cine.agregar_funcion(self)  # Se agrega automáticamente al cine
    #sala.agregar_funcion(self)  # Se agrega automáticamente a la sala

  def __str__(self):
        return (
            f"Función de '{self.movie.nombre}' en {self.sala} - "
            f"{self.horario} - Precio: ${self.precio}"
        )
  


class Boleta:
  def __init__(self, funcion: Funcion, asiento: Seat, precio: float, sala: Sala):
    self.precio = precio
    self.funcion = funcion
    self.asiento = asiento
    self.numero = asiento.num



class Persona: 
  def __init__(self, nombre: str, id: int, edad: int):
    self.nombre = nombre
    self.id = id
    self.edad = edad



class Usuario(Persona):  
  def __init__(self, nombre: str, id: int, edad: int, nboletas: int, cine: Cine):
    super().__init__(nombre, id, edad) 
    self.nboletas = nboletas
    self.boletas = []
    self.funciones = []
    self.cine = cine  
    

  def registrar_usuario(self, cine):
    cine.usuarios.append(self)
    print(f"{self.nombre} ha sido registrado en la base de datos del cine {cine.nombre}.")


  def elegir_asiento(self, sala, num_asiento):
    for asiento in sala.asientos:
      if asiento.num == num_asiento and asiento.disponible:
        asiento.ocupar()
        print(f"{self.nombre} ha elegido el asiento {num_asiento}")
        return asiento
    print(f"El asiento {num_asiento} no está disponible o no existe.")
    return None


  def comprar_boleta(self, funcion, num_asiento: int):
    asiento = self.elegir_asiento(funcion.sala, num_asiento)
    if asiento:
      boleta = Boleta(funcion, asiento, funcion.precio, funcion.sala)
      self.boletas.append(boleta)
      print(f"{self.nombre} ha comprado una boleta para la función '{funcion.movie.nombre}' en el asiento {num_asiento}.")
    else:
      print("No se pudo completar la compra de la boleta.")


  def mostrar_boletas(self):
    for boleta in self.boletas:
      print(f"Boleta {boleta.numero} - {boleta.funcion.movie.nombre} - Asiento {boleta.asiento.num}")



'''
def consultar_sala():    #Metodo para consultar las salas y sus funciones
  while True:
     sala_nombre = input("Ingrese el nombre de la sala (o escriba 'salir' para terminar): ")
     if sala_nombre.lower() == "salir":
        print("Saliendo de la consulta de salas.")
        break
     encontrado = False
     for sala in cine.salas:
        if sala.nombre == sala_nombre:
          print(f"Sala {sala.nombre} encontrada")
          cine.mostrar_una_sala(sala_nombre)
          print(f"Funciones disponibles en la sala {sala.nombre}:")
          for funcion in sala.funciones:
            print(f" - {funcion.movie.nombre} a las {funcion.horario.horaInicio.strftime('%H:%M')}")
          print()
          encontrado = True
          break
     if not encontrado:
        print("Sala no encontrada. Intente nuevamente.")
'''


def registrar_usuario(cine):                         # 
  print("Bienvenido al sistema de registro de usuarios.")
  nombre = input("Ingrese su nombre: ")
  id = int(input("Ingrese su ID: "))
  edad = int(input("Ingrese su edad: "))
  usuario1 = Usuario(nombre, id, edad, 0, cine)
 # cine.registrar_usuario(usuario1)                 # Registrar el usuario en el cine
  #print(f"Usuario {usuario1.nombre} registrado con éxito.")
  return usuario1

#Procedimiento 

cine = Cine("Cine Cultural Barranquilla")


alpha = Sala( "alpha",10, 8)
beta = Sala( "beta",10, 8)
omega = Sala("omega",10, 8)

cine.agregar_sala(alpha)
cine.agregar_sala(beta)
cine.agregar_sala(omega)


# Solo dos funciones para cada sala
# Se crean las funciones y se agregan a las salas
Intensamente2 = Movie("Intensamente 2", "Animación", 2)
GodzillaandtheKingKong = Movie("Godzilla y Kong: El nuevo imperio", "Acción", 2)
Dunaparte2 = Movie("Duna: parte 2", "Ciencia Ficción", 2)


funcion1 = Funcion( Intensamente2, alpha, 10000, cine, Horario(datetime(2025, 4 , 20 , 10, 0), datetime(2025, 4, 20, 11, 40)))
funcion2 = Funcion( GodzillaandtheKingKong, alpha, 10000, cine, Horario(datetime(2025, 4, 20, 15, 0), datetime(2025, 4, 20, 16, 55)))   # para modificar los precios y la hora
funcion3 = Funcion( Dunaparte2, omega, 10000, cine, Horario(datetime(2025, 4, 19, 11, 0), datetime(2025, 4, 19, 13, 45)))
funcion4 = Funcion( Intensamente2, omega, 10000, cine, Horario(datetime(2025, 4 , 20 , 17, 0), datetime(2025, 4, 20, 18, 40)))
funcion5 = Funcion( GodzillaandtheKingKong, beta, 10000, cine, Horario(datetime(2025, 4 , 19 , 12, 0), datetime(2025, 4, 19, 13, 55)))
funcion6 = Funcion( Dunaparte2, beta, 10000, cine, Horario(datetime(2025, 4 , 19 , 18, 0), datetime(2025, 4, 19, 20, 45)))

alpha.agregar_funcion(funcion1)
alpha.agregar_funcion(funcion2)
beta.agregar_funcion(funcion5)
beta.agregar_funcion(funcion6)
omega.agregar_funcion(funcion3)
omega.agregar_funcion(funcion4)

cine.agregar_funcion_en_sala(funcion1)
cine.agregar_funcion_en_sala(funcion2)
cine.agregar_funcion_en_sala(funcion3)
cine.agregar_funcion_en_sala(funcion4)
cine.agregar_funcion_en_sala(funcion5)
cine.agregar_funcion_en_sala(funcion6)


#cine.mostrar_salas() Funciona


#consultar_sala()  Funciona

#omega.mostrar_funciones()   Funciona

#cine.mostrar_funciones_en_salas()   Funciona


# Crear usuario
#usuario1 = Usuario("Carlos", 101, 25, 0, cine)    # Crear los archivos de los usuarios y las boletas


#usuario1.registrar_usuario(cine)  # Registrar el usuario en el cine
#usuario1.mostrar_boletas()  # Mostrar las boletas del usuario (vacío al principio)  



def vender_boleta(cine):                          # pPara comprar una boleta
  print("Bienvenido al sistema de venta de boletas.")
  while True:
    print("Funciones disponibles:")
    for funcion in cine.funciones_en_salas:
      print(f" - {funcion.movie.nombre} en la sala {funcion.sala.nombre} a las {funcion.horario.horaInicio.strftime('%H:%M')}")

    respuesta = input("¿Desea comprar una boleta? (si/no): ").lower()
    if respuesta != "si":
      print("Gracias por visitar el sistema. ¡Hasta luego!")
      break

    pelicula_nombre = input("Ingrese el nombre de la película que desea ver: ")
    funciones_disponibles = [funcion for funcion in cine.funciones_en_salas if funcion.movie.nombre.lower() == pelicula_nombre.lower()]

    if not funciones_disponibles:
      print(f"No se encontraron funciones para la película '{pelicula_nombre}'. Intente nuevamente.")
      continue

    print(f"Funciones disponibles para '{pelicula_nombre}':")
    for i, funcion in enumerate(funciones_disponibles, start=1):
      print(f"{i}. Sala {funcion.sala.nombre} - {funcion.horario} - Precio: ${funcion.precio}")

    seleccion = int(input("Seleccione el número de la función que desea (o 0 para cancelar): "))
    if seleccion == 0:
      print("Compra cancelada.")
      continue

    if seleccion < 1 or seleccion > len(funciones_disponibles):
      print("Selección inválida. Intente nuevamente.")
      continue

    funcion_seleccionada = funciones_disponibles[seleccion - 1]

    # Verificar si han pasado más de 30 minutos desde el inicio de la función
    ahora = datetime.now()
    limite_compra = funcion_seleccionada.horario.horaInicio + timedelta(minutes=30)
    if ahora > limite_compra:
      print("No se pueden comprar boletas para esta función porque ya han pasado 30 minutos desde su inicio.")
      continue

    cine.mostrar_una_sala(funcion_seleccionada.sala.nombre)

    num_asiento = int(input("Ingrese el número de asiento que desea comprar: "))
    print("¿Desea confirmar la compra? (si/no)")
    confirmacion = input().lower()
    if confirmacion != "si":
      print("Compra cancelada.")
      continue

    nombre_usuario = input("Ingrese su nombre: ")
    id_usuario = int(input("Ingrese su ID: "))
    edad_usuario = int(input("Ingrese su edad: "))
    usuario = Usuario(nombre_usuario, id_usuario, edad_usuario, 0, cine)
    cine.registrar_usuario(usuario)

    usuario.comprar_boleta(funcion_seleccionada, num_asiento)
    print("¡Compra realizada con éxito! Aquí está su boleta:")
    usuario.mostrar_boletas()
    print("Gracias por su compra. ¡Disfrute la función!")

    otra_compra = input("¿Desea comprar otra boleta? (si/no): ").lower()
    if otra_compra != "si":
      print("Gracias por visitar el sistema. ¡Hasta luego!")
      break

vender_boleta(cine)  # Llamar a la función para vender boletas


