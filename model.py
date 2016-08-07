from pony.orm import *
from Configuracion import *

unaConfiguracion = Configuracion()
db = Database()


class Consulta(db.Entity):
    id = PrimaryKey(int, auto=True)
    documentos = Set('Documento')
    clave = Required(str)

class Documento(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Required(str)
    clase = Required(bool)
    consulta = Required(Consulta)
    atributo = Optional('Atributo')
    html = Optional(LongStr)
    body = Optional(LongStr)
    anchor = Optional(LongStr)
    documentoPattern = Optional(unicode)

class Atributo(db.Entity):
    id = PrimaryKey(int, auto=True)
    documento = Required(Documento)
    queryTermNumberDocumento = Required(int)
    queryTermNumberAnchor = Required(int)
    queryTermNumberTitle = Required(int)
    queryTermNumberUrl = Required(int)
    queryTermRatioDocumento = Required(float)
    queryTermRatioAnchor = Required(float)
    queryTermRatioTitle = Required(float)
    queryTermRatioUrl = Required(float)

db.bind(unaConfiguracion.bd, host=unaConfiguracion.host, user=unaConfiguracion.user, passwd=unaConfiguracion.passwd, db=unaConfiguracion.db)
db.generate_mapping(create_tables=True)

def crearDocumento(url,clase,consulta):
    unDocumento = Documento(url=url,clase=clase,consulta=consulta)
    unDocumento.html = URL(unDocumento.url).donwload()
    return unDocumento
