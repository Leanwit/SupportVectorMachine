from SVM import *
from documento import *

unDocumento = documento("http://turismomisiones.com","Turismo")
enlaces = unDocumento.elemento('a[href=""]')
for unEnlace in enlaces:
    print unEnlace.href


# unSVM = SVM(1.0,'linear',.7,.3,X,Y)
# print "Precision : " ,unSVM.testing()
