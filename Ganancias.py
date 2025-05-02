class Sala:
    def __init__(self, num_filas, num_asientos):
        self.num_filas = num_filas
        self.num_asientos = num_asientos
        self.ganancias = 0
        self.personas = 0
        self.asientos = []
        self.funciones = []
        self.crear_sala()

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
                        print(sala.personas)
                        sala.ganancias = sala.ganancias + funcion.precio
                        print(sala.ganancias)
