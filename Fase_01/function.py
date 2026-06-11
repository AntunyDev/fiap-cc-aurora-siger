import csv
import data as d
import google.generativeai as genai
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

genai.configure(api_key="AIzaSyDzwEm4p8Z4Vssp03R0HBOV-X6cfbxBc9M")


def limpar_terminal():
    import subprocess
    import platform

    sistema = platform.system()
    if sistema == "Windows":
        subprocess.run("cls", shell=True)  # Windows
    else:
        subprocess.run("clear", shell=True)  # Linux e Mac


def validar_entrada(prompt, min_val, max_val):
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Valor deve estar entre {min_val} e {max_val}.")
        except ValueError:
            print("Valor inválido. Digite um número.")


def calcular_analise_energetica(telemetria):
    energia = telemetria["energia"]
    nivel = energia["nivel"]
    capacidade_total = energia["capacidade_total_kwh"]
    consumo_decolagem = energia["consumo_decolagem_kwh"]
    perdas_energeticas = energia["perdas_energeticas"]

    energia_disponivel = capacidade_total * (nivel / 100)
    energia_util = energia_disponivel * (1 - perdas_energeticas / 100)
    margem = energia_util - consumo_decolagem

    return (
        capacidade_total,
        nivel,
        energia_disponivel,
        perdas_energeticas,
        energia_util,
        consumo_decolagem,
        margem,
    )


def mostrar_hub_pre_decolagem():
    print("\n======== HUB - Pré-Decolagem ============\n")
    print("[1] Visualizar dados Telemetria")
    print("[2] Atualizar dados Telemetria manualmente")
    print("[3] Executar Análise energética")
    print("[4] Executar verificação de segurança")
    print("[5] Gerar relatório de pré-decolagem em csv")
    print("[6] Consultar análise por IA")
    print("[0] Sair")

    op = input("\nEscolha uma opção: ")
    return op


def visualizar_dados_telemetria(telemetria):
    print("\n======== DADOS DE TELEMETRIA ============\n")

    # Dicionário de unidades para melhor exibição
    unidades = {
        "temperatura_interna": "°C",
        "temperatura_externa": "°C",
        "integridade_estrutural": "(0/1)",
        "nivel_energia": "%",
        "pressao_tanques": "kPa",
        "status_modulos_criticos": "(0/1)",
        "nivel": "%",
        "capacidade_total_kwh": "kWh",
        "consumo_decolagem_kwh": "kWh",
        "perdas_energeticas": "%",
    }

    table_data = []
    for chave, valor in telemetria.items():
        if isinstance(valor, dict):
            for sub_chave, sub_valor in valor.items():
                unidade = unidades.get(sub_chave, "")
                table_data.append(
                    [sub_chave.replace("_", " ").title(), f"{sub_valor} {unidade}"]
                )
        else:
            unidade = unidades.get(chave, "")
            table_data.append([chave.replace("_", " ").title(), f"{valor} {unidade}"])

    print(tabulate(table_data, headers=["Parâmetro", "Valor"], tablefmt="grid"))
    print("\n----------------------------\n")
    input("Pressione Enter para continuar...")


def atualizar_dados_telemetria_manual(telemetria):

    campos = [
        {
            "key": "temperatura_interna",
            "label": "Temperatura Interna",
            "unit": "°C",
            "min": 0,
            "max": 100,
        },
        {
            "key": "temperatura_externa",
            "label": "Temperatura Externa",
            "unit": "°C",
            "min": 0,
            "max": 150,
        },
        {
            "key": "integridade_estrutural",
            "label": "Integridade Estrutural",
            "unit": "(0-1)",
            "min": 0,
            "max": 1,
            "cast": int,
        },
        {
            "key": "nivel_energia",
            "label": "Nível de Energia",
            "unit": "%",
            "min": 0,
            "max": 100,
        },
        {
            "key": "pressao_tanques",
            "label": "Pressão dos Tanques",
            "unit": "kPa",
            "min": 0,
            "max": 10000,
        },
        {
            "key": "status_modulos_criticos",
            "label": "Status dos Módulos Críticos",
            "unit": "(0-1)",
            "min": 0,
            "max": 1,
            "cast": int,
        },
    ]

    def mostrar_menu():
        print("\n======== ATUALIZAR DADOS DE TELEMETRIA MANUALMENTE ============\n")
        for idx, campo in enumerate(campos, start=1):
            valor_atual = telemetria.get(campo["key"], "N/A")
            print(f"[{idx}] - {campo['label']} (atual: {valor_atual} {campo['unit']})")
        print(f"[{len(campos) + 1}] - Atualizar todos os dados")
        print("[0] - Voltar")

    while True:
        limpar_terminal()
        mostrar_menu()
        opcao = input("\nEscolha o dado que deseja atualizar: ")

        if opcao == "0":
            return

        if opcao == str(len(campos) + 1):
            escolhas = range(1, len(campos) + 1)
        elif opcao.isdigit() and 1 <= int(opcao) <= len(campos):
            escolhas = [int(opcao)]
        else:
            print("Opção inválida. Selecione um número válido do menu.")
            input("\nPressione Enter para continuar...")
            continue

        for escolha in escolhas:
            campo = campos[escolha - 1]
            try:
                valor = validar_entrada(
                    f"Digite o novo valor para {campo['label']} ({campo['unit']}): ",
                    campo["min"],
                    campo["max"],
                )
                if "cast" in campo:
                    valor = campo["cast"](valor)

                telemetria[campo["key"]] = valor
                print(
                    f"{campo['label']} atualizado para {valor} {campo['unit']} com sucesso."
                )
            except ValueError:
                print(
                    "Valor inválido. Por favor, insira um número dentro do intervalo permitido."
                )

        input("\nPressione Enter para continuar...")


def executar_analise_energetica(telemetria):

    print("\n======== ANÁLISE ENERGÉTICA ============\n")

    (
        capacidade_total,
        nivel,
        energia_disponivel,
        perdas_energeticas,
        energia_util,
        consumo_decolagem,
        margem,
    ) = calcular_analise_energetica(telemetria)

    print(f"Capacidade total da bateria: {capacidade_total} kWh")
    print(f"Carga atual: {nivel}%")
    print(f"Energia disponível: {energia_disponivel:.2f} kWh")
    print(f"Perdas energéticas estimadas: {perdas_energeticas}%")
    print(f"Energia útil após perdas: {energia_util:.2f} kWh")
    print(f"Consumo estimado na decolagem: {consumo_decolagem} kWh")
    print(f"Margem energética: {margem:.2f} kWh\n")

    if margem >= 0:
        if margem < 10:
            print(
                Fore.YELLOW
                + "Status: Energia suficiente, mas margem crítica. Recomenda-se recarga."
                + Style.RESET_ALL
            )
        else:
            print(
                Fore.GREEN
                + "Status: Energia suficiente para a decolagem."
                + Style.RESET_ALL
            )
    else:
        print(
            Fore.RED
            + "Status: Energia insuficiente para a decolagem. Recarregar ou reduzir consumo."
            + Style.RESET_ALL
        )
    print("\n----------------------------\n")
    input("Pressione Enter para continuar...")


def executar_verificacao_seguranca(telemetria):
    print("\n======== VERIFICAÇÃO DE SEGURANÇA ============\n")

    seguro = True

    # Temperatura interna
    if telemetria["temperatura_interna"] > 40:
        print(Fore.RED + "Temperatura interna elevada." + Style.RESET_ALL)
        seguro = False
    else:
        print(Fore.GREEN + "Temperatura interna dentro do limite." + Style.RESET_ALL)

    # Temperatura externa
    if telemetria["temperatura_externa"] > 90:
        print(Fore.RED + "Temperatura externa muito alta." + Style.RESET_ALL)
        seguro = False
    else:
        print(Fore.GREEN + "Temperatura externa dentro do limite." + Style.RESET_ALL)

    # Integridade estrutural
    if telemetria["integridade_estrutural"] != 1:
        print(Fore.RED + "Problema na integridade estrutural." + Style.RESET_ALL)
        seguro = False
    else:
        print(Fore.GREEN + "Estrutura íntegra." + Style.RESET_ALL)

    # Pressão dos tanques
    if telemetria["pressao_tanques"] < 4000:
        print(Fore.RED + "Pressão dos tanques abaixo do ideal." + Style.RESET_ALL)
        seguro = False
    else:
        print(Fore.GREEN + "Pressão dos tanques adequada." + Style.RESET_ALL)

    # Módulos críticos
    if telemetria["status_modulos_criticos"] != 1:
        print(Fore.RED + "Falha em módulos críticos." + Style.RESET_ALL)
        seguro = False
    else:
        print(Fore.GREEN + "Módulos críticos operacionais." + Style.RESET_ALL)

    print("\n---------------------------------------------\n")

    if seguro:
        print(Fore.GREEN + "STATUS FINAL: PRONTO PARA DECOLAR" + Style.RESET_ALL)
    else:
        print(Fore.RED + "STATUS FINAL: DECOLAGEM ABORTADA" + Style.RESET_ALL)

    print("\n---------------------------------------------\n")
    input("Pressione Enter para continuar...")


def gerar_relatorio_csv(telemetria):

    print("\nGerando relatório de telemetria...\n")

    with open("relatorio_telemetria.csv", "w", newline="") as arquivo:

        writer = csv.writer(arquivo)

        writer.writerow(["Parametro", "Valor"])

        for chave, valor in telemetria.items():

            if isinstance(valor, dict):

                for sub_chave, sub_valor in valor.items():
                    writer.writerow([sub_chave, sub_valor])

            else:
                writer.writerow([chave, valor])

    print("Relatório CSV gerado com sucesso: relatorio_telemetria.csv")
    input("Pressione Enter para continuar...")


def consultar_analise_ia(telemetria):
    print("\n ======= CONSULTA DE ANÁLISE POR IA =======\n")

    dados = ""

    for chave, valor in telemetria.items():

        if isinstance(valor, dict):

            for sub_chave, sub_valor in valor.items():
                dados += f"{sub_chave}: {sub_valor}\n"

        else:
            dados += f"{chave}: {valor}\n"

    prompt = f"""
    Você é um sistema de análise de telemetria de missão. Analise os seguintes dados: {dados} 
    FORNEÇA:
    1. Classificação geral do sistema.
    2. Possíveis anomalias.
    3. Sugestões de risco antes da decolagem. 
    """
    print("Enviando dados para análise por IA...\n")

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        resposta = model.generate_content(prompt)
        print("\n===== ANÁLISE DA IA =====\n")
        print(resposta.text)
    except Exception as e:
        print(Fore.RED + "Erro ao consultar a IA:" + Style.RESET_ALL)
        print(f"  Tipo: {type(e).__name__}")
        print(f"  Detalhes: {e}")
        print("  Verifique a conexão de rede e a chave de API e tente novamente.\n")
        print("Tentando uma segunda tentativa...\n")
        try:
            resposta = model.generate_content(prompt)
            print("\n===== ANÁLISE DA IA =====\n")
            print(resposta.text)
        except Exception as e2:
            print(Fore.RED + "Erro persistente ao consultar a IA:" + Style.RESET_ALL)
            print(f"  Tipo: {type(e2).__name__}")
            print(f"  Detalhes: {e2}\n")
            print(
                "Devido a problemas técnicos, utilizaremos análise simulada à seguir.\n"
            )
            analise_assistida_ia_simulada(telemetria)

    input("Pressione Enter para continuar...")


def analise_assistida_ia_simulada(telemetria):

    print("\n======= ANÁLISE ASSISTIDA POR IA =======\n")

    anomalias = []
    risco = "Baixo"

    # Pegando dados
    temp_int = telemetria["temperatura_interna"]
    temp_ext = telemetria["temperatura_externa"]
    integridade = telemetria["integridade_estrutural"]
    energia = telemetria["energia"]["nivel"]
    pressao = telemetria["pressao_tanques"]

    # Detectando anomalias
    if temp_ext > 70:
        anomalias.append("Temperatura externa elevada")

    if energia < 30:
        anomalias.append("Nível de energia baixo")

    if integridade != 1:
        anomalias.append("Integridade estrutural comprometida")

    if pressao < 3000:
        anomalias.append("Pressão dos tanques abaixo do ideal")

    # Classificação geral
    if len(anomalias) == 0:
        classificacao = "Sistema estável"
    elif len(anomalias) <= 2:
        classificacao = "Sistema com alertas"
        risco = "Médio"
    else:
        classificacao = "Sistema em condição crítica"
        risco = "Alto"

    # Exibição
    print("Classificação geral do sistema:", classificacao)

    print("\nPossíveis anomalias:")
    if anomalias:
        for a in anomalias:
            print("-", a)
    else:
        print("Nenhuma anomalia detectada")

    print("\nNível de risco:", risco)

    print("\nSugestões antes da decolagem:")

    if risco == "Baixo":
        print("- Sistema pronto para decolagem")

    if risco == "Médio":
        print("- Recomenda-se revisão preventiva dos sistemas")

    if risco == "Alto":
        print("- Abortagem da missão recomendada até correção dos problemas")

    input("Pressione Enter para continuar...")
