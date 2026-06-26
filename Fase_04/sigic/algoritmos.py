"""Algoritmos de rede usados pelo SIGIC."""

from collections import deque   # deque: fila com pop na esquerda em O(1)
from heapq import heappop, heappush  # heap minimo para Dijkstra eficiente

from sigic.dados import MODULOS
from sigic.grafo import GRAFO


# =============================================================================
# BFS — Busca em Largura (Breadth-First Search)
# =============================================================================

def busca_largura(origem):
    """
    Explora a rede nivel a nivel a partir do modulo de origem.

    Logica:
    - Usa uma fila (FIFO) para garantir que os vizinhos diretos sejam
      visitados antes dos vizinhos de vizinhos.
    - Resultado: lista com todos os modulos na ordem de descoberta.

    Aplicacao na Aurora Siger:
    - Verificar quais modulos sao alcancaveis a partir de um ponto.
    - Medir a "camada de cobertura" da rede.
    """
    visitados = []              # lista com a ordem de visita (retorno da funcao)
    fila = deque([origem])      # fila FIFO inicializada com o no de origem
    vistos = {origem}           # conjunto de nos ja adicionados a fila (evita repeticao)

    while fila:
        atual = fila.popleft()          # retira o primeiro elemento da fila
        visitados.append(atual)         # registra a visita

        # Adiciona vizinhos nao visitados ao final da fila
        for vizinho, _distancia, _perda in GRAFO[atual]:
            if vizinho not in vistos:
                vistos.add(vizinho)
                fila.append(vizinho)

    return visitados


# =============================================================================
# DFS — Busca em Profundidade (Depth-First Search)
# =============================================================================

def busca_profundidade(origem):
    """
    Explora a rede seguindo cada ramificacao ate o fim antes de retroceder.

    Logica:
    - Implementada de forma recursiva: visita o no atual, depois chama
      a si mesma para cada vizinho nao visitado.
    - Resultado: lista com todos os modulos na ordem de descoberta.

    Aplicacao na Aurora Siger:
    - Detectar componentes conexos (usado em contar_componentes).
    - Explorar caminhos alternativos em situacoes de falha.
    """
    visitados = []   # ordem de visita (retorno da funcao)
    vistos = set()   # conjunto de nos ja visitados (evita ciclos)

    def visitar(atual):
        """Funcao interna recursiva: visita 'atual' e seus descendentes."""
        vistos.add(atual)           # marca o no como visitado
        visitados.append(atual)     # registra a ordem de visita

        # Para cada vizinho ainda nao visitado, aprofunda a busca
        for vizinho, _distancia, _perda in GRAFO[atual]:
            if vizinho not in vistos:
                visitar(vizinho)    # chamada recursiva (stack de chamadas = "pilha" do DFS)

    visitar(origem)  # inicia a busca a partir do no de origem
    return visitados


# =============================================================================
# Dijkstra — Caminho de Custo Minimo
# =============================================================================

def dijkstra(origem, destino, criterio="distancia"):
    """
    Encontra o caminho de menor custo entre dois modulos.

    Parametros:
    - origem   : sigla do modulo de partida.
    - destino  : sigla do modulo alvo.
    - criterio : "distancia" (km) ou "perda" (%) — define o peso usado.

    Logica:
    - Usa um heap minimo (fila de prioridade) para sempre expandir o no
      com menor custo acumulado primeiro.
    - Mantem um vetor de distancias (custo minimo ate cada no) e um vetor
      de anteriores (para reconstruir o caminho ao final).
    - Complexidade: O((V + E) * log V), onde V = vertices e E = arestas.

    Aplicacao na Aurora Siger:
    - criterio "distancia": rota com menos km percorridos.
    - criterio "perda"    : rota com menor desperdicio energetico.
    """
    # Inicializa todos os custos como infinito (nenhum no foi alcancado ainda)
    distancias = {codigo: float("inf") for codigo in MODULOS}
    # Guarda o no anterior no caminho otimo (para reconstruir a rota)
    anteriores = {codigo: None for codigo in MODULOS}

    distancias[origem] = 0              # custo para chegar na origem e zero
    fila = [(0, origem)]               # heap: (custo_acumulado, no)

    while fila:
        custo_atual, atual = heappop(fila)   # extrai o no de menor custo

        # Interrupcao antecipada: ja chegamos ao destino
        if atual == destino:
            break

        # Ignora entradas desatualizadas no heap (lazy deletion)
        if custo_atual > distancias[atual]:
            continue

        # Relaxamento das arestas: tenta melhorar o custo dos vizinhos
        for vizinho, distancia, perda in GRAFO[atual]:
            # Seleciona o peso conforme o criterio escolhido
            peso = distancia if criterio == "distancia" else perda

            novo_custo = custo_atual + peso
            # Atualiza apenas se encontrou um caminho mais barato
            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                anteriores[vizinho] = atual          # registra de onde viemos
                heappush(fila, (novo_custo, vizinho))

    # Reconstroi a rota seguindo os ponteiros de 'anteriores' de tras pra frente
    caminho = reconstruir_caminho(anteriores, origem, destino)
    return caminho, distancias[destino]


def reconstruir_caminho(anteriores, origem, destino):
    """
    Reconstroi o caminho otimo percorrendo o vetor 'anteriores' de tras para frente.

    Comeca pelo destino e segue os ponteiros ate chegar na origem,
    depois inverte a lista para obter a ordem correta de travessia.
    Retorna lista vazia se nao existe caminho valido (grafo desconexo).
    """
    caminho = []
    atual = destino

    # Percorre os nos anteriores ate chegar na origem (anterior = None)
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()  # inverte para obter a ordem origem -> destino

    # Valida: se o primeiro elemento nao e a origem, o destino e inalcancavel
    if caminho and caminho[0] == origem:
        return caminho
    return []
