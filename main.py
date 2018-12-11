#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import random
import solucao as sol
import local
import copy as cp

# Leitura dos arquivos csv
capacidade = pd.read_csv('instancia/capacidades.csv', sep = '\t', header = None) # Capacidade dos locais (de votacao)
demandas = pd.read_csv('instancia/demandas.csv', sep = '\t', header = None)  # Demandas de cada setor(regiao)
distancias = pd.read_csv('instancia/distancias.csv', sep = ';', header = None) # Distancias regiao x local

# Constantes globais
maxDist = 3000  # Distancia máxima admitida (maior distancia da instancia: 12487)
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

        listaSetores = random.sample(range(len(demandas[0])), len(demandas[0])) # sequencia aleatoria de setores

        while(len(listaSetores) > 0):# Atribui as demandas das regioes da cidade aos locais de votacao
        	cont = random.randint(0, 165)
            # Verifica a capacidade maxima do local de votaçao
        	if(s.getLocal(cont).getOcupacao() + demandas[0][listaSetores[0]] <= s.getLocal(cont).getCapacidade() and
            distancias[cont][listaSetores[0]] <= maxDist):
        		s.getLocal(cont).addRegiao(listaSetores[0])
        		s.getLocal(cont).addOcupacao(demandas[0][listaSetores[0]])
        		listaSetores.pop(0)
        calculaFitness(s)
        populacao.append(s)
    return populacao

# Função que calcula o fitness
def calculaFitness(s):
    fit = 0
    penalidadeDistancia = 1000000
    penalidadeCapacidade = 10000000
    s.setViavel(True)
    for i in s.getLocais():
        for j in i.getRegioesAtendidas():
            fit = fit + demandas[0][j] * distancias[i.getId()][j]
            if(distancias[i.getId()][j] > maxDist):
                # print "Distancia ",i.getId(), j, distancias[i.getId()][j], "maxDist:", maxDist
                s.setViavel(False)
                fit += penalidadeDistancia
        if (i.getOcupacao() > i.getCapacidade()):
            # print "ocupacao"
            s.setViavel(False)
            fit += penalidadeCapacidade
    s.setFitness(fit)

# Exibir atributos de individuo
def exibeIndividuo(individuo):
    for i in individuo.getLocais():
        print i.getId(), '->' ,i.getRegioesAtendidas()
    print "Fitness:", individuo.getFitness(), " Viável:", individuo.getViavel()

def gera_clones(pop_clonar):
    clones = []
    for i in range(len(pop_clonar)):
        k = 0
        while(k < num_clones[i]):
            clones.append(cp.deepcopy(pop_clonar[i]))
            k += 1
    return clones

def clonalg(populacao):
    fitness = []
    for i in populacao:
        fitness.append(i.getFitness())
    fit_ordenado = cp.copy(fitness)
    fit_ordenado.sort()

    pop_clonar = []
    for i in range(0, 10): # 10 individuos a serem clonados
    	index = fitness.index(fit_ordenado[i])
    	pop_clonar.append(populacao[index])
    clones = gera_clones(pop_clonar)
    print len(clones), "tamanho len clones"
    print sum(num_clones), "somatorio, deveria ser isso"

    # clones = mutar(clones)
    # populacao_intermediaria = popInicial(tamanho_populacao - quant_clones)
    # populacao = clones
    # populacao.append(populacao_intermediaria)

if __name__ == '__main__':
    populacao = popInicial(tamanho_populacao)
    clonalg(populacao)
