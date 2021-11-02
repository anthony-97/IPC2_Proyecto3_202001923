class Factura:
    def __init__(self, tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total, codigo):
        self.tiempo = tiempo 
        self.referencia = referencia
        self.nit_emisor= nit_emisor
        self.nit_receptor = nit_receptor
        self.valor= valor
        self.iva = iva
        self.total = total
        self.codigo = codigo

    def __str__(self):
            print("Tiempo: ", self.tiempo)
            print("Referencia: ", self.referencia)
            print("NIT emisor: ", self.nit_emisor)
            print("NIT Receptor: ", self.nit_receptor)
            print("Valor: ", self.valor)
            print("IVA: ", self.iva)
            print("Total: ", self.total)
            print("Codigo de autorizacion: ", self.codigo)