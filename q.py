#import xml.etree.ElementTree as ET 
from threading import Event
from xml.dom import minidom
import qrcode
import base64
import os
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time







def magia():

    data = {"CantReg":[],"CbteTipo":[],"Cuit":[],"FchProceso":[],"PtoVta":[],"Reproceso":[],"Resultado":[],"CAE":[],"CAEFchVto":[],"CbteDesde":[],"CbteFch":[],"CbteHasta":[],"Concepto":[],"DocNro":[],"DocTipo":[]}

    VER =  '1'
    fecha = 'CbteFch'
    Cuit = 'Cuit'
    ptoVta = 'PtoVta'
    tipoCmp = 'CbteTipo'
    nroCmp = 'CbteDesde'
    IMPORTE = "10630" # DESPUES PONERLO PARA QUE LO PIDA
    MONEDA = '"PES"'
    CTZ = '1'
    tipoDocRec = 'DocTipo'
    nroDocRec = 'DocNro'
    TIPO_COD_AUT = '"A"'
    codAut = 'CAE'


    PDF    = 'FACA000300005533'
    FOLDER = 'FACA000300005533'
    XML = 'FACA000300005533AFIP.XML' 

    xml = minidom.parse('Otros/'+FOLDER+'/'+XML)


    fields = xml.getElementsByTagName("field")

    #extraccion del xml y cargado de datos a data
    for field in fields:
        name = field.getAttribute("name")
        if name in data:
            data[name] = field.firstChild.data   


    # Acomodar fecha con "-"
    year = data[fecha][:4] + '-'
    month_day = data[fecha][4:]
    month_day = month_day[:2] + '-' + month_day[2:]
    data[fecha] = '"' + year + month_day + '"' 



    # Pedir importe

    # Tomar el importe de importe_total.txt, en caso de no existir, lo pide y crea
    f = open('Otros/'+FOLDER+'/'+'importe_total', "a+")
    f.close()
    f = open('Otros/'+FOLDER+'/'+'importe_total', "r+")
    contenido = f.read()
    if contenido =='':
        print('Ingrese el importe total:')
        IMPORTE = input()
        f.write(IMPORTE)
        print("Ok, el importe ingresado es: " + IMPORTE)
    else:
        IMPORTE = contenido
    print('Importe utilizado: ' + IMPORTE)
    f.close()



    #DATOS DE EJEMPLO #DATOS_CMP_BASE_64 = '{"ver":1,"fecha":"2020-10-13","cuit":30000000007,"ptoVta":10,"tipoCmp":1,"nroCmp":94,"importe":12100,"moneda":"DOL","ctz":65,"tipoDocRec":80,"nroDocRec":20000000001,"tipoCodAut":"E","codAut":70417054367476}' 
    URL = 'https://www.afip.gob.ar/fe/qr/'
    DATOS_CMP_BASE_64 = '{"ver":'+VER+',"fecha":'+data[fecha]+',"cuit":'+data[Cuit]+',"ptoVta":'+data[ptoVta]+',"tipoCmp":'+data[tipoCmp]+',"nroCmp":'+data[nroCmp]+',"importe":'+IMPORTE+',"moneda":'+MONEDA+',"ctz":'+CTZ+',"tipoDocRec":'+data[tipoDocRec]+',"nroDocRec":'+data[nroDocRec]+',"tipoCodAut":'+TIPO_COD_AUT+',"codAut":'+data[codAut]+'}'
    DATOS_CMP_BASE_64_ENCODED = base64.b64encode(bytes(DATOS_CMP_BASE_64, 'utf-8')) # encode a 64
    DATOS_CMP_BASE_64_ENCODED = DATOS_CMP_BASE_64_ENCODED.decode("utf-8") # de 64 hay que hacerle esta decodificacion para que sea string
    qr_string = URL + '?p=' + DATOS_CMP_BASE_64_ENCODED
    print(qr_string)

    # generate qr
    PATH_QR_IMG = "qr_output.jpg"
    img = qrcode.make(qr_string)
    f = open(PATH_QR_IMG, "wb")
    img.save(f)
    f.close()

    #pegar en mascara
    img_bg = Image.open('mascara_a.jpg')    # 428 x 584 px
    img_qr = Image.open('qr_output.jpg')
    img_qr = img_qr.resize((100,100))
    img_bg.paste(img_qr,(20,770))
    img_bg.show()






def on_created(event):
    print("created")
    print(event.src_path)
    magia()

def on_deleted(event):
    print("deleted")

def on_modified(event):
    print("modified")

def on_moved(event):
    print("moved")

if __name__ == "__main__":

    event_handler = FileSystemEventHandler()

    # calling functions
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    folder_to_track = "PDF"
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=False)
    observer.start()
    try:
        print("monitoreando")
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

