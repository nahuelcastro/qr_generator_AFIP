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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from  PyPDF2 import PdfFileReader, PdfFileWriter






def magia(src_path):
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

    src_path_without_ext = os.path.splitext(src_path)
    src_path_without_ext = src_path_without_ext[0].split('/')
    filename = src_path_without_ext[len(src_path_without_ext)-1]

    SLASH = '/'
    PDF    = filename                       #'FACA000300005533'
    folder_info_name = filename + SLASH     #'FACA000300005533'
    XML = filename + 'AFIP.XML'             #'FACA000300005533AFIP.XML'
    FOLDER_MASTER_INFO = 'Otros' + SLASH 
    
    #armado de paths
    path_pdf_original = src_path
    path_info = FOLDER_MASTER_INFO + folder_info_name
    path_importe = path_info + 'importe_total'
    path_pfd_with_qr = 'PDF_QR/'

    xml = minidom.parse(path_info + XML)
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
    f = open(path_importe, "a+")
    f.close()
    f = open(path_importe, "r+")
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

    # #pegar en mascara img
    # img_bg = Image.open('mascara_a.jpg')    # 428 x 584 px
    # img_qr = Image.open('qr_output.jpg')
    # img_qr = img_qr.resize((100,100))
    # img_bg.paste(img_qr,(20,770))
    # img_bg.show()


    ### PDF 

    pdf_original = PdfFileReader(path_pdf_original, strict=False)
    page_pdf_original = pdf_original.getPage(0)


    # create pdf with only qr >>> tamaño A4 es  =  (595.275590551181, 841.8897637795275) weight, height
    w, h = A4
    path_only_pdf_qr = "only_qr.pdf"
    c = canvas.Canvas(path_only_pdf_qr, pagesize=A4)
    c.drawImage(PATH_QR_IMG, 18 , 15, width=85, height=85)
    c.showPage()
    c.save()

    #merge pdfs
    pdf_qr_only = PdfFileReader(path_only_pdf_qr)
    page_pdf_original.mergePage(pdf_qr_only.getPage(0))

    PATH_OUTPUT = path_pfd_with_qr + PDF + '.pdf'   # output.pdf
    # PATH_OUTPUT = "output.pdf" #"output.png"
    print (PATH_OUTPUT)
    output = PdfFileWriter()
    output.addPage(page_pdf_original)
    outputStream = open(PATH_OUTPUT, 'wb')
    output.write(outputStream)
    outputStream.close()


    # PATH_OUTPUT = "output.pdf" #"output.png"
    # output = PdfFileWriter()
    # output.addPage(page_pdf_original)
    # outputStream = open(PATH_OUTPUT, 'wb')
    # output.write(outputStream)
    # outputStream.close()





def on_created(event):
    print("created")
    src_path = event.src_path
    print("path: " + src_path)
    if src_path.endswith(('.pdf')):
        magia(src_path)

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

