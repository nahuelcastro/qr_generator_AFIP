#import xml.etree.ElementTree as ET
from threading import Event
from xml.dom import minidom
import qrcode
import base64
import os, sys, subprocess
#from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from  PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter



def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])








#Variables globales
global IMPORTE
global open_original_pdf
global end_tk


def magia(src_path):
    data = {"CantReg":[],"CbteTipo":[],"Cuit":[],"FchProceso":[],"PtoVta":[],"Reproceso":[],"Resultado":[],"CAE":[],"CAEFchVto":[],"CbteDesde":[],"CbteFch":[],"CbteHasta":[],"Concepto":[],"DocNro":[],"DocTipo":[],"CodAutorizacion":[],"FchVto":[]}

    VER =  '1'
    fecha = 'CbteFch'
    Cuit = 'Cuit'
    CUIT = '' #! COMPLETAR CON 'NUMERO DE CUIT' EN FORMATO STR
    ptoVta = 'PtoVta'
    tipoCmp = 'CbteTipo'
    nroCmp = 'CbteDesde'
    MONEDA = '"PES"'
    CTZ = '1'
    tipoDocRec = 'DocTipo'
    nroDocRec = 'DocNro'
    TIPO_COD_AUT = '"A"'
    codAut = 'CAE'
    global IMPORTE
    IMPORTE = ''
    global m
    m = False

    global open_final_pdf;
    open_final_pdf = True;

    global end_tk
    end_tk = False;

    if(CUIT == ''):
        print('ERROR, VARIABLE CUIT INCOMPLETA')
        print('ERROR, VARIABLE CUIT INCOMPLETA')
        print('ERROR, VARIABLE CUIT INCOMPLETA')
        return 
        

    path = os.getcwd()
    pdf = os.path.basename(src_path)        # example: pdf = 'FACA000300005533'
    base = os.path.splitext(pdf)[0]     #'FACA000300005533'
    folder_info = base
    XML = base + 'AFIP.XML'             #'FACA000300005533AFIP.XML'
    FOLDER_MASTER_INFO = 'Otros'
    FOLDER_MASTER_PDF = 'PDF'
    FOLDER_MASTER_PDF_QR = 'PDF_QR'

    #armado de paths
    path_pdf_original = src_path
    path_info = os.path.join(path, FOLDER_MASTER_INFO, folder_info)
    path_xml = os.path.join(path_info, XML)
    path_importe = os.path.join(path_info, 'importe_total.txt')
    path_pfd_with_qr = os.path.join(path, FOLDER_MASTER_PDF_QR)

    # time.sleep(1)
    # time_start = time.time()
    # if(not os.path.exists(path_xml)):
    #     print('Todavia no existe el xml, voy a darle hasta 30 segundos mas, sino se rompe todo')
    # while (not os.path.exists(path_xml)):
    #     time_now = time.time()
    #     if(time_now - time_start > 30 ):
    #         print('Espere 30 segundos y NO aparecio el xml en: \n ', path_xml)
    #         break
    # time.sleep(1)


    time.sleep(1)

    time_start = time.time()
    if(not os.path.exists(path_xml)):
        print('Todavia no existe el xml, voy a darle hasta 30 segundos mas, sino se rompe todo')
    while ( (not os.access(path_xml, os.F_OK)) and (not os.access(path_xml, os.R_OK))):
        time_now = time.time()
        if(time_now - time_start > 30 ):
            print('Espere 30 segundos y NO aparecio el xml en: \n ', path_xml)
            break
        
    time.sleep(1)




    #extraccion del xml y cargado de datos a data
    xml = minidom.parse(path_xml)
    fields = xml.getElementsByTagName("field")

    for field in fields:
        name = field.getAttribute("name")
        if name in data:
            data[name] = field.firstChild.data


    # Acomodar fecha con "-" example: 20211004 -> 2021-10-04
    year = data[fecha][:4] + '-'
    month_day = data[fecha][4:]
    month_day = month_day[:2] + '-' + month_day[2:]
    data[fecha] = '"' + year + month_day + '"'


    # Pedir importe
    # Tomar el importe de importe_total.txt, en caso de no existir, lo pide y crea
    txt_importe = open(path_importe, "a+")
    txt_importe.close()
    txt_importe = open(path_importe, "r+")
    contenido = txt_importe.read()

    display = tkinter.Tk()
    display.geometry("400x300")
    display.title('QR')


    label = tkinter.Label(display)
    label["text"] = 'Doc: ' + data[nroDocRec]
    label.pack()

    label_fac = tkinter.Label(display)
    label_fac.pack()
    label_fac["text"] = 'N de factura: ' + data[nroCmp]

    label_importe = tkinter.Label(display)
    label_importe.pack()
    label_importe["text"] = 'IMPORTE: '

    CajaTexto = tkinter.Entry(display)
    CajaTexto.insert(0, contenido)
    CajaTexto.pack()


    def Next(event = None):
        global IMPORTE
        global end_tk
        IMPORTE = CajaTexto.get()
        end_tk = True
        display.destroy()

    def OpenOriginalPDF(event = None):
        open_file(src_path)

    
    def CheckboxOpen(event = None):
        global open_final_pdf
        open_final_pdf = var1.get()


    CajaTexto.bind('<Return>', Next)
    button = tkinter.Button(display, text = "Next", command=Next )
    button.pack()

    button_open_pdf = tkinter.Button(display, text = "Abrir PDF original", command=OpenOriginalPDF )
    button_open_pdf.pack()

    var1 = tkinter.BooleanVar()
    c1 = tkinter.Checkbutton(display, text='Abrir PDF al finalizar?',variable=var1, onvalue=True, offvalue=False, command=CheckboxOpen)
    c1.select()
    c1.pack()

    display.mainloop()



    if(end_tk):

        # limpia txt 
        txt_importe.close()
        txt_importe = open(path_importe, "w")

        txt_importe.write(IMPORTE)
        print("Ok, el importe ingresado es: " + IMPORTE)
        print('Importe utilizado: ' + IMPORTE)
        txt_importe.close()


        print(data)
        for x in data:
            print (x);
            print (data[x]);
            print (" ");

        #HARDCODEO:
        # data[codAut] = '71145231295843'
        # data['CAEFchVto'] = '2021-04-15'
        if (data[codAut] == []):
            data[codAut] = data['CodAutorizacion'];
            data['CAEFchVto'] = data['FchVto'];


        #DATOS DE EJEMPLO #
        #DATOS_CMP_BASE_64 = '{"ver":1,"fecha":"2020-10-13","cuit":30000000007,"ptoVta":10,"tipoCmp":1,"nroCmp":94,"importe":12100,"moneda":"DOL","ctz":65,"tipoDocRec":80,"nroDocRec":20000000001,"tipoCodAut":"E","codAut":70417054367476}'
        
        URL = 'https://www.afip.gob.ar/fe/qr/'
        DATOS_CMP_BASE_64 = '{"ver":'+VER+',"fecha":'+data[fecha]+',"cuit":'+CUIT+',"ptoVta":'+data[ptoVta]+',"tipoCmp":'+data[tipoCmp]+',"nroCmp":'+data[nroCmp]+',"importe":'+IMPORTE+',"moneda":'+MONEDA+',"ctz":'+CTZ+',"tipoDocRec":'+data[tipoDocRec]+',"nroDocRec":'+data[nroDocRec]+',"tipoCodAut":'+TIPO_COD_AUT+',"codAut":'+data[codAut]+'}'
        #con str#DATOS_CMP_BASE_64 = '{"ver":'+str(VER)+',"fecha":'+str(data[fecha])+',"cuit":'+str(CUIT)+',"ptoVta":'+str(data[ptoVta])+',"tipoCmp":'+str(data[tipoCmp])+',"nroCmp":'+str(data[nroCmp])+',"importe":'+str(IMPORTE)+',"moneda":'+str(MONEDA)+',"ctz":'+str(CTZ)+',"tipoDocRec":'+str(data[tipoDocRec])+',"nroDocRec":'+str(data[nroDocRec])+',"tipoCodAut":'+str(TIPO_COD_AUT)+',"codAut":'+str(data[codAut])+'}'
        DATOS_CMP_BASE_64_ENCODED = base64.b64encode(bytes(DATOS_CMP_BASE_64, 'utf-8')) # encode a 64
        DATOS_CMP_BASE_64_ENCODED = DATOS_CMP_BASE_64_ENCODED.decode("utf-8") # de 64 hay que hacerle esta decodificacion para que sea string
        qr_string = URL + '?p=' + DATOS_CMP_BASE_64_ENCODED
        print(qr_string)
        #print(DATOS_CMP_BASE_64_ENCODED)
        print('Con estos datos quedo:')
        print(DATOS_CMP_BASE_64)

        # generate qr
        PATH_QR_IMG = "qr_output.jpg"
        img = qrcode.make(qr_string)
        f = open(PATH_QR_IMG, "wb")
        img.save(f)
        f.close()



        ### PDF
        pdf_original = PdfFileReader(path_pdf_original, strict=False)
        page_pdf_original = pdf_original.getPage(0)

        w, h = A4
        path_only_pdf_qr = "only_qr.pdf"
        c = canvas.Canvas(path_only_pdf_qr, pagesize=A4)
        c.drawImage(PATH_QR_IMG, 163 , 23.5, width=79, height=79)
        c.showPage()
        c.save()

        #merge pdfs
        pdf_qr_only = PdfFileReader(path_only_pdf_qr)
        page_pdf_original.mergePage(pdf_qr_only.getPage(0))

        PATH_OUTPUT = os.path.join(path_pfd_with_qr, pdf)   # output.pdf
        output = PdfFileWriter()
        output.addPage(page_pdf_original)
        outputStream = open(PATH_OUTPUT, 'wb')
        output.write(outputStream)
        outputStream.close()

        # if (open_final_pdf is None): 
        #     open_final_pdf = True
        print("OPEEEN", open_final_pdf)
        if(open_final_pdf):
            open_file(PATH_OUTPUT)

    print("monitoreando")




def on_created(event):
    print("created")
    src_path = event.src_path
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

