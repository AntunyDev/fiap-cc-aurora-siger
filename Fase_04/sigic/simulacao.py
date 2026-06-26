"""Modelagem matematica, simulacoes e indicadores operacionais."""

import math  # usado na segunda modelagem (crescimento exponencial)

from sigic.algoritmos import dijkstra
from sigic.dados import CONEXOES, MODULOS
from sigic.grafo import GRAFO, contar_componentes, remover_aresta


# =============================================================================
# MODELAGEM 1 — Energia Necessaria por Rota
# Formula: E(d, p) = D * (1 + p / 100) + 0.8 * d
# =============================================================================

def modelagem_energetica(demanda_total, distancia_total, perda_total):
    """
    Calcula a energia bruta que deve ser injetada em ENE para suprir o destino.

    Formula: E(d, p) = D * (1 + p / 100) + 0.8 * d

    Variaveis:
        D  = demanda energetica base do modulo destino (unidades/hora)
        p  = perda percentual acumulada ao longo da rota (%)
        d  = distancia total percorrida na rota (km)
        E  = energia bruta necessaria a ser fornecida (unidades/hora)

    Analise qualitativa:
    - A funcao cresce monotonicamente com d e p.
    - O termo D*(p/100) compensa a energia perdida em transito.
    - O fator 0.8*d modela a resistencia de percurso (calor dissipado no cabo).
    - Minimizar E equivale a minimizar p e d simultaneamente -> objetivo do Dijkstra.
    """
    # Parcela 1: demanda ajustada pela perda percentual da rota
    compensacao_perda = demanda_total * (1 + perda_total / 100)

    # Parcela 2: resistencia proporcional a distancia percorrida
    resistencia_percurso = 0.8 * distancia_total

    return compensacao_perda + resistencia_percurso


# =============================================================================
# MODELAGEM 2 — Crescimento do Consumo por Expansao da Colonia
# Formula: C(n) = C0 * e^(k * n)
# =============================================================================

def modelagem_crescimento_consumo(n_modulos_adicionais, consumo_base=None, k=0.18):
    """
    Modela o crescimento exponencial do consumo energetico conforme a colonia expande.

    Formula: C(n) = C0 * e^(k * n)

    Variaveis:
        C0 = consumo atual total da colonia (calculado automaticamente se None)
        n  = numero de novos modulos a serem adicionados
        k  = taxa de crescimento por modulo (padrao: 0.18)
        C  = consumo projetado apos adicionar n modulos

    Analise qualitativa:
    - Funcao exponencial: o consumo cresce de forma acelerada com a expansao.
    - A derivada C'(n) = C0 * k * e^(k*n) e sempre positiva e crescente,
      indicando que cada novo modulo eleva o custo marginal de energia.
    - Ponto critico: quando C(n) > armazenamento_total, a rede entra em deficit.
    - Aplicacao: planejar quantos modulos podem ser adicionados sem comprometer
      a sustentabilidade energetica da Aurora Siger.
    """
    # Calcula consumo base atual se nao fornecido
    if consumo_base is None:
        consumo_base = sum(dados["consumo"] for dados in MODULOS.values())

    # Aplica o modelo exponencial: C(n) = C0 * e^(k * n)
    consumo_projetado = consumo_base * math.exp(k * n_modulos_adicionais)

    # Calcula tambem a derivada no ponto n (taxa de crescimento instantanea)
    taxa_marginal = consumo_base * k * math.exp(k * n_modulos_adicionais)

    return {
        "consumo_base": consumo_base,
        "consumo_projetado": consumo_projetado,
        "taxa_marginal": taxa_marginal,       # unidades/hora por modulo adicional
        "variacao_percentual": ((consumo_projetado - consumo_base) / consumo_base) * 100,
    }


# =============================================================================
# Funcoes de suporte e simulacao
# =============================================================================

def calcular_metricas_rota(caminho):
    """
    Percorre o caminho e acumula distancia total e perda total da rota.

    Itera sobre pares consecutivos (origem, destino) do caminho e busca
    os pesos na lista de adjacencia do grafo.
    """
    distancia_total = 0.0
    perda_total = 0.0

    # Percorre pares de nos consecutivos no caminho
    for origem, destino in zip(caminho, caminho[1:]):
        # Busca o vizinho correspondente na lista de adjacencia
        for vizinho, distancia, perda in GRAFO[origem]:
            if vizinho == destino:
                distancia_total += distancia
                perda_total += perda
                break  # encontrou a aresta correta; passa para o proximo par

    return distancia_total, perda_total


def simular_envio_energia(destino):
    """
    Simula o envio de energia do modulo ENE ate o modulo destino.

    Passos:
    1. Calcula a rota otima por menor perda usando Dijkstra.
    2. Acumula distancia e perda da rota escolhida.
    3. Aplica a modelagem energetica (Modelagem 1) para estimar energia necessaria.
    4. Gera uma decisao operacional com base na prioridade e no custo calculado.

    Retorna um dicionario com todos os dados da simulacao para exibicao.
    """
    origem = "ENE"  # hub central de energia — ponto fixo de partida

    # Passo 1: calcula rota otima priorizando menor perda energetica
    caminho, _custo = dijkstra(origem, destino, "perda")

    # Passo 2: acumula metricas fisicas da rota
    distancia_total, perda_total = calcular_metricas_rota(caminho)

    # Passo 3: aplica formula de energia necessaria
    demanda = MODULOS[destino]["consumo"]
    energia_necessaria = modelagem_energetica(demanda, distancia_total, perda_total)

    # Passo 4: decisao operacional baseada em prioridade e custo
    if MODULOS[destino]["prioridade"] >= 9:
        decisao = "Prioridade maxima. Manter fornecimento mesmo em restricao."
    elif energia_necessaria > 55:
        decisao = "Alto custo. Recomenda-se reduzir cargas nao essenciais."
    else:
        decisao = "Fornecimento normal dentro da eficiencia esperada."

    # Retorna dicionario com todos os dados para exibicao no terminal
    return {
        "origem": origem,
        "destino": destino,
        "caminho": caminho,
        "distancia_total": distancia_total,
        "perda_total": perda_total,
        "demanda": demanda,
        "energia_necessaria": energia_necessaria,
        "decisao": decisao,
    }


def obter_conexoes_criticas():
    """
    Identifica conexoes criticas da rede por dois criterios:

    Criterio 1 — Conectividade:
        Remove cada aresta e conta os componentes conexos resultantes.
        Se o numero aumentar, a aresta e uma ponte (sua remocao fragmenta a rede).

    Criterio 2 — Prioridade:
        Conexoes entre dois modulos de alta prioridade (soma >= 18) sao criticas
        mesmo que nao fragmentem a rede, pois afetam servicos essenciais.

    Retorna lista de dicionarios com dados de cada conexao critica encontrada.
    """
    # Numero de componentes do grafo completo (referencia para comparacao)
    base_componentes = contar_componentes(GRAFO)
    criticas = []

    for origem, destino, distancia, perda in CONEXOES:
        # Testa o impacto de remover esta aresta
        grafo_teste = remover_aresta(GRAFO, origem, destino)
        componentes = contar_componentes(grafo_teste)

        # Soma das prioridades dos dois modulos ligados pela aresta
        impacto_prioridade = MODULOS[origem]["prioridade"] + MODULOS[destino]["prioridade"]

        # Criterio 1: aresta ponte (isola parte da rede)
        # Criterio 2: liga dois modulos de alta prioridade (soma >= 18)
        if componentes > base_componentes or impacto_prioridade >= 18:
            motivo = (
                "isola parte da rede"
                if componentes > base_componentes
                else "liga sistemas de alta prioridade"
            )
            criticas.append({
                "origem": origem,
                "destino": destino,
                "distancia": distancia,
                "perda": perda,
                "impacto": impacto_prioridade,
                "motivo": motivo,
            })

    return criticas


def calcular_indicadores():
    """
    Calcula indicadores globais de eficiencia operacional da Aurora Siger.

    Indicadores calculados:
    - consumo_total      : soma do consumo de todos os modulos (u/h)
    - armazenamento_total: soma da capacidade de todos os modulos (u)
    - ativos             : quantidade de modulos com status "ativo"
    - prioridade_media   : media da prioridade operacional dos modulos
    - perda_media        : media das perdas percentuais das conexoes
    - eficiencia         : indice sintetico de 0 a 100 estimando saude da rede
    """
    consumo_total = sum(dados["consumo"] for dados in MODULOS.values())
    armazenamento_total = sum(dados["armazenamento"] for dados in MODULOS.values())
    ativos = sum(1 for dados in MODULOS.values() if dados["status"] == "ativo")
    prioridade_media = sum(dados["prioridade"] for dados in MODULOS.values()) / len(MODULOS)
    perda_media = sum(perda for _o, _d, _dist, perda in CONEXOES) / len(CONEXOES)

    # Indice de eficiencia: penaliza alta perda media e alto ratio consumo/armazenamento
    eficiencia = max(0, 100 - perda_media * 8 - (consumo_total / armazenamento_total) * 10)

    return {
        "consumo_total": consumo_total,
        "armazenamento_total": armazenamento_total,
        "ativos": ativos,
        "prioridade_media": prioridade_media,
        "perda_media": perda_media,
        "eficiencia": eficiencia,
    }
