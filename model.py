from pony.orm import *
from Configuracion import *
from pattern.web import *
from pattern.vector import Document
import sys

unaConfiguracion = Configuracion()
db = Database()


class Consulta(db.Entity):
    id = PrimaryKey(int, auto=True)
    documentos = Set('Documento')
    clave = Required(str)

class Documento(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Required(str)
    clase = Required(int)
    consulta = Required(Consulta)
    atributo = Optional('Atributo')
    html = Optional(LongStr)
    body = Optional(LongStr)
    urlValues = Optional(LongStr)
    titulo = Optional(LongStr)

class Atributo(db.Entity):
    id = PrimaryKey(int, auto=True)
    documento = Required(Documento)
    queryTermNumberDocumento = Optional(int)
    queryTermNumberUrl = Optional(int)
    queryTermNumberTitle = Optional(int)
    queryTermNumberUrlValues = Optional(int)
    queryTermNumberBody = Optional(int)
    queryTermRatioDocumento = Optional(float)
    queryTermRatioUrl = Optional(float)
    queryTermRatioTitle = Optional(float)
    queryTermRatioUrlValues = Optional(float)

    def setearQueryTermNumber(self,unDocumento):
        unaConsulta = unDocumento.consulta
        unaQuery = Document(unaConsulta.clave).words
        html = Document(unDocumento.html).words
        titulo = Document(unDocumento.titulo).words
        self.queryTermNumberDocumento = self.contarNumeroAparicion(html,unaQuery)
        self.queryTermNumberUrl = self.contarNumeroAparicion(unDocumento.url,unaQuery)
        self.queryTermNumberTitle = self.contarNumeroAparicion(titulo,unaQuery)
        self.queryTermNumberUrlValues = self.contarNumeroAparicion(unDocumento.urlValues,unaQuery)
        self.queryTermNumberBody = self.contarNumeroAparicion(unDocumento.body,unaQuery)


    def contarNumeroAparicion(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                contador += 1
        return contador


db.bind(unaConfiguracion.bd, host=unaConfiguracion.host, user=unaConfiguracion.user, passwd=unaConfiguracion.passwd, db=unaConfiguracion.db)
db.generate_mapping(create_tables=True)

def crearDocumento(url,clase,consulta):
    unDocumento = Documento(url=url,clase=clase,consulta=consulta)
    print "Descargando -> ", unDocumento.url
    try:
        html = URL(unDocumento.url,unicode=False).download(user_agent='Mozilla/5.0')
        unDocumento.html = decode_utf8(html)
        unDocumento.body = ""
        unElemento = Element(html)
        for unBody in unElemento.by_tag('body'):
            unDocumento.body += plaintext(decode_utf8(unBody.source))

        unDocumento.urlValues = ""
        for unValueUrl in unElemento('a:first-child'):
             unDocumento.urlValues += plaintext(decode_utf8(unValueUrl.content))+ " - "
        if unElemento.by_tag('title'):
            unDocumento.titulo = decode_utf8(unElemento.by_tag('title')[0].content)
    except Exception,e:
        print "Excepcion en Descargar el archivo ", unDocumento.url
        print "Motivo : ", str(e)
    return unDocumento

def crearAtributos(unDocumento):
    unAtributo = Atributo(documento=unDocumento)
    unAtributo.setearQueryTermNumber(unDocumento)
    return unAtributo

def getDocumentosAtributos(metodo):
    with db_session:
        X = []
        if metodo == 'predecir':
            for p in select(p for p in Documento if p.clase == -1):
                atributos = Atributo.get(documento = p)
                atributosAux = getAtributos(atributos)

                X.append(atributosAux)
        elif metodo == 'entrenamiento':
            for p in select(p for p in Documento if p.clase != -1):
                atributos = Atributo.get(documento = p)
                atributosAux = getAtributos(atributos)
                X.append(atributosAux)
    return X

def getAtributos(atributos):
    atributosAux = []
    for attr,value in atributos.to_dict(exclude="id,documento").iteritems():
        if value == None:
            value = 0
        atributosAux.append(value)
    return atributosAux


def getDocumentosClase():
    with db_session:
        Y = []
        for p in select(p for p in Documento):
            if p.clase != -1:
                Y.append(p.clase)
    return Y

def lecturaArchivo(archivo,metodo):
    archivo = open(archivo,'r').read()
    for unaLinea in archivo.split("\n"):
        if unaLinea:
            atributos = unaLinea.split(" , ")
            consulta = atributos[0]
            url = atributos[1]
            if metodo == "predecir":
                clase = -1
            else:
                clase = atributos[2]
            duplicar = 0
            with db_session:
                if not duplicar :
                    unaConsulta = Consulta.get(clave=consulta)
                    if not unaConsulta:
                        unaConsulta = Consulta(clave=consulta)
                        unDocumento = crearDocumento(url,clase,unaConsulta)
                        unAtributo = crearAtributos(unDocumento)
                    else:
                        unDocumento = Documento.get(url=url,consulta=unaConsulta)
                        if not unDocumento:
                            unDocumento = crearDocumento(url,clase,unaConsulta)
                            unAtributo = crearAtributos(unDocumento)
                        else:
                            unAtributo = Atributo.get(documento=unDocumento)
                            if not unAtributo:
                                unAtributo = crearAtributos(unDocumento)
                else:
                    unaConsulta = Consulta(clave=consulta)
                    unDocumento = crearDocumento(url,clase,unaConsulta)
                    unAtributo = crearAtributos(unDocumento)
