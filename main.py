#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import random
import solucao as sol
import local


# Leitura dos arquivos csv
capacidade = pd.read_csv('instancia/capacidades.csv', sep = '\t', header = None) # Capacidade dos locais (de votacao)
demandas = pd.read_csv('instancia/demandas.csv', sep = '\t', header = None)  # Demandas de cada setor(regiao)
distancias = pd.read_csv('instancia/distancias.csv', sep = ';', header = None) # Distancias regiao x local
maxDist = 1000000  # Distancia máxima admitida
tamanho_populacao = 100
num_clones = [10,8,6,4,2,2,2,2,2,2]
mut_clones = [0.01, 0.02, 0.04, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

# Constrói a populacao inicial
def popInicial(numIndividuos):
    populacao = []
    for i in range(numIndividuos):
        s = sol.Solucao()
        for i in range(len(capacidade[0])): # Adiciona os locais de votacao ao array locais
            localVotacao = local.Local(i, capacidade[0][i])
            s.addLocal(localVotacao)

        cont = 0
        listaSetores = random.sample(range(len(demandas[0])), len(demandas[0])) # sequencia aleatoria de setores
        while(len(listaSetores) > 0):# Atribui as demandas das regioes da cidade aos locais de votacao
        	cont = random.randint(0, 165)
        	if(s.getLocal(cont).getOcupacao() + demandas[0][listaSetores[0]] <= s.getLocal(cont).getCapacidade()):
        		s.getLocal(cont).addRegiao(listaSetores[0])
        		s.getLocal(cont).addOcupacao(demandas[0][listaSetores[0]])
        		listaSetores.pop(0)
        populacao.append(s)
    #exibeIndividuo(populacao[0])
    calculaFitness(populacao[0])
    print populacao[0].getFitness()
    return populacao

# Função que calcula o fitness
def calculaFitness(s):
    fit = 0
    penalidadeDistancia = 1000
    penalidadeCapacidade = 100000
    for i in s.getLocais():
    	print 'local', i.getId()
        for j in i.getRegioesAtendidas():
        	fit = fit + demandas[0][j] * distancias[i.getId()][j]
        	if(distancias[i.getId()][j] > maxDist):
        		fit += penalidadeDistancia
        if (i.getOcupacao() > i.getCapacidade()):
        	fit += penalidadeCapacidade

    s.setFitness(fit)
# def gera_clones(populacao):
# 	clones = []

def exibeIndividuo(individuo):
	for i in individuo.getLocais():
		print i.getId(), '->' ,i.getRegioesAtendidas()


def clonalg(populacao):
    fitness = list(map(calculaFitness, populacao))
    fit_ordenado = fitness.sort(reverse = True)
    pop_clonar = []
    for i in range(0, 10):
    	index = fitness.index(fit_ordenado[i])
    	pop_clonar.append(populacao[index])
    clones = gera_clones(pop_clonar, quant_clones)
    clones = mutar(clones)
    populacao_intermediaria = popInicial(tamanho_populacao - quant_clones)
    populacao = clones
    populacao.append(populacao_intermediaria)

if __name__ == '__main__':
	populacao = popInicial(tamanho_populacao)
    #clonalg(populacao)
