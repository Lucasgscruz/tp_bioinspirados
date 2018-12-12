#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Local:
    def __init__(self, index, capacidade):
        self.id = index
        self.capacidade = capacidade
        self.ocupacao = 0
        self.regioesAtendidas = []

    def getId(self):
        return self.id

    def setCapacidade(self, capacidade):
        self.capacidade = capacidade

    def getCapacidade(self):
        return self.capacidade

    def setOcupacao(self, ocupacao):
        self.ocupacao = ocupacao

    def getOcupacao(self):
        return self.ocupacao

    def addOcupacao(self, demanda):
        self.ocupacao += demanda

    def removerOcupacao(self, demanda):
        self.ocupacao = self.ocupacao - demanda

    def setRegioesAtendidas(self, regioes):
        self.regioesAtendidas = regioes

    def getRegioesAtendidas(self):
        return self.regioesAtendidas

    def addRegiao(self, idRegiao):
        self.regioesAtendidas.append(idRegiao)

    def removerRegiao(self, index):
        self.regioesAtendidas.pop(index)
