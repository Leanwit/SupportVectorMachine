from pattern.web import download, URL, plaintext, blocks, Element


class documento(object):
    """docstring for documento"""

    url = ""
    clase = ""
    atributos = {}
    query = ""
    html = ""
    contenido = ""
    elemento = None
    # unDocumento.elemento('a[href=""]') Para obtener solo los enlaces con href

    def __init__(self,url, query):
        super(documento, self).__init__()
        self.url = url
        self.urlObjet = URL('http://www.clips.ua.ac.be')
        self.html = self.urlObjet.download(user_agent='Mozilla/5.0')
        self.contenido = plaintext(self.html, keep=[], replace=blocks, linebreaks=2, indentation=False)
        self.elemento = Element(self.html)

    def save(self,arg):
        pass

    def descargar(self, arg):
        pass

    def obtenerAtributos(self,arg):
        pass

    def setUnAtributo(self,atributo,valor):
        pass
