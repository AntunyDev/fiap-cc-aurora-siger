"""Funcoes de montagem e analise estrutural do grafo da colonia."""

from collections import deque  # deque: fila eficiente O(1) para BFS

from sigic.dados import CONEXOES, MODULOS


def montar_lista_adjacencia():
    """
    Constroi a lista de adjacencia do grafo nao-dirigido da colonia.

    Estrutura resultante (dicionario de listas):
        { "ENE": [("CTL", 2.0, 3.0), ("HAB", 2.5, 4.0), ...], ... }

    Escolha da estrutura:
    - Dicionario: acesso O(1) por sigla do modulo.
    - Lista de tuplas: vizinhos em ordem de insercao; cada tupla guarda
      (destino, distancia_km, perda_%) de forma imutavel e legivel.
    """
    # Inicializa cada modulo com lista vazia de vizinhos
    grafo = {codigo: [] for codigo in MODULOS}

    # Percorre todas as conexoes e popula o grafo nos dois sentidos (nao-dirigido)
    for origem, destino, distancia, perda in CONEXOES:
        grafo[origem].append((destino, distancia, perda))   # sentido direto
        grafo[destino].append((origem, distancia, perda))   # sentido inverso

    return grafo


def montar_matriz_adjacencia(grafo):
    """
    Gera a matriz de adjacencia quadrada N×N do grafo (N = numero de modulos).

    Cada celula matriz[i][j] contem a distancia em km entre os modulos i e j,
    ou 0 se nao houver conexao direta.

    Estrutura: lista de listas (matriz bidimensional) — permite indexacao
    por posicao e visualizacao tabular no terminal.
    """
    codigos = list(MODULOS.keys())              # lista ordenada das siglas
    n = len(codigos)
    matriz = [[0] * n for _ in range(n)]       # inicializa NxN com zeros
    indice_codigos = {codigo: indice for indice, codigo in enumerate(codigos)}

    # Preenche as celulas com a distancia entre modulos conectados
    for origem, vizinhos in grafo.items():
        i = indice_codigos[origem]
        for destino, distancia, _perda in vizinhos:
            j = indice_codigos[destino]
            matriz[i][j] = distancia           # peso = distancia em km

    return codigos, matriz


def remover_aresta(grafo, origem, destino):
    """
    Retorna uma copia do grafo sem a aresta (origem <-> destino).

    Usado na deteccao de conexoes criticas: remove uma aresta por vez
    e verifica se o numero de componentes conexos aumenta (indicando
    que aquela aresta era uma ponte da rede).

    Nao modifica o grafo original — trabalha sobre uma copia rasa.
    """
    # Copia superficial: preserva o grafo original intacto
    copia = {codigo: list(vizinhos) for codigo, vizinhos in grafo.items()}

    # Remove nos dois sentidos (grafo nao-dirigido)
    copia[origem] = [item for item in copia[origem] if item[0] != destino]
    copia[destino] = [item for item in copia[destino] if item[0] != origem]

    return copia


def contar_componentes(grafo):
    """
    Conta quantos componentes conexos existem no grafo usando BFS.

    Um componente conexo e um subconjunto de vertices onde todos os nos
    sao alcancaveis entre si. Se o grafo for totalmente conectado, retorna 1.
    Se uma aresta critica for removida e isolar um modulo, retorna 2 ou mais.
    """
    vistos = set()       # conjunto de modulos ja visitados
    componentes = 0      # contador de componentes conexos encontrados

    for origem in grafo:
        if origem in vistos:
            continue     # modulo ja pertence a um componente encontrado

        # Inicia novo componente: explora todos os alcancaveis a partir de 'origem'
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


# Instancia global do grafo — criada uma vez ao importar o modulo
GRAFO = montar_lista_adjacencia()
