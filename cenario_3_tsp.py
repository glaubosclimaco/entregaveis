#!/usr/bin/env python3.7

import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB


# -----
# Há várias formulações para o TSP, que variam principalmente em como se evita a formação de subciclos na rota
# Nesta implementação, foi utilizada uma abordagem branch-and-cut, que geralmente resolve o TSP de maneira mais
# rápida, além de possibilitar a resolução de problemas maiores
# -----

# função do tipo callback para a adição de restrições, em tempo de execução, para a eliminação de sub-rotas (ciclos)
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        # encontra o menor ciclo na lista de arestas selecionadas
        tour = subtour(vals)
        if len(tour) < n:
            # adiciona uma restrição de eliminação de subciclo para cada par de cidade na rota
            model.cbLazy(gp.quicksum(model._vars[i, j]
                                     for i, j in combinations(tour, 2))
                         <= len(tour)-1)


# Dada uma tuplelist de arestas, encontra a menor sub-rota

def subtour(vals):
    # make a list of edges selected in the solution
    edges = gp.tuplelist((i, j) for i, j in vals.keys()
                         if vals[i, j] > 0.5)
    unvisited = list(range(n))
    cycle = range(n+1)  # initial length has 1 more city
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle



arq = open('states_coords.txt','r')

points = []
cont=0
for line in arq.readlines():
    split = line.split()
    new_point = (float(split[0]), float(split[1]))
    # print(new_point)
    points.append(new_point)
    cont = cont + 1

n = 26 # nº de cidades


# print('points:\n\n', points)


# dicionario de distancias euclidianas entre cada par de pontos
dist = {(i, j):
        math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
        for i in range(n) for j in range(i)}




# print(dist)

# input()

m = gp.Model()

# criando as variaveis

vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i, j in vars.keys():
    vars[j, i] = vars[i, j]  # aresta na direção oposta


# adicionando a restrição de grau

m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))


# otimizando o modelo

m._vars = vars
m.Params.LazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('X', vars)
tour = subtour(vals)
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.ObjVal)
print('')


# 0 - São Paulo
# 1 - Rio de Janeiro
# 2 - Minas Gerais
# 3 - Rio Grande do Sul
# 4 - Pernambuco
# 5 - Ceará
# 6 - Bahia
# 7 - Paraná
# 8 - Pará
# 9 - Goiás
# 10 - Amazonas
# 11 - Espírito Santo
# 12 - Alagoas
# 13 - Rio Grande do Norte
# 14 - Maranhão
# 15 - Santa Catarina
# 16 - Paraíba
# 17 - Piauí
# 18 - Mato Grosso
# 19 - Mato Grosso do Sul
# 20 - Sergipe
# 21 - Amapá
# 22 - Rondônia
# 23 - Acre
# 24 - Tocantins
# 25 - Roraima
