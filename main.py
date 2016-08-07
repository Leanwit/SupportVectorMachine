from SVM import *
from documento import *
from pattern.web import *
from model import *


import os

lecturaArchivo('data/documentos.csv','entrenamiento')

X = getDocumentosAtributos('entrenamiento')
Y = getDocumentosClase()
unSVM = SVM(1.0,'poly',.7,.3,X,Y)
unSVM.training()
print "Precision : " ,unSVM.testing()

lecturaArchivo('data/prediccion.csv','predecir')
X = getDocumentosAtributos('predecir')
print unSVM.predecir(X)
