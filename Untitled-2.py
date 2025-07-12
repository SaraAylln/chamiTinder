class Perfil:
    def __init__(self, nombreyapellido, email, habitacion, crushes):
        self.nombreyapellido = nombreyapellido
        self.email = email
        self.habitacion = habitacion
        self.crushes = [] 
        # es una lista que se va a rellenar cuando se seleccionen opciones de crushes en el tiempo2
        # por tanto se va a rellenar con objetos tipo Perfil

        