from  PyPDF2 import PdfFileReader, PdfFileWriter
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


PATH_FILE = 'factura_original.pdf'
pdf = PdfFileReader(PATH_FILE)


# read pdf
number_of_pages = pdf.getNumPages()
print (number_of_pages)
page = pdf.getPage(0)
page_content = page.extractText()
print (page_content)


URL = 'https://www.afip.gob.ar/fe/qr/'
DATOS_CMP_BASE_64 = 'HACER MAGIA, ABAJO METO UN MINI HARDCODEO DE EJEMPLO'
DATOS_CMP_BASE_64 = '{"ver":1,"fecha":"2020-10-13","cuit":30000000007,"ptoVta":10,"tipoCmp":1,"nroCmp":94,"importe":12100,"moneda":"DOL","ctz":65,"tipoDocRec":80,"nroDocRec":20000000001,"tipoCodAut":"E","codAut":70417054367476}'
#qr_string="https://www.afip.gob.ar/fe/qr/?p=eyJ2ZXIiOjEsImZlY2hhIjoiMjAyMC0xMC0xMyIsImN1aXQiOjMwMDAwMDAwMDA3LCJwdG9WdGEiOjEwLCJ0aXBvQ21wIjoxLCJucm9DbXAiOjk0LCJpbXBvcnRlIjoxMjEwMCwibW9uZWRhIjoiRE9MIiwiY3R6Ijo2NSwidGlwb0RvY1JlYyI6ODAsIm5yb0RvY1JlYyI6MjAwMDAwMDAwMDEsInRpcG9Db2RBdXQiOiJFIiwiY29kQXV0Ijo3MDQxNzA1NDM2NzQ3Nn0="
# Aca tiene que venir la logica para armar los campos de datos del qr: tiene que cumplir https://www.afip.gob.ar/fe/qr/especificaciones.asp
qr_string = URL + '?p=' + DATOS_CMP_BASE_64

print (qr_string)

# generate qr 
PATH_QR_IMG = "qr_output.png"
img = qrcode.make(qr_string)
f = open(PATH_QR_IMG, "wb")
img.save(f)
f.close()


# write pdf with hola mundo   # >>> tamaño A4 es  =  (595.275590551181, 841.8897637795275) weight, height
w, h = A4
PATH_ONLY_PDF_QR = "only_qr.pdf"
c = canvas.Canvas(PATH_ONLY_PDF_QR, pagesize=A4)
c.drawImage(PATH_QR_IMG, w/2 , h/2, width=90, height=90)
c.showPage()
c.save()


pdf_qr_only = PdfFileReader(PATH_ONLY_PDF_QR);
page.mergePage(pdf_qr_only.getPage(0))

PATH_OUTPUT = "output.png"
output = PdfFileWriter()
output.addPage(page)
outputStream = open(PATH_OUTPUT, 'wb')
output.write(outputStream)
outputStream.close()


