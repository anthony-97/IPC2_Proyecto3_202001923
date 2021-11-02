import builtins
from os import confstr
from flask import Flask,request, jsonifyS
from flask_cors import CORS
import xml.etree.ElementTree as xml
from Factura import Factura
from Fecha import Fecha, fecha_prelim 
import webbrowser, json, re
from matplotlib import pyplot as plt

app = Flask(__name__)

#LISTA DE FACTURAS
facturas=[]

#Fechas en prelim
fechas=[]
#Fechas en tipo caracter
fechas_cad=[]
#Fechas en objeto
listaFechas=[]

#Referencias duplicadas a eliminar
ref_eliminar=[]

CORS(app)

@app.route("/")
def index():
    return "Prueba"

@app.route("/procesar", methods=['POST'])
def procesar():
    datos = request.json['name']
    entrada = open("/home/polares/Downloads/IPC2Proyecto3/aplicacion/flask/entrada.xml", "w+")
    entrada.write(datos)
    entrada.close()
    #Carga el archivo, inicializa las fechas preliminares
    cargar("/home/polares/Downloads/IPC2Proyecto3/aplicacion/flask/entrada.xml")
    for f in facturas:
        print(f.__str__())
    global fechas
    for fc in fechas:
        print(fc.__str__())
    print("\nfechas ingresadas"+str(len(fechas)))
    print("\nfacturas ingresadas"+str(len(facturas)))
    llenarF()
    print(listaFechas)
    salida()
    webbrowser.open("/home/polares/Downloads/IPC2Proyecto3/autorizaciones.xml")
    obtener_nits("16/01/2021")
    rango_fechas1("15/01/2021","16/01/2021")
    rango_fechas2("15/01/2021","18/01/2021")
    #generarGrafica()
    return "recibido"

def cargar(ruta):
    obj=xml.parse(ruta)
    root=obj.getroot()
    ultimo = 1
    for d in root.findall("DTE"):
        error=False
        errores_ref=0
        errores_emisor=0
        errores_receptor=0
        errores_total=0
        errores_iva=0
        for tm in d.findall("TIEMPO"):
            tmp=tm.text
            ls=re.split(" ", tmp)
            f=ls[2].replace(" ","")
            if f in fechas_cad:
                pass
            else:
                fechas_cad.append(f)
                f_prelim=fecha_prelim(f,[],[0,0,0,0,0],0,0,[],[],[])
                fechas.append(f_prelim)
        for r in d.findall("REFERENCIA"):
            ref=r.text
            for fh in fechas:
                if fh.fecha == f:
                    if ref in fh.referencias:
                        errores_ref+=2
                        error=True
                        ref_eliminar.append(ref)
                    else:
                        fh.referencias.append(ref)
        for ne in d.findall("NIT_EMISOR"):
            nem=ne.text
            if len(nem) > 20:
                error = True
                errores_emisor+=1
            try:
                nit_em=int(nem)
                for fh in fechas:
                    if fh.fecha == f:
                        if nit_em in fh.emisores:
                            pass
                        else:
                            fh.emisores.append(nit_em)
            except ValueError:
                errores_emisor+=1
                error = True
        for nr in d.findall("NIT_RECEPTOR"):
            nrec=nr.text
            if len(nrec) > 20:
                error = True
                errores_receptor+=1
            try:
                nit_rec=int(nrec)
                for fh in fechas:
                    if fh.fecha == f:
                        if nit_rec in fh.receptores:
                            pass
                        else:
                            fh.receptores.append(nit_rec)
            except ValueError:
                error = True
                errores_receptor+=1
        for v in d.findall("VALOR"):
            vl=v.text
            val = vl.replace(" ", "")
        for i in d.findall("IVA"):
            iva=i.text
            iv = iva.replace(" ", "")
        for t in d.findall("TOTAL"):
            tt=t.text
            tot = tt.replace(" ", "")
            print("\n\tFecha actual "+f)
            print("\t Error en la pasada "+str(error)+'\n')
            print(val + "..........." + iv +".........."+ str(float(val) + float(iv)))
        if round(float(val)+float(iv),2) == float(tot) and not error:
            ca = f.split("/")
            fecha_cod=""
            for cad in reversed(ca):
                fecha_cod+=cad
            if ultimo < 10:
                cadena="0000000"
            else:
                cadena="000000"
            c_apr = fecha_cod +cadena+str(ultimo)
            fac = Factura(f,ref,nit_em,nit_rec,val,iv,tot,c_apr)
            facturas.append(fac)
            for fh in fechas:
                if fh.fecha == f:
                    fh.correctas+=1
                    fh.autorizaciones.append(fac)
                    ultimo+=1
        if round(float(val)+ float(iv),2) != float(tot):
            errores_total+=1
            error = True
        if float(iv) != round(0.12*float(val),2):
            errores_iva+=1
            error = True
        print("\n\tFecha actual "+f)
        print("\t Error en la pasada "+str(error)+'\n')
        print("errores emisor: " + str(errores_emisor))
        print("errores receptor: " + str(errores_receptor))
        print("errores iva: " + str(errores_iva))
        print("errores total: " + str(errores_total))
        print("errores referencia: " + str(errores_ref))
        if error:
            #Busca la fecha en fechas preliminares y agrega los errores
            for fh in fechas:
                if fh.fecha==f:
                    fh.con_errores+=1
                    fh.errores[0]+=errores_emisor
                    fh.errores[1]+=errores_receptor
                    fh.errores[2]+=errores_iva
                    fh.errores[3]+=errores_total
                    fh.errores[4]+=errores_ref
    #Revisar que los archivos de prueba esten correctos, con las fechas y todo eso.

    def agregarFechas():
        lfechas=[fechas]
        for f in fechas:
            lfechas.append({"fecha":f.fecha})
        return lfechas
        
#Llena una lista con objetos de tipo fecha
def llenarF():
    error=False
    eliminadas=0
    for f in fechas:
        #Cambiar el 2 parametro para que sean las recibidas en esa fecha, 3 lista de errores, 
        # 4 correctas (entero), los emisores y receptores estan casi bien creo, leer del doc.
        for r in ref_eliminar:
            if r in f.referencias:
                contador = 0
                for fact in f.autorizaciones:
                    if r == fact.referencia:
                        f.autorizaciones.remove(f.autorizaciones[contador])
                        f.correctas=f.correctas-1
                        eliminadas+=1
                        error=True
                    contador+=1
        if error:
            fc=Fecha(f.fecha, f.correctas+f.con_errores+eliminadas, f.errores, f.correctas, len(f.emisores),len(f.receptores),f.autorizaciones)
        else:
            fc=Fecha(f.fecha, f.correctas+f.con_errores, f.errores, f.correctas, len(f.emisores),len(f.receptores),f.autorizaciones)
        listaFechas.append(fc)


@app.route("/ConsultaDatos", methods=['GET'])
#Implementar el metodo salida()
def consulta_datos():
    datos = request.json(['entrada'])
    print(str(datos))
    return datos

def salida():
    root = xml.Element('LISTAAUTORIZACIONES')
    for f in listaFechas:
        autorizacion= xml.SubElement(root, 'AUTORIZACION') #Usar el .text=str para agregarle el texto a la etqt.
        fch=xml.SubElement(autorizacion, "FECHA").text=str(f.fecha)
        fact=xml.SubElement(autorizacion, 'FACTURAS_RECIBIDAS').text=str(f.recibidas)
        err=xml.SubElement(autorizacion, "ERRORES")
        nit_e=xml.SubElement(err,"NIT_EMISOR").text=str(f.errores[0])
        nit_r=xml.SubElement(err, "NITRECEPTOR").text=str(f.errores[1])
        iva=xml.SubElement(err, "IVA").text=str(f.errores[2])
        total=xml.SubElement(err, "TOTAL").text=str(f.errores[3])
        rd=xml.SubElement(err, "REFERENCIA_DUPLICADA").text=str(f.errores[4])
        fc=xml.SubElement(autorizacion, "FACTURAS_CORRECTAS").text=str(f.correctas)
        ce=xml.SubElement(autorizacion, "CANTIDAD_EMISORES").text=str(f.emisores)
        cr=xml.SubElement(autorizacion, "CANTIDAD_RECEPTORES").text=str(f.receptores)
        listado=xml.SubElement(autorizacion, "LISTADO_AUTORIZACIONES")
        for a in f.autorizaciones:
            aprobacion=xml.SubElement(listado, "APROBACION")
            nE=xml.SubElement(aprobacion, "NIT_EMISOR", ref=str(a.referencia)).text=str(a.nit_emisor)
            ns=xml.SubElement(aprobacion, "NIT_RECEPTOR").text=str(a.nit_receptor)
            codigo=xml.SubElement(aprobacion, "CODIGO_APROBACION").text=str(a.codigo)
            t=xml.SubElement(aprobacion, "TOTAL").text=str(a.total)
        aprobacion=xml.SubElement(listado, "TOTAL_APROBACIONES").text=str(len(f.autorizaciones))
    archivo = xml.ElementTree(root)
    archivo.write('autorizaciones.xml')
    a = open('autorizaciones.xml', 'r')
    salida = a.read()
    return jsonify({"salida":salida})
    

    #Revisar el algoritmo de lectura del xml probandolo con la entrada


    #Generar grafica
def generarGrafica1(inicio, final):
    fig, ax = plt.subplots()
    lista_x=[]
    lista_y=[]
    indice = 0
    partida =0
    llegada =0
    for f in fechas:
        if f.fecha == inicio:
            partida = indice
        if f.fecha == final:
            llegada = indice
        indice+=1 
    fchs=[]
    while fechas[partida].fecha != fechas[llegada].fecha:
        fchs.append(fechas[partida].fecha)
        lista_x.append(partida)
        total_general=0.0
        for a in fechas[partida].autorizaciones:
            total_general+=float(a.total)
        lista_y.append(round(total_general,2))
        partida+=1
        if fechas[partida].fecha == fechas[llegada].fecha:
            fchs.append(fechas[partida].fecha)
            lista_x.append(partida)
            total_general=0.0
            for a in fechas[partida].autorizaciones:
                total_general+=float(a.total)
            lista_y.append(round(total_general,2))
            break
    ax.scatter(lista_x,lista_y)
    plt.xticks(lista_x, fchs)
    plt.yticks(lista_y,lista_y)
    ax.set_title("Valores totales (con IVA) comprendidos entre el " + inicio + " y el " + final, loc = "center")
    plt.savefig("graficaTotales.png")
    plt.show()

#Genera la grafica sin IVA.
def generarGrafica2(inicio, final):
    fig, ax = plt.subplots()
    lista_x=[]
    lista_y=[]
    indice = 0
    partida = 0
    llegada = 0
    for f in fechas:
        if f.fecha == inicio:
            partida = indice
        if f.fecha == final:
            llegada = indice
        indice+=1
    fchs=[]
    while fechas[partida].fecha != fechas[llegada].fecha:
        fchs.append(fechas[partida].fecha)
        lista_x.append(partida)
        total_sinIVA=0.0
        for a in fechas[partida].autorizaciones:
            total_sinIVA+=float(a.valor)
        lista_y.append(round(total_sinIVA,2))
        partida+=1
        if fechas[partida].fecha == fechas[llegada].fecha:
            fchs.append(fechas[partida].fecha)
            lista_x.append(partida)
            total_sinIVA=0.0
            for a in fechas[partida].autorizaciones:
                total_sinIVA+=float(a.valor)
            lista_y.append(round(total_sinIVA,2))
            break
    ax.scatter(lista_x,lista_y)
    plt.xticks(lista_x, fchs)
    plt.yticks(lista_y,lista_y)
    ax.set_title("Valores sin IVA comprendidos entre el " + inicio + " y el " + final, loc = "center")
    plt.savefig("graficaSinIVA.png")
    plt.show()

#Metodo para pasar a tabla los datos en el frontend
#@app.route('/obtener_pacientes', methods=['GET'])
def obtener_nits(fecha):
    json_nit = []
    for f in fechas:
        if f.fecha == fecha:
            for a in f.autorizaciones:
                lista_prelim = {'emisor':a.nit_emisor, 'receptor':a.nit_receptor, 'iva': a.iva}
                jsonStr = json.dumps(lista_prelim)
                json_nit.append(jsonStr)
    print("--------Tabla de nits------\n")
    print(json_nit)
    return json_nit

#Metodo para pasar a tabla los datos en el frontend valores totales
def rango_fechas1(inicio, final):
    json_total_general = []
    indice = 0
    partida = 0
    llegada = 0
    for f in fechas:
        if f.fecha == inicio:
            partida=indice
        if f.fecha == final:
            llegada=indice
        indice+=1
    while fechas[partida].fecha != fechas[llegada].fecha:
        total_general=0.0
        for a in fechas[partida].autorizaciones:
            total_general+=float(a.total)
        lista_prelim = {"fecha":fechas[partida].fecha,"total_general": total_general}
        jsonStr = json.dumps(lista_prelim)
        json_total_general.append(jsonStr)
        partida+=1
        if fechas[partida].fecha == fechas[llegada].fecha:
            total_general=0.0
            for a in fechas[partida].autorizaciones:
                total_general+=float(a.total)
            lista_prelim = {"fecha":fechas[partida].fecha,"total_general": total_general}
            jsonStr = json.dumps(lista_prelim)
            json_total_general.append(jsonStr)
            break

    print("--------GENERAL---------\n")
    print(json_total_general)
    generarGrafica1(inicio,final)
    return json_total_general

#Metodo para pasar a tabla los datos en el frontend valores sin iva
def rango_fechas2(inicio, final):
    json_sinIVA = []
    indice = 0
    partida = 0
    llegada = 0
    for f in fechas:
        if f.fecha == inicio:
            partida=indice
        if f.fecha == final:
            llegada=indice
        indice+=1
    while fechas[partida].fecha != fechas[llegada].fecha:
        total_sinIVA=0.0
        for a in fechas[partida].autorizaciones:
            total_sinIVA+=float(a.valor)
        lista_prelim = {"fecha":fechas[partida].fecha,"sin_iva": total_sinIVA}
        jsonStr = json.dumps(lista_prelim)
        json_sinIVA.append(jsonStr)
        partida+=1
        if fechas[partida].fecha == fechas[llegada].fecha:
            total_sinIVA=0.0
            for a in fechas[partida].autorizaciones:
                total_sinIVA+=float(a.valor)
            lista_prelim = {"fecha":fechas[partida].fecha,"sin_iva": total_sinIVA}
            jsonStr = json.dumps(lista_prelim)
            json_sinIVA.append(jsonStr)
            break
    print("--------SIN IVA---------\n")
    print(json_sinIVA)
    generarGrafica2(inicio,final)
    return json_sinIVA

if __name__=="__main__":
    app.run(debug=True)