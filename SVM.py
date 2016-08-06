from __future__ import division
from sklearn import svm
import pickle
import os.path
import numpy as np
from sklearn.externals import joblib

class SVM(object):
    """docstring for SVM"""
    c = ""
    kernel = ""
    cantEntrenamiento = None
    cantTest = None
    X = []
    Y = []
    xEntrenamiento = []
    xTest = []
    yEntrenamiento = []
    yTest = []
    clf = None
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self,c,kernel,entrenamiento,test,X=[],Y=[]):
        super(SVM, self).__init__()
        self.c = c
        self.kernel = kernel
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.cantEntrenamiento = entrenamiento
        self.cantTest = test
        self.definirConjuntos()
        if os.path.isfile(self.dir_path+'/persistencia/svm.pkl'):
            self.clf = joblib.load(self.dir_path+'/persistencia/svm.pkl')
        else:
            self.clf = svm.SVC(C=c,kernel=kernel)

    def training(self):
        self.clf.fit(self.xEntrenamiento,self.yEntrenamiento)

    def agregarDocumentosEntrenamiento(self,X,Y):
        self.clf.fit(np.array(X),np.array(Y))


    def testing(self):
        errores = 0
        prediccion = self.predecir(self.xTest)
        cantidadTotal = len(self.xTest)
        for unaClase,unaPrediccion in zip(self.yTest,prediccion):
            if unaClase != unaPrediccion:
                errores +=1
        aciertos = cantidadTotal - errores
        return round((aciertos*100)/cantidadTotal,2)

    def predecir(self,conjunto):
        if len(conjunto) == 1:
            return self.clf.predict(conjunto.reshape(1,-1))
        else:
            return self.clf.predict(conjunto)
    def guardarSVM(self):
        joblib.dump(self.clf, self.dir_path+'/persistencia/svm.pkl')

    def definirConjuntos(self):
        self.xEntrenamiento = self.X[:int(self.cantEntrenamiento*len(self.X))]
        self.xTest = self.X[int(self.cantTest*len(self.X))*int(-1):]
        self.yEntrenamiento = self.Y[:int(self.cantEntrenamiento*len(self.Y))]
        self.yTest = self.Y[int(self.cantTest*len(self.Y))*int(-1):]
