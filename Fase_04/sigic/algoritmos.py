"""Algoritmos de rede usados pelo SIGIC."""

from collections import deque
from heapq import heappop, heappush

from sigic.dados import MODULOS
from sigic.grafo import GRAFO


def busca_largura(origem):
    visitados = []
    fila = deque([origem])
    vistos = {origem}

    while fila:
        atual = fila.popleft()
        visitados.append(atual)
        for vizinho, _distancia, _perda in GRAFO[atual]:
            if vizinho not in vistos:
                vistos.add(vizinho)
                fila.append(vizinho)

    return visitados


def busca_profundidade(origem):
    visitados = []
    vistos = set()

    def visitar(atual):
        vistos.add(atual)
        visitados.append(atual)
        for vizinho, _distancia, _perda in GRAFO[atual]:
            if vizinho not in vistos:
                visitar(vizinho)

    visitar(origem)
    return visitados


def dijkstra(origem, destino, criterio="distancia"):
    distancias = {codigo: float("inf") for codigo in MODULOS}
    anteriores = {codigo: None for codigo in MODULOS}
    distancias[origem] = 0
    fila = [(0, origem)]

    while fila:
        custo_atual, atual = heappop(fila)
        if atual == destino:
            break
        if custo_atual > distancias[atual]:
            continue

        for vizinho, distancia, perda in GRAFO[atual]:
            peso = distancia if criterio == "distancia" else perda
            novo_custo = custo_atual + peso
            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                anteriores[vizinho] = atual
                heappush(fila, (novo_custo, vizinho))

    caminho = reconstruir_caminho(anteriores, origem, destino)
    return caminho, distancias[destino]


def reconstruir_caminho(anteriores, origem, destino):
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()
    if caminho and caminho[0] == origem:
        return caminho
    return []
