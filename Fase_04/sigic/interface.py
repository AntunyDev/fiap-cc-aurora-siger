"""Interface de terminal do SIGIC."""

import os

from sigic.algoritmos import busca_largura, busca_profundidade, dijkstra
from sigic.dados import MODULOS
from sigic.grafo import GRAFO, montar_matriz_adjacencia
from sigic.simulacao import (
    calcular_indicadores,
    obter_conexoes_criticas,
    simular_envio_energia,
)


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para voltar ao menu...")
    limpar_tela()


def validar_modulo(codigo):
    codigo = codigo.strip().upper()
    if codigo in MODULOS:
        return codigo
    print("Modulo nao encontrado. Use uma das siglas exibidas no sistema.")
    return None


def exibir_cabecalho():
    print("=" * 72)
    print(" SIGIC - AURORA SIGER ".center(72))
    print(" Sistema Inteligente de Gerenciamento da Infraestrutura da Colonia ".center(72))
    print("=" * 72)


def exibir_rede():
    exibir_cabecalho()
    print("\nLISTA DE ADJACENCIA - conexoes ponderadas")

    for codigo, vizinhos in GRAFO.items():
        nome = MODULOS[codigo]["nome"]
        ligacoes = [
            f"{destino} ({distancia:.1f} km, perda {perda:.1f}%)"
            for destino, distancia, perda in vizinhos
        ]
        print(f"{codigo} - {nome}: " + ", ".join(ligacoes))

    print("\nMATRIZ DE ADJACENCIA - pesos por distancia em km")
    codigos, matriz = montar_matriz_adjacencia(GRAFO)
    print("     " + " ".join(f"{c:>5}" for c in codigos))
    for codigo, linha in zip(codigos, matriz):
        valores = " ".join(f"{valor:>5.1f}" for valor in linha)
        print(f"{codigo:>4} {valores}")

    print("\nJustificativa da rede:")
    print("- ENE, CTL e OXI ficam mais centrais por serem sistemas criticos.")
    print("- HAB se conecta diretamente a MED para reduzir tempo de resposta.")
    print("- AGR fica conectada a HAB e OXI por depender de agua, ar e suporte humano.")
    print("- COM tem redundancia com CTL, LAB e OXI para manter comunicacao em falhas.")


def listar_modulos():
    exibir_cabecalho()
    print("\nMODULOS CADASTRADOS")
    for codigo, dados in MODULOS.items():
        print(
            f"{codigo} | {dados['nome']:<26} | Consumo: {dados['consumo']:>3} u/h | "
            f"Prioridade: {dados['prioridade']:>2} | Status: {dados['status']}"
        )


def consultar_modulo():
    listar_modulos()
    codigo = validar_modulo(input("\nDigite a sigla do modulo para consulta: "))
    if not codigo:
        return

    limpar_tela()
    exibir_cabecalho()
    dados = MODULOS[codigo]
    print("\nDETALHES DO MODULO")
    print(f"Nome: {dados['nome']}")
    print(f"Consumo energetico: {dados['consumo']} unidades/hora")
    print(f"Prioridade operacional: {dados['prioridade']} de 10")
    print(f"Capacidade de armazenamento: {dados['armazenamento']} unidades")
    print(f"Necessidade de comunicacao: {dados['comunicacao']}")
    print(f"Status operacional: {dados['status']}")
    print(f"Descricao: {dados['descricao']}")
    print("\nConexoes diretas:")

    for destino, distancia, perda in GRAFO[codigo]:
        print(f"- {MODULOS[destino]['nome']} ({distancia:.1f} km, perda {perda:.1f}%)")


def executar_algoritmos():
    listar_modulos()
    origem = validar_modulo(input("\nOrigem: "))
    if not origem:
        return
    destino = validar_modulo(input("Destino para Dijkstra: "))
    if not destino:
        return

    ordem_bfs = busca_largura(origem)
    ordem_dfs = busca_profundidade(origem)
    caminho_dist, custo_dist = dijkstra(origem, destino, "distancia")
    caminho_perda, custo_perda = dijkstra(origem, destino, "perda")

    limpar_tela()
    exibir_cabecalho()
    print("\nEXPLORACAO DA REDE")
    print("BFS  (largura):      " + " -> ".join(ordem_bfs))
    print("DFS  (profundidade): " + " -> ".join(ordem_dfs))

    print("\nCAMINHOS MINIMOS")
    print(f"Menor distancia: {' -> '.join(caminho_dist)} | total: {custo_dist:.1f} km")
    print(f"Menor perda:     {' -> '.join(caminho_perda)} | total: {custo_perda:.1f}%")


def simular_distribuicao_energia():
    listar_modulos()
    destino = validar_modulo(input("\nModulo que deve receber energia a partir de ENE: "))
    if not destino:
        return

    resultado = simular_envio_energia(destino)

    limpar_tela()
    exibir_cabecalho()
    print("\nSIMULACAO OPERACIONAL - DISTRIBUICAO DE ENERGIA")
    print(f"Origem: {MODULOS[resultado['origem']]['nome']} ({resultado['origem']})")
    print(f"Destino: {MODULOS[resultado['destino']]['nome']} ({resultado['destino']})")
    print(f"Rota otimizada por menor perda: {' -> '.join(resultado['caminho'])}")
    print(f"Distancia acumulada: {resultado['distancia_total']:.1f} km")
    print(f"Perda energetica acumulada: {resultado['perda_total']:.1f}%")
    print(f"Demanda base do destino: {resultado['demanda']:.1f} unidades/hora")
    print(f"Energia estimada necessaria: {resultado['energia_necessaria']:.2f} unidades/hora")
    print(f"Decisao: {resultado['decisao']}")


def detectar_conexoes_criticas():
    exibir_cabecalho()
    print("\nCONEXOES CRITICAS")

    for conexao in obter_conexoes_criticas():
        print(
            f"- {conexao['origem']}-{conexao['destino']}: "
            f"{conexao['distancia']:.1f} km, perda {conexao['perda']:.1f}%, "
            f"impacto {conexao['impacto']}. Motivo: {conexao['motivo']}."
        )

    print("\nRecomendacao:")
    print("Criar rotas redundantes para conexoes criticas e monitorar perdas em tempo real.")


def analisar_eficiencia_operacional():
    exibir_cabecalho()
    indicadores = calcular_indicadores()

    print("\nANALISE DE EFICIENCIA OPERACIONAL")
    print(f"Consumo total: {indicadores['consumo_total']:.1f} unidades/hora")
    print(f"Armazenamento total: {indicadores['armazenamento_total']:.1f} unidades")
    print(f"Modulos ativos: {indicadores['ativos']} de {len(MODULOS)}")
    print(f"Prioridade media da infraestrutura: {indicadores['prioridade_media']:.2f}")
    print(f"Perda media das conexoes: {indicadores['perda_media']:.2f}%")
    print(f"Indice de eficiencia estimado: {indicadores['eficiencia']:.2f}/100")

    print("\nMODELAGEM MATEMATICA")
    print("Formula usada na simulacao: E(d,p) = D * (1 + p/100) + 0.8*d")
    print("D representa a demanda do modulo; p e a perda acumulada; d e a distancia.")
    print("A funcao cresce quando a rota fica maior ou perde mais energia.")
    print("Logo, o SIGIC busca rotas com menor perda e menor distancia para preservar recursos.")


def exibir_esg():
    exibir_cabecalho()
    print("\nSUSTENTABILIDADE E GOVERNANCA")
    print("1. Uso sustentavel de energia:")
    print("   Monitorar perdas por conexao e priorizar rotas com menor desperdicio.")
    print("2. Expansao organizada:")
    print("   Novos modulos devem se conectar primeiro a CTL, ENE ou OXI com redundancia.")
    print("3. Priorizacao de sistemas criticos:")
    print("   Habitacao, Oxigenio, Energia, Controle e Medico recebem prioridade operacional.")
    print("4. Governanca tecnologica:")
    print("   Toda decisao automatica deve registrar criterio: distancia, perda ou prioridade.")
    print("5. Reducao de desperdicios:")
    print("   Desligar cargas nao essenciais em alerta e redistribuir energia pela rota eficiente.")


def exibir_menu():
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
    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu()
        opcao = input("\nEscolha uma opcao: ").strip()
        limpar_tela()

        if opcao == "0":
            print("Encerrando o SIGIC. Operacao finalizada.")
            break
        if opcao == "1":
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

        if opcao != "0":
            pausar()
