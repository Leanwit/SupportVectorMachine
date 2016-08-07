from SVM import *
from documento import *
from pattern.web import *
from model import *


import os

archivo = open('data/documentos.csv','r').read()
for unaLinea in archivo.split("\n"):
    if unaLinea:
        atributos = unaLinea.split(" , ")
        clase = atributos[0]
        consulta = atributos[1]
        url = atributos[2]

        with db_session:

            unaConsulta = Consulta.get(clave=consulta)
            if not unaConsulta:
                unaConsulta = Consulta(clave=consulta)

            unDocumento = Documento.get(url=url)
            if not unDocumento:
               unDocumento = crearDocumento(url,clase,unaConsulta)
               print unDocumento.html

# unDocumento = documento("http://turismomisiones.com","Turismo")
# enlaces = unDocumento.elemento('a[href=""]')
# for unEnlace in enlaces:
#     print unEnlace.href

# unDocumento = URL("http://turismomisiones.com").download(user_agent='Mozilla/5.0')
# print unDocumento
# unElemento = Element(unDocumento)


#
# # Obtener body
# textBody = ""
# for unBody in unElemento.by_tag('body'):
#     textBody += plaintext(unBody.source)
# # print textBody
#
# # Obtener value of a
# for unAnchor in unElemento('a:first-child'):
    # print plaintext(unAnchor.content)

# SVM
# unSVM = SVM(1.0,'linear',.7,.3,X,Y)
# print "Precision : " ,unSVM.testing()
