#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import random
import time
import solucao as sol
import local
import copy as cp

# Leitura dos arquivos csv
capacidade = pd.read_csv('instancia/capacidades.csv', sep = '\t', header = None) # Capacidade dos locais (de votacao)
demandas = pd.read_csv('instancia/demandas.csv', sep = '\t', header = None)  # Demandas de cada setor(regiao)
distancias = pd.read_csv('instancia/distancias.csv', sep = ';', header = None) # Distancias regiao x local

# Constantes globais
maxDist = 3000  # Distancia máxima admitida (maior distancia da instancia: 12487)
tamanho_populacao = 200
num_clones = [10,8,6,4,2,2,2,2,2,2]
mut_clones = [0.01, 0.02, 0.04, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
geracoes = 2

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

# Produz os clones dos individuos recebidos como parametro
def gera_clones(pop_clonar):
    clones = []
    for i in range(len(pop_clonar)):
        k = 0
        while(k < num_clones[i]):
            clones.append(cp.deepcopy(pop_clonar[i]))
            k += 1
    return clones

# Realiza mutação nos clones
def muta_clones(clones):
    for i in range(0, len(num_clones)):
        k = 0
        while(k < num_clones[i]): #Só pra garantir que o vetor do num_clones e mutação estejam na mesma pos
            for j in clones[k].getLocais():
                rand = random.uniform(0.0, 1.0)
                if(rand < mut_clones[i]):
                    #print 'mutou'
                    rand2 = random.randint(0, 165)
                    #print 'saiu de', j.getId()
                    #print 'foi para', rand2
                    setor_atendido = j.getRegioesAtendidas()
                    if len(setor_atendido) is not 0:
                        setor_muda = setor_atendido[0]
                        if(clones[k].getLocal(rand2).getOcupacao() + demandas[0][setor_muda] <=
                        clones[k].getLocal(rand2).getCapacidade() and
                        distancias[clones[k].getLocal(rand2).getId()][setor_muda] <= maxDist):
                            j.removerRegiao(0)
                            j.removerOcupacao(demandas[0][setor_muda])
                            clones[k].getLocal(rand2).addRegiao(setor_muda)
            calculaFitness(clones[k])
            k += 1
    return clones

def gera_nova_pop(clones, populacao_intermediaria):
    populacao = []
    for i in range(len(clones)):
        populacao.append(clones[i])
    for j in range(len(populacao_intermediaria)):
        populacao.append(populacao_intermediaria[i])
    return populacao

def somaLocais(individuo):
    soma = 0
    for i in individuo.getLocais():
        if(len(i.getRegioesAtendidas()) > 0):
            soma += 1
    return soma

def clonalg(populacao):
    y = 0
    melhores_fit = []
    melhores_indiv = []
    while (y < geracoes):
        fitness = []
        for i in populacao:
            fitness.append(i.getFitness())
        fit_ordenado = cp.copy(fitness)
        fit_ordenado.sort()

        pop_clonar = []
        for i in range(0, 10): # 10 individuos a serem clonados
        	index = fitness.index(fit_ordenado[i])
        	pop_clonar.append(populacao[index])

        melhores_fit.append(fit_ordenado[0])
        melhores_indiv.append(pop_clonar[0])

        clones = gera_clones(pop_clonar)
        clones = muta_clones(clones)
        quant_aleatorio = tamanho_populacao - len(clones)
        pop_inter = popInicial(quant_aleatorio)
        populacao = gera_nova_pop(clones, pop_inter)

        #print len(clones), "tamanho len clones"
        #print sum(num_clones), "somatorio, deveria ser isso"
        # populacao = clones
        # populacao.append(populacao_intermediaria)
        y += 1
        print 'Geracao %d  melhor fitness -> %d' % (y, melhores_fit[-1:][0])

    print melhores_fit
    return melhores_indiv[-1:][0]

if __name__ == '__main__':
    inicio = time.time()
    populacao = popInicial(tamanho_populacao)
    melhorIdividuo = clonalg(populacao)
    fim = time.time()
    print '\nMelhor individuo\n - Fitness:', melhorIdividuo.getFitness(),'\n - Nº locais instalados:', somaLocais(melhorIdividuo), '\n - Viável:', melhorIdividuo.getViavel()
    print '\n\nTempo de execução: %.4f segundos' % (fim - inicio)
