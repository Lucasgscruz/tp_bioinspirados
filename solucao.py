#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Solucao:
    def __init__(self):
        self.fitness = sys.maxint
        self.viavel = True
        self.locais = []

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def getViavel(self):
        return self.viavel

    def setViavel(self, valor):
        self.viavel = valor

    def setLocais(self, locais):
        self.locais = locais

    def getLocais(self):
        return self.locais

    def getLocal(self, index):
        return self.locais[index]

    def addLocal(self, local):
        self.locais.append(local)

    def removerLocal(self, index):
        self.locais.pop(index)
