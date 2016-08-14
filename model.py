from pony.orm import *
from Configuracion import *
from pattern.web import *
from pattern.vector import Document, distance, COSINE, stemmer, PORTER, Model, TFIDF
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
    queryTermRatioTitle = Optional(float)
    queryTermRatioUrlValues = Optional(float)
    queryTermRatioBody = Optional(float)

    querySumTermFrequencyDocumento = Optional(float)
    querySumTermFrequencyTitle = Optional(float)
    querySumTermFrequencyUrlValues = Optional(float)
    querySumTermFrequencyBody = Optional(float)

    queryMinTermFrequencyDocumento = Optional(float)
    queryMinTermFrequencyTitle = Optional(float)
    queryMinTermFrequencyUrlValues = Optional(float)
    queryMinTermFrequencyBody = Optional(float)

    queryMaxTermFrequencyDocumento = Optional(float)
    queryMaxTermFrequencyTitle = Optional(float)
    queryMaxTermFrequencyUrlValues = Optional(float)
    queryMaxTermFrequencyBody = Optional(float)

    queryVarianceTermFrequencyDocumento = Optional(float)
    queryVarianceTermFrequencyTitle = Optional(float)
    queryVarianceTermFrequencyUrlValues = Optional(float)
    queryVarianceTermFrequencyBody = Optional(float)

    queryVectorSpaceModelDocumento = Optional(float)
    queryVectorSpaceModelTitle = Optional(float)
    queryVectorSpaceModelUrlValues = Optional(float)
    queryVectorSpaceModelBody = Optional(float)

    querySumTfidfDocumento = Optional(float)
    querySumTfidfTitle = Optional(float)
    querySumTfidfUrlValues = Optional(float)
    querySumTfidfBody = Optional(float)

    queryMinTfidfDocumento = Optional(float)
    queryMinTfidfTitle = Optional(float)
    queryMinTfidfUrlValues = Optional(float)
    queryMinTfidfBody = Optional(float)

    queryMaxTfidfDocumento = Optional(float)
    queryMaxTfidfTitle = Optional(float)
    queryMaxTfidfUrlValues = Optional(float)
    queryMaxTfidfBody = Optional(float)

    queryPromTfidfDocumento = Optional(float)
    queryPromTfidfTitle = Optional(float)
    queryPromTfidfUrlValues = Optional(float)
    queryPromTfidfBody = Optional(float)


    def setQueryTermNumber(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryTermNumberDocumento = self.contarNumeroAparicion(html,unaQuery)
        self.queryTermNumberUrl = self.contarNumeroAparicion(unDocumento.url,unaQuery)
        self.queryTermNumberTitle = self.contarNumeroAparicion(titulo,unaQuery)
        self.queryTermNumberUrlValues = self.contarNumeroAparicion(urlValues,unaQuery)
        self.queryTermNumberBody = self.contarNumeroAparicion(body,unaQuery)

    def setQueryTermRatio(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryTermRatioDocumento = self.contarFrecuenciaAparicion(html,unaQuery)
        self.queryTermRatioTitle = self.contarFrecuenciaAparicion(titulo,unaQuery)
        self.queryTermRatioUrlValues = self.contarFrecuenciaAparicion(urlValues,unaQuery)
        self.queryTermRatioBody = self.contarFrecuenciaAparicion(body,unaQuery)

    def setIDF(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryIDFDocumento = self.calcularIDF(html,unaQuery)
        self.queryIDFTitle = self.calcularIDF(titulo,unaQuery)
        self.queryIDFUrlValues = self.calcularIDF(urlValues,unaQuery)
        self.queryIDFBody = self.calcularIDF(body,unaQuery)

    def setQuerySumTermFrequency(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.querySumTermFrequencyDocumento = self.calcularSumTermFrequency(html,unaQuery)
        self.querySumTermFrequencyTitle = self.calcularSumTermFrequency(titulo,unaQuery)
        self.querySumTermFrequencyUrlValues = self.calcularSumTermFrequency(urlValues,unaQuery)
        self.querySumTermFrequencyBody = self.calcularSumTermFrequency(body,unaQuery)

    def setQueryMinTermFrequency(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryMinTermFrequencyDocumento = self.calcularMinTermFrequency(html,unaQuery)
        self.queryMinTermFrequencyTitle = self.calcularMinTermFrequency(titulo,unaQuery)
        self.queryMinTermFrequencyUrlValues = self.calcularMinTermFrequency(urlValues,unaQuery)
        self.queryMinTermFrequencyBody = self.calcularMinTermFrequency(body,unaQuery)


    def setQueryMaxTermFrequency(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryMaxTermFrequencyDocumento = self.calcularMaxTermFrequency(html,unaQuery)
        self.queryMaxTermFrequencyTitle = self.calcularMaxTermFrequency(titulo,unaQuery)
        self.queryMaxTermFrequencyUrlValues = self.calcularMaxTermFrequency(urlValues,unaQuery)
        self.queryMaxTermFrequencyBody = self.calcularMaxTermFrequency(body,unaQuery)

    def setQueryVarianceTermFrequency(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryVarianceTermFrequencyDocumento = self.calcularVarianceTermFrequency(html,unaQuery)
        self.queryVarianceTermFrequencyTitle = self.calcularVarianceTermFrequency(titulo,unaQuery)
        self.queryVarianceTermFrequencyUrlValues = self.calcularVarianceTermFrequency(urlValues,unaQuery)
        self.queryVarianceTermFrequencyBody = self.calcularVarianceTermFrequency(body,unaQuery)

    def setQueryVectorSpaceModel(self,unDocumento,unaQuery,html,titulo,body,urlValues):
        self.queryVectorSpaceModelDocumento = self.calcularVectorSpaceModel(html,unaQuery)
        self.queryVectorSpaceModelTitle = self.calcularVectorSpaceModel(titulo,unaQuery)
        self.queryVectorSpaceModelUrlValues = self.calcularVectorSpaceModel(urlValues,unaQuery)
        self.queryVectorSpaceModelBody = self.calcularVectorSpaceModel(body,unaQuery)



    def contarNumeroAparicion(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                 contador += 1
        return contador

    def contarFrecuenciaAparicion(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            try:
                contador += string[unTermino]
            except:
                pass
        contador = contador / len(unaQuery)
        return contador

    def calcularIDF(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                 contador += string.tfidf(unTermino)
        return contador

    def calcularSumTermFrequency(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                 contador += string.tf(unTermino)
        return contador

    def calcularMinTermFrequency(self,string,unaQuery):
        contador = 1.1
        for unTermino in unaQuery:
            if unTermino in string:
                 if contador > string.tf(unTermino):
                    contador = string.tf(unTermino)
        return contador

    def calcularMaxTermFrequency(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                 if contador < string.tf(unTermino):
                    contador = string.tf(unTermino)
        return contador

    def calcularVarianceTermFrequency(self,string,unaQuery):
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                contador += string.tf(unTermino)
        promedio = contador / len(unaQuery)
        contador = 0
        for unTermino in unaQuery:
            if unTermino in string:
                contador += (string.tf(unTermino)- promedio)**2
        contador = contador / len(unaQuery)
        return contador

    def calcularVectorSpaceModel(self,string,unaQuery):
        return distance(string, unaQuery, method=COSINE)

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
    unaConsulta = unDocumento.consulta
    unaQuery = Document(unaConsulta.clave)
    html = Document(unDocumento.html)
    titulo = Document(unDocumento.titulo)
    body = Document(unDocumento.body)
    urlValues = Document(unDocumento.urlValues)

    unAtributo = Atributo(documento=unDocumento)
    unAtributo.setQueryTermNumber(unDocumento,unaQuery.words,html.words,titulo.words,body.words,urlValues.words)
    unAtributo.setQueryTermRatio(unDocumento,unaQuery.vector,html.vector,titulo.vector,body.vector,urlValues.vector)
    unAtributo.setQuerySumTermFrequency(unDocumento,unaQuery,html,titulo,body,urlValues)
    unAtributo.setQueryMinTermFrequency(unDocumento,unaQuery,html,titulo,body,urlValues)
    unAtributo.setQueryMaxTermFrequency(unDocumento,unaQuery,html,titulo,body,urlValues)
    unAtributo.setQueryVarianceTermFrequency(unDocumento,unaQuery,html,titulo,body,urlValues)
    unAtributo.setQueryVectorSpaceModel(unDocumento,unaQuery.vector,html.vector,titulo.vector,body.vector,urlValues.vector)

    return unAtributo

def getDocumentosAtributos(metodo):
    with db_session:
        X = []
        listaDocumentos = []
        if metodo == 'predecir':
            for p in select(p for p in Documento if p.clase == -1):
                atributos = Atributo.get(documento = p)
                atributosAux = getAtributos(atributos)
                X.append(atributosAux)
                listaDocumentos.append(p.id)
        elif metodo == 'entrenamiento':
            for p in select(p for p in Documento if p.clase != -1):
                atributos = Atributo.get(documento = p)
                atributosAux = getAtributos(atributos)
                X.append(atributosAux)
                listaDocumentos.append(p.id)

    # Metodo para obtener atributos que dependen del corpus entero
    getDocumentosAtributosCorpus(listaDocumentos)
    return X

def getDocumentosAtributosCorpus(listaDocumentos):
    with db_session:
        for unaConsulta in Consulta.select():
            listaDocumentosHtml, listaDocumentosBody, listaDocumentosUrlValues, listaDocumentosTitle,listaDocumentosID = ([] for i in range(5))
            for unDocumento in listaDocumentos:
                unDocumento = Documento[unDocumento]
                if unaConsulta.clave == unDocumento.consulta.clave:
                    listaDocumentosHtml.append(Document(unDocumento.html,stemmer=PORTER,weigth=TFIDF))
                    listaDocumentosBody.append(Document(unDocumento.body,stemmer=PORTER,weigth=TFIDF))
                    listaDocumentosUrlValues.append(Document(unDocumento.urlValues,stemmer=PORTER,weigth=TFIDF))
                    listaDocumentosTitle.append(Document(unDocumento.titulo,stemmer=PORTER,weigth=TFIDF))
                    listaDocumentosID.append(unDocumento.id)
            modelos = {}
            modelos['documento'] = Model(listaDocumentosHtml)
            modelos['body'] = Model(listaDocumentosBody)
            modelos['urlValues'] = Model(listaDocumentosUrlValues)
            modelos['title'] = Model(listaDocumentosTitle)
            calcularAtributosCorpus(modelos,unaConsulta,listaDocumentosID)

def calcularAtributosCorpus(modelos,unaConsulta,listaDocumentos):
    for unModelo in modelos:
        calcularAtributosCorpusSum(modelos[unModelo],unModelo,unaConsulta,listaDocumentos)
        calcularAtributosCorpusMin(modelos[unModelo],unModelo,unaConsulta,listaDocumentos)
        calcularAtributosCorpusMax(modelos[unModelo],unModelo,unaConsulta,listaDocumentos)
        calcularAtributosCorpusProm(modelos[unModelo],unModelo,unaConsulta,listaDocumentos)




def calcularAtributosCorpusSum(modelos,atributo,consulta,listaDocumentos):
    contador = 0
    listaDocumentosBD = Documento.select(lambda p: p.consulta == consulta)
    consulta = Document(consulta.clave,stemmer=PORTER)
    for unDocumento,unDocumentoBD in zip(modelos,listaDocumentos):
        for unaConsulta in consulta:
            contador += unDocumento.tfidf(unaConsulta)
        unAtributo = Atributo.get(documento = unDocumentoBD)
        diccionario = {'querySumTfidf'+getNameAtributo(atributo):contador}
        unAtributo.set(**diccionario)

def getNameAtributo(unAtributo):
    if "documento" in unAtributo:
        return "Documento"
    elif "body" in unAtributo:
        return "Body"
    elif "url" in unAtributo:
        return "UrlValues"
    elif "title" in unAtributo:
        return "Title"

def calcularAtributosCorpusMax(modelos,atributo,consulta,listaDocumentos):
    consulta = Document(consulta.clave,stemmer=PORTER)
    for unDocumento,unDocumentoBD in zip(modelos,listaDocumentos):
        contador = 0
        for unaConsulta in consulta:
            contadorAux = unDocumento.tfidf(unaConsulta)
            if contador < contadorAux:
                contador = contadorAux
        unAtributo = Atributo.get(documento = unDocumentoBD)
        diccionario = {'queryMaxTfidf'+getNameAtributo(atributo):contador}
        unAtributo.set(**diccionario)

def calcularAtributosCorpusMin(modelos,atributo,consulta,listaDocumentos):
    consulta = Document(consulta.clave,stemmer=PORTER)
    for unDocumento,unDocumentoBD in zip(modelos,listaDocumentos):
        contador = 100
        for unaConsulta in consulta:
            contadorAux = unDocumento.tfidf(unaConsulta)
            if contador > contadorAux:
                contador = contadorAux
        unAtributo = Atributo.get(documento = unDocumentoBD)
        diccionario = {'queryMinTfidf'+getNameAtributo(atributo):contador}
        unAtributo.set(**diccionario)

def calcularAtributosCorpusProm(modelos,atributo,consulta,listaDocumentos):
    consulta = Document(consulta.clave,stemmer=PORTER)
    for unDocumento,unDocumentoBD in zip(modelos,listaDocumentos):
        contador = 0
        for unaConsulta in consulta:
            contador += unDocumento.tfidf(unaConsulta)
        contador = contador / len(consulta)
        unAtributo = Atributo.get(documento = unDocumentoBD)
        diccionario = {'queryPromTfidf'+getNameAtributo(atributo):contador}
        unAtributo.set(**diccionario)

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
