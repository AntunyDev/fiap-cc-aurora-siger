"""Modelagem matematica, simulacoes e indicadores operacionais."""

from sigic.algoritmos import dijkstra
from sigic.dados import CONEXOES, MODULOS
from sigic.grafo import GRAFO, contar_componentes, remover_aresta


def modelagem_energetica(demanda_total, distancia_total, perda_total):
    """
    Formula: E(d, p) = D * (1 + p / 100) + 0.8 * d

    D = demanda energetica do modulo destino.
    p = perda acumulada da rota em porcentagem.
    d = distancia total da rota em km.
    """
    return demanda_total * (1 + perda_total / 100) + 0.8 * distancia_total


def calcular_metricas_rota(caminho):
    distancia_total = 0
    perda_total = 0

    for origem, destino in zip(caminho, caminho[1:]):
        for vizinho, distancia, perda in GRAFO[origem]:
            if vizinho == destino:
                distancia_total += distancia
                perda_total += perda
                break

    return distancia_total, perda_total


def simular_envio_energia(destino):
    origem = "ENE"
    caminho, _custo = dijkstra(origem, destino, "perda")
    distancia_total, perda_total = calcular_metricas_rota(caminho)
    demanda = MODULOS[destino]["consumo"]
    energia_necessaria = modelagem_energetica(demanda, distancia_total, perda_total)

    if MODULOS[destino]["prioridade"] >= 9:
        decisao = "Prioridade maxima. Manter fornecimento mesmo em restricao."
    elif energia_necessaria > 55:
        decisao = "Alto custo. Recomenda-se reduzir cargas nao essenciais."
    else:
        decisao = "Fornecimento normal dentro da eficiencia esperada."

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
    base_componentes = contar_componentes(GRAFO)
    criticas = []

    for origem, destino, distancia, perda in CONEXOES:
        grafo_teste = remover_aresta(GRAFO, origem, destino)
        componentes = contar_componentes(grafo_teste)
        impacto_prioridade = MODULOS[origem]["prioridade"] + MODULOS[destino]["prioridade"]

        if componentes > base_componentes or impacto_prioridade >= 18:
            motivo = "isola parte da rede" if componentes > base_componentes else "liga sistemas de alta prioridade"
            criticas.append(
                {
                    "origem": origem,
                    "destino": destino,
                    "distancia": distancia,
                    "perda": perda,
                    "impacto": impacto_prioridade,
                    "motivo": motivo,
                }
            )

    return criticas


def calcular_indicadores():
    consumo_total = sum(dados["consumo"] for dados in MODULOS.values())
    armazenamento_total = sum(dados["armazenamento"] for dados in MODULOS.values())
    ativos = sum(1 for dados in MODULOS.values() if dados["status"] == "ativo")
    prioridade_media = sum(dados["prioridade"] for dados in MODULOS.values()) / len(MODULOS)
    perda_media = sum(perda for _o, _d, _dist, perda in CONEXOES) / len(CONEXOES)
    eficiencia = max(0, 100 - perda_media * 8 - (consumo_total / armazenamento_total) * 10)

    return {
        "consumo_total": consumo_total,
        "armazenamento_total": armazenamento_total,
        "ativos": ativos,
        "prioridade_media": prioridade_media,
        "perda_media": perda_media,
        "eficiencia": eficiencia,
    }
