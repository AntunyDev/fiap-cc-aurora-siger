"""Funcoes de montagem e analise estrutural do grafo da colonia."""

from collections import deque

from sigic.dados import CONEXOES, MODULOS


def montar_lista_adjacencia():
    grafo = {codigo: [] for codigo in MODULOS}
    for origem, destino, distancia, perda in CONEXOES:
        grafo[origem].append((destino, distancia, perda))
        grafo[destino].append((origem, distancia, perda))
    return grafo


def montar_matriz_adjacencia(grafo):
    codigos = list(MODULOS.keys())
    matriz = [[0 for _ in codigos] for _ in codigos]
    indice_codigos = {codigo: indice for indice, codigo in enumerate(codigos)}

    for origem, vizinhos in grafo.items():
        i = indice_codigos[origem]
        for destino, distancia, _perda in vizinhos:
            j = indice_codigos[destino]
            matriz[i][j] = distancia

    return codigos, matriz


def remover_aresta(grafo, origem, destino):
    copia = {codigo: list(vizinhos) for codigo, vizinhos in grafo.items()}
    copia[origem] = [item for item in copia[origem] if item[0] != destino]
    copia[destino] = [item for item in copia[destino] if item[0] != origem]
    return copia


def contar_componentes(grafo):
    vistos = set()
    componentes = 0

    for origem in grafo:
        if origem in vistos:
            continue
        componentes += 1
        fila = deque([origem])
        vistos.add(origem)

        while fila:
            atual = fila.popleft()
            for vizinho, _distancia, _perda in grafo[atual]:
                if vizinho not in vistos:
                    vistos.add(vizinho)
                    fila.append(vizinho)

    return componentes


GRAFO = montar_lista_adjacencia()
