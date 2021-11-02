class Fecha:
    def __init__(self, fecha, recibidas, errores, correctas, emisores, receptores, autorizaciones):
        self.fecha = fecha
        self.recibidas = recibidas 
        self.errores = errores
        self.correctas = correctas
        self.emisores= emisores
        self.receptores = receptores
        self.autorizaciones = autorizaciones #Este atributo va a contener la lista de facturas aprobadas

    def __str__(self):
            print("---------------------------------------------")
            print("Fecha: ", self.fecha)
            print("Recibidas: ", self.recibidas)
            print("Errores: ", self.errores)
            print("Correctas: ", self.correctas)
            print("Emisores: ", self.emisores)
            print("Receptores: ", self.receptores)
            print("Autorizaciones: ", self.autorizaciones)
            print("----------------------------------------------")

class fecha_prelim:
    def __init__(self, fecha, referencias, errores, correctas, con_errores, emisores, receptores, autorizaciones):
        self.fecha = fecha
        self.referencias = referencias
        self.errores = errores
        self.correctas = correctas
        self.con_errores = con_errores
        self.emisores = emisores
        self.receptores = receptores
        self.autorizaciones = autorizaciones
        

    def __str__(self):
            print("---------------------------------------------")
            print("Fecha: ", self.fecha)
            print("Referencias: ", self.referencias) 
            print("Errores: ", self.errores)
            print("Correctas: ", self.correctas)
            print("Con errores: ", self.con_errores)
            print("Emisores: ", self.emisores)
            print("Receptores: ", self.receptores)
            print("Autorizaciones: ", self.autorizaciones)
            print("---------------------------------------------")