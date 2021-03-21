#import xml.etree.ElementTree as ET 
from xml.dom import minidom
import qrcode
import base64

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

xml = minidom.parse('data/FACB000300001430AFIP.XML')

fields = xml.getElementsByTagName("field")

#extraccion del xml y cargado de datos a data
for field in fields:
    name = field.getAttribute("name")
    if name in data:
        #print(name + ": " + field.firstChild.data)
        data[name] = field.firstChild.data   



# Acomodar fecha con "-"
year = data[fecha][:4] + '-'
month_day = data[fecha][4:]
month_day = month_day[:2] + '-' + month_day[2:]
data[fecha] = '"' + year + month_day + '"' 


# Pedir importe
print('Ingrese el importe total:')
IMPORTE = input()
print("Ok, el importe ingresado es: " + IMPORTE)

#
URL = 'https://www.afip.gob.ar/fe/qr/'
DATOS_CMP_BASE_64 = '{"ver":'+VER+',"fecha":'+data[fecha]+',"cuit":'+data[Cuit]+',"ptoVta":'+data[ptoVta]+',"tipoCmp":'+data[tipoCmp]+',"nroCmp":'+data[nroCmp]+',"importe":'+IMPORTE+',"moneda":'+MONEDA+',"ctz":'+CTZ+',"tipoDocRec":'+data[tipoDocRec]+',"nroDocRec":'+data[nroDocRec]+',"tipoCodAut":'+TIPO_COD_AUT+',"codAut":'+data[codAut]+'}'

DATOS_CMP_BASE_64 = '{"ver":1,"fecha":"2020-10-13","cuit":30000000007,"ptoVta":10,"tipoCmp":1,"nroCmp":94,"importe":12100,"moneda":"DOL","ctz":65,"tipoDocRec":80,"nroDocRec":20000000001,"tipoCodAut":"E","codAut":70417054367476}'


original_data = DATOS_CMP_BASE_64
#print('Original:', original_data)

DATOS_CMP_BASE_64_ENCODED = base64.b64encode(bytes(original_data, 'utf-8'))
#print(DATOS_CMP_BASE_64_ENCODED)






#qr_string="https://www.afip.gob.ar/fe/qr/?p=eyJ2ZXIiOjEsImZlY2hhIjoiMjAyMC0xMC0xMyIsImN1aXQiOjMwMDAwMDAwMDA3LCJwdG9WdGEiOjEwLCJ0aXBvQ21wIjoxLCJucm9DbXAiOjk0LCJpbXBvcnRlIjoxMjEwMCwibW9uZWRhIjoiRE9MIiwiY3R6Ijo2NSwidGlwb0RvY1JlYyI6ODAsIm5yb0RvY1JlYyI6MjAwMDAwMDAwMDEsInRpcG9Db2RBdXQiOiJFIiwiY29kQXV0Ijo3MDQxNzA1NDM2NzQ3Nn0="
# Aca tiene que venir la logica para armar los campos de datos del qr: tiene que cumplir https://www.afip.gob.ar/fe/qr/especificaciones.asp

#DATOS_CMP_BASE_64 = '{"ver":1,"fecha":"2020-07-08","cuit":30710603045,"ptoVta":3,"tipoCmp":6,"nroCmp":1430,"importe":10630,"moneda":"PES","ctz":1,"tipoDocRec":96,"nroDocRec":23183119,"tipoCodAut":"A","codAut":70285829520681}'

#string del codigo qr 
qr_string = URL + '?p=' + DATOS_CMP_BASE_64_ENCODED.decode("utf-8")
print(qr_string)


PATH_QR_IMG = "qr_output.png"
img = qrcode.make(qr_string)
f = open(PATH_QR_IMG, "wb")
img.save(f)
f.close()



