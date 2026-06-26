"""Interface de terminal do SIGIC — Aurora Siger."""

import os

from sigic.algoritmos import busca_largura, busca_profundidade, dijkstra
from sigic.dados import MODULOS
from sigic.grafo import GRAFO, montar_matriz_adjacencia
from sigic.simulacao import (
    calcular_indicadores,
    modelagem_crescimento_consumo,
    obter_conexoes_criticas,
    simular_envio_energia,
)


# =============================================================================
# Utilitarios de terminal
# =============================================================================

def limpar_tela():
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Aguarda Enter do usuario antes de voltar ao menu principal."""
    input("\nPressione Enter para voltar ao menu...")
    limpar_tela()


def validar_modulo(codigo):
    """
    Valida se a sigla digitada corresponde a um modulo existente.
    Retorna a sigla em maiusculas ou None em caso de erro.
    """
    codigo = codigo.strip().upper()
    if codigo in MODULOS:
        return codigo
    print("Modulo nao encontrado. Use uma das siglas exibidas no sistema.")
    return None


# =============================================================================
# Cabecalho
# =============================================================================

def exibir_cabecalho():
    """Exibe o cabecalho padrao do sistema."""
    print("=" * 72)
    print(" SIGIC - AURORA SIGER ".center(72))
    print(" Sistema Inteligente de Gerenciamento da Infraestrutura da Colonia ".center(72))
    print("=" * 72)


# =============================================================================
# Opcao 1 — Visualizar rede
# =============================================================================

def exibir_rede():
    """
    Exibe a representacao computacional da rede da colonia:
    - Lista de adjacencia: vizinhos de cada modulo com distancia e perda.
    - Matriz de adjacencia: pesos por distancia em formato tabular.
    - Justificativa da topologia escolhida.
    """
    exibir_cabecalho()
    print("\nLISTA DE ADJACENCIA - conexoes ponderadas")

    # Percorre cada modulo e lista seus vizinhos diretos com os pesos das arestas
    for codigo, vizinhos in GRAFO.items():
        nome = MODULOS[codigo]["nome"]
        ligacoes = [
            f"{destino} ({distancia:.1f} km, perda {perda:.1f}%)"
            for destino, distancia, perda in vizinhos
        ]
        print(f"{codigo} - {nome}: " + ", ".join(ligacoes))

    print("\nMATRIZ DE ADJACENCIA - pesos por distancia em km")
    codigos, matriz = montar_matriz_adjacencia(GRAFO)

    # Cabecalho da matriz com as siglas dos modulos
    print("     " + " ".join(f"{c:>5}" for c in codigos))

    # Linhas da matriz: cada linha representa as distancias saindo daquele modulo
    for codigo, linha in zip(codigos, matriz):
        valores = " ".join(f"{valor:>5.1f}" for valor in linha)
        print(f"{codigo:>4} {valores}")

    # Justificativa das escolhas de topologia da rede
    print("\nJustificativa da rede:")
    print("- ENE, CTL e OXI ficam mais centrais por serem sistemas criticos.")
    print("- HAB se conecta diretamente a MED para reduzir tempo de resposta.")
    print("- AGR fica conectada a HAB e OXI por depender de agua, ar e suporte humano.")
    print("- COM tem redundancia com CTL, LAB e OXI para manter comunicacao em falhas.")


# =============================================================================
# Opcao 2 — Listar modulos
# =============================================================================

def listar_modulos():
    """Exibe tabela resumida com todos os modulos cadastrados no sistema."""
    exibir_cabecalho()
    print("\nMODULOS CADASTRADOS")

    # Exibe cada modulo com suas principais informacoes em formato de tabela
    for codigo, dados in MODULOS.items():
        print(
            f"{codigo} | {dados['nome']:<26} | Consumo: {dados['consumo']:>3} u/h | "
            f"Prioridade: {dados['prioridade']:>2} | Status: {dados['status']}"
        )


# =============================================================================
# Opcao 3 — Consultar modulo especifico
# =============================================================================

def consultar_modulo():
    """
    Permite ao usuario escolher um modulo e exibe todos os seus atributos
    detalhados, incluindo conexoes diretas com distancia e perda.
    """
    listar_modulos()
    codigo = validar_modulo(input("\nDigite a sigla do modulo para consulta: "))
    if not codigo:
        return

    limpar_tela()
    exibir_cabecalho()
    dados = MODULOS[codigo]

    print("\nDETALHES DO MODULO")
    print(f"Nome:                     {dados['nome']}")
    print(f"Consumo energetico:        {dados['consumo']} unidades/hora")
    print(f"Prioridade operacional:    {dados['prioridade']} de 10")
    print(f"Capacidade de armazenamento: {dados['armazenamento']} unidades")
    print(f"Necessidade de comunicacao: {dados['comunicacao']}")
    print(f"Status operacional:        {dados['status']}")
    print(f"Descricao:                 {dados['descricao']}")

    # Lista os vizinhos diretos do modulo no grafo
    print("\nConexoes diretas:")
    for destino, distancia, perda in GRAFO[codigo]:
        print(f"  -> {MODULOS[destino]['nome']:<26} | {distancia:.1f} km | perda {perda:.1f}%")


# =============================================================================
# Opcao 4 — Executar BFS, DFS e Dijkstra
# =============================================================================

def executar_algoritmos():
    """
    Executa os tres algoritmos de rede sobre a infraestrutura da colonia:
    - BFS: ordem de exploracao nivel a nivel.
    - DFS: ordem de exploracao em profundidade.
    - Dijkstra (x2): menor distancia e menor perda entre dois modulos.
    """
    listar_modulos()
    origem = validar_modulo(input("\nOrigem: "))
    if not origem:
        return
    destino = validar_modulo(input("Destino para Dijkstra: "))
    if not destino:
        return

    # Executa os tres algoritmos
    ordem_bfs = busca_largura(origem)
    ordem_dfs = busca_profundidade(origem)
    caminho_dist, custo_dist = dijkstra(origem, destino, "distancia")
    caminho_perda, custo_perda = dijkstra(origem, destino, "perda")

    limpar_tela()
    exibir_cabecalho()

    # --- Resultado BFS e DFS ---
    print("\nEXPLORACAO DA REDE")
    print("BFS  (largura):      " + " -> ".join(ordem_bfs))
    print("DFS  (profundidade): " + " -> ".join(ordem_dfs))

    # --- Resultado Dijkstra ---
    print("\nCAMINHOS MINIMOS")
    print(f"Menor distancia: {' -> '.join(caminho_dist)} | total: {custo_dist:.1f} km")
    print(f"Menor perda:     {' -> '.join(caminho_perda)} | total: {custo_perda:.1f}%")


# =============================================================================
# Opcao 5 — Simular distribuicao de energia
# =============================================================================

def simular_distribuicao_energia():
    """
    Simula o envio de energia a partir do modulo ENE ate um modulo escolhido.
    Exibe a rota otima (menor perda), metricas fisicas e decisao operacional.
    Esta e a demonstracao pratica da integracao entre Dijkstra e a modelagem matematica.
    """
    listar_modulos()
    destino = validar_modulo(input("\nModulo que deve receber energia a partir de ENE: "))
    if not destino:
        return

    # Executa a simulacao completa (Dijkstra + modelagem energetica)
    resultado = simular_envio_energia(destino)

    limpar_tela()
    exibir_cabecalho()
    print("\nSIMULACAO OPERACIONAL - DISTRIBUICAO DE ENERGIA")
    print(f"Origem:                    {MODULOS[resultado['origem']]['nome']} ({resultado['origem']})")
    print(f"Destino:                   {MODULOS[resultado['destino']]['nome']} ({resultado['destino']})")
    print(f"Rota otimizada (min perda): {' -> '.join(resultado['caminho'])}")
    print(f"Distancia acumulada:       {resultado['distancia_total']:.1f} km")
    print(f"Perda energetica acumulada: {resultado['perda_total']:.1f}%")
    print(f"Demanda base do destino:   {resultado['demanda']:.1f} unidades/hora")
    print(f"Energia estimada necessaria: {resultado['energia_necessaria']:.2f} unidades/hora")
    print(f"Decisao operacional:       {resultado['decisao']}")


# =============================================================================
# Opcao 6 — Detectar conexoes criticas
# =============================================================================

def detectar_conexoes_criticas():
    """
    Identifica arestas criticas da rede usando dois criterios:
    1. Conectividade: aresta cuja remocao fragmenta a rede (ponte).
    2. Prioridade: aresta que liga dois modulos de missao critica.
    """
    exibir_cabecalho()
    print("\nCONEXOES CRITICAS")

    # Exibe cada conexao critica com seus dados e o motivo da classificacao
    for conexao in obter_conexoes_criticas():
        print(
            f"  [{conexao['origem']}-{conexao['destino']}] "
            f"{conexao['distancia']:.1f} km | perda {conexao['perda']:.1f}% | "
            f"impacto {conexao['impacto']} | Motivo: {conexao['motivo']}."
        )

    print("\nRecomendacao:")
    print("Criar rotas redundantes para conexoes criticas e monitorar perdas em tempo real.")


# =============================================================================
# Opcao 7 — Analisar eficiencia e modelagem matematica
# =============================================================================

def analisar_eficiencia_operacional():
    """
    Exibe os indicadores globais da rede e apresenta as duas modelagens matematicas:

    Modelagem 1 — Energia por Rota:   E(d,p) = D * (1 + p/100) + 0.8*d
    Modelagem 2 — Crescimento do Consumo: C(n) = C0 * e^(k * n)
    """
    exibir_cabecalho()
    indicadores = calcular_indicadores()

    # --- Indicadores operacionais ---
    print("\nANALISE DE EFICIENCIA OPERACIONAL")
    print(f"Consumo total:              {indicadores['consumo_total']:.1f} unidades/hora")
    print(f"Armazenamento total:        {indicadores['armazenamento_total']:.1f} unidades")
    print(f"Modulos ativos:             {indicadores['ativos']} de {len(MODULOS)}")
    print(f"Prioridade media:           {indicadores['prioridade_media']:.2f}")
    print(f"Perda media das conexoes:   {indicadores['perda_media']:.2f}%")
    print(f"Indice de eficiencia:       {indicadores['eficiencia']:.2f} / 100")

    # --- Modelagem 1 ---
    print("\nMODELAGEM 1 - Energia Necessaria por Rota")
    print("  Formula:    E(d, p) = D * (1 + p/100) + 0.8 * d")
    print("  Variaveis:  D = demanda do modulo destino")
    print("              p = perda acumulada da rota (%)")
    print("              d = distancia total da rota (km)")
    print("  Qualitativo: funcao cresce com d e p; Dijkstra minimiza ambos,")
    print("  reduzindo a energia bruta necessaria e preservando reservas de ENE.")

    # --- Modelagem 2 ---
    print("\nMODELAGEM 2 - Crescimento do Consumo por Expansao")
    print("  Formula:    C(n) = C0 * e^(k * n)   |   k = 0.18 por modulo")
    print("  Variaveis:  C0 = consumo atual da colonia; n = novos modulos; k = taxa")

    # Simula a projecao para 1, 3 e 5 novos modulos
    print("\n  Projecao de consumo por expansao:")
    for n in [1, 3, 5]:
        proj = modelagem_crescimento_consumo(n)
        print(
            f"    +{n} modulo(s): consumo projetado = {proj['consumo_projetado']:.1f} u/h | "
            f"variacao = +{proj['variacao_percentual']:.1f}% | "
            f"taxa marginal = {proj['taxa_marginal']:.2f} u/h por modulo"
        )

    print("\n  Qualitativo: a derivada C'(n) = C0 * k * e^(k*n) e sempre crescente,")
    print("  indicando que cada modulo adicional eleva o custo marginal de energia.")
    print("  Ponto critico: quando C(n) supera a capacidade de ENE (220 u), ha deficit.")


# =============================================================================
# Opcao 8 — Sustentabilidade e Governanca ESG
# =============================================================================

def exibir_esg():
    """
    Apresenta a analise de sustentabilidade e governanca ESG da Aurora Siger,
    cobrindo os cinco pilares definidos no planejamento da colonia.
    """
    exibir_cabecalho()
    print("\nSUSTENTABILIDADE E GOVERNANCA (ESG)")

    print("\n1. Uso sustentavel de energia:")
    print("   Monitorar perdas por conexao e priorizar rotas com menor desperdicio.")
    print("   O Dijkstra por perda minima e o mecanismo central desta estrategia.")

    print("\n2. Expansao organizada da colonia:")
    print("   Novos modulos devem se conectar primeiro a CTL, ENE ou OXI com redundancia.")
    print("   A Modelagem 2 projeta o crescimento do consumo antes de qualquer expansao.")

    print("\n3. Priorizacao de sistemas criticos:")
    print("   HAB, OXI, ENE, CTL e MED recebem prioridade maxima (9-10).")
    print("   O sistema garante fornecimento a esses modulos mesmo em restricao energetica.")

    print("\n4. Governanca tecnologica:")
    print("   Toda decisao automatica registra o criterio: distancia, perda ou prioridade.")
    print("   Auditabilidade e transparencia sao principios do SIGIC.")

    print("\n5. Reducao de desperdicios:")
    print("   Desligar cargas nao essenciais em modo alerta (LAB durante manutencao).")
    print("   Redistribuir energia pela rota de menor perda reduz consumo bruto.")


# =============================================================================
# Menu principal
# =============================================================================

def exibir_menu():
    """Exibe as opcoes do menu principal do SIGIC."""
    print("\n1. Visualizar rede da colonia")
    print("2. Listar modulos")
    print("3. Consultar modulo")
    print("4. Executar BFS, DFS e Dijkstra")
    print("5. Simular distribuicao de energia")
    print("6. Detectar conexoes criticas")
    print("7. Analisar eficiencia e modelagem matematica")
    print("8. Sustentabilidade e governanca ESG")
    print("0. Sair")


def menu_principal():
    """
    Loop principal do sistema.
    Exibe o menu, le a opcao do usuario e despacha para a funcao correspondente.
    """
    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu()

        opcao = input("\nEscolha uma opcao: ").strip()
        limpar_tela()

        # Tabela de despacho: mapeia opcao -> funcao
        if opcao == "0":
            print("Encerrando o SIGIC. Operacao finalizada.")
            break
        elif opcao == "1":
            exibir_rede()
        elif opcao == "2":
            listar_modulos()
        elif opcao == "3":
            consultar_modulo()
        elif opcao == "4":
            executar_algoritmos()
        elif opcao == "5":
            simular_distribuicao_energia()
        elif opcao == "6":
            detectar_conexoes_criticas()
        elif opcao == "7":
            analisar_eficiencia_operacional()
        elif opcao == "8":
            exibir_esg()
        else:
            print("Opcao invalida. Tente novamente.")

        # Pausa para leitura antes de voltar ao menu (exceto ao sair)
        if opcao != "0":
            pausar()
