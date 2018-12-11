#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import random
import solucao as sol
import local


# Leitura dos arquivos csv
capacidade = pd.read_csv('instancia/capacidades.csv', sep = '\t', header = None) # Capacidade dos locais (de votacao)
demandas = pd.read_csv('instancia/demandas.csv', sep = '\t', header = None)  # Demandas de cada setor(regiao)
distancias = pd.read_csv('instancia/distancias.csv', sep = '\t', header = None) # Distancias regiao x local
maxDist = 1000000  # Distancia máxima admitida

# Constrói a populacao inicial
def popInicial(numIndividuos):
    populacao = []
    for i in range(numIndividuos):
        s = sol.Solucao()
        for i in range(len(capacidade[0])): # Adiciona os locais de votacao ao array locais
            localVotacao = local.Local(i, capacidade[0][i])
            s.addLocal(localVotacao)

        cont = 0
        contSetor = 0
        listaSetores = random.sample(range(len(demandas[0])), len(demandas[0])) # sequencia aleatoria de setores
        while(len(listaSetores) > 0): # Atribui as demandas das regioes da cidade aos locais de votacao
            if(s.getLocal(cont).getOcupacao() + demandas[0][contSetor] <= s.getLocal(cont).getCapacidade()):
                s.getLocal(cont).addRegiao(listaSetores[contSetor])
                s.getLocal(cont).addOcupacao(demandas[0][contSetor])
                listaSetores.pop(0)
                cont += 1
                contSetor += 1
            else:
                cont += 1

            if(cont >= len(capacidade[0])):
                cont = 0

# Função que calcula o fitness
def calculaFitness(s):
    fit = 0
    penalidadeDistancia = 1000
    penalidadeCapacidade = 100000
    for i in s.getLocais():
        for j in i.getRegioesAtendidas():
            fit = fit + demandas[0][j] * distancias[i.getId()][j]
            if(distancias[i.getId()][j] > maxDist):
                fit += penalidadeDistancia
        if (i.getOcupacao() > i.getCapacidade()):
            fit += penalidadeCapacidade

    s.setFitness(fit)

def main():
    popInicial(2)

if __name__ == '__main__':
    main()
