import json
import sys
from datetime import datetime

try:
    # Garante saída em UTF-8 mesmo em consoles Windows configurados
    # com codepage antigo (cp1252/cp850), evitando UnicodeEncodeError
    # ao imprimir acentos e caracteres de desenho de caixa (║, ═, ✔...).
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import auxiliares

ARQUIVO_JSON = "dados_colonia.json"
ARQUIVO_REGISTROS = "registros_colonia.txt"

# DADOS DA COLÔNIA AURORA SIGER E EXIBIÇÃO DE DASHBOARD

def carregar_dados():
    """Carrega o JSON e garante que as estruturas principais existam."""
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if "modulos" not in dados:
            dados["modulos"] = []

        if "alertas" not in dados:
            dados["alertas"] = []

        return dados

    except FileNotFoundError:
        auxiliares.msg_erro(
            f"Arquivo '{ARQUIVO_JSON}' não encontrado."
        )
        return {"modulos": [], "alertas": []}

    except json.JSONDecodeError:
        auxiliares.msg_erro(
            f"Erro ao interpretar '{ARQUIVO_JSON}'."
        )
        return {"modulos": [], "alertas": []}


def salvar_dados(dados):
    """Persiste as alterações no JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def registrar_log(mensagem):
    """Registra uma ocorrência na memória textual do NCAS."""
    agora = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    with open(ARQUIVO_REGISTROS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{agora} {mensagem}\n")


def ler_memoria():
    """Lê o histórico textual do NCAS."""
    try:
        with open(ARQUIVO_REGISTROS, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        return ""


def localizar_modulo(nome_modulo, dados):
    for modulo in dados["modulos"]:
        if modulo["nome"] == nome_modulo:
            return modulo
    return None


def localizar_alerta(id_alerta, dados):
    for alerta in dados["alertas"]:
        if alerta["id_alerta"] == id_alerta:
            return alerta
    return None


def exibir_dashboard():
    dados = carregar_dados()

    total_modulos = len(dados["modulos"])
    total_alertas = len(dados["alertas"])

    criticos = sum(
        1 for alerta in dados["alertas"]
        if alerta.get("resultado_logico") is True
    )

    pendentes = sum(
        1 for alerta in dados["alertas"]
        if not alerta.get("resolvido", False)
    )

    revisoes = sum(
        1 for alerta in dados["alertas"]
        if alerta.get("revisao_humana") == "SIM"
    )

    auxiliares.imprimir_dashboard(
        total_modulos,
        total_alertas,
        criticos,
        pendentes,
        revisoes
    )


def exibir_modulos():
    auxiliares.painel_titulo("MÓDULOS DA COLÔNIA AURORA SIGER")
    dados = carregar_dados()
    auxiliares.imprimir_tabela_modulos(dados["modulos"])

# FUNÇÕES DE ALERTAS

def cadastrar_alerta():
    """
    Registra apenas o evento.
    A classificação não é solicitada ao operador:
    ela será calculada posteriormente a partir dos dados do módulo.
    """
    auxiliares.painel_titulo("CADASTRO DE REGISTRO DE ALERTA")

    dados = carregar_dados()

    if not dados["modulos"]:
        auxiliares.msg_erro("Não existem módulos cadastrados.")
        return

    modulo_afetado = auxiliares.solicitar_input(
        "Módulo afetado (Ex: HABIT-02): "
    ).upper()

    modulo = localizar_modulo(modulo_afetado, dados)

    if modulo is None:
        auxiliares.msg_erro("Módulo não encontrado na colônia.")
        return

    descricao = auxiliares.solicitar_input(
        "Descrição do evento/problema: "
    )

    if not descricao:
        auxiliares.msg_erro("A descrição não pode ficar vazia.")
        return

    proximo_id = max(
        [a["id_alerta"] for a in dados["alertas"]],
        default=0
    ) + 1

    novo_alerta = {
        "id_alerta": proximo_id,
        "modulo_afetado": modulo_afetado,
        "descricao_alerta": descricao,
        "resultado_logico": None,
        "classificacao_ia": None,
        "prioridade_ia": None,
        "recomendacao_ia": None,
        "revisao_humana": None,
        "resolvido": False
    }

    dados["alertas"].append(novo_alerta)
    salvar_dados(dados)

    registrar_log(
        f"Alerta ID {proximo_id} registrado para o módulo {modulo_afetado}. "
        f"Evento: {descricao}"
    )

    auxiliares.msg_sucesso("REGISTRO DE ALERTA CRIADO COM SUCESSO")


def consultar_alertas():
    auxiliares.painel_titulo("REGISTROS DE ALERTA")

    dados = carregar_dados()

    if not dados["alertas"]:
        auxiliares.msg_info("Nenhum alerta cadastrado.")
        return

    for alerta in dados["alertas"]:
        auxiliares.imprimir_alerta(alerta)

# LÓGICA BOOLEANA UTILIZADA NA PRIMEIRA CAMADA DE TRIAGEM

def calcular_variaveis_logicas(modulo):
    """
    Converte os dados quantitativos/operacionais em variáveis booleanas.

    F = falha no sensor
    E = alta criticidade
    R = área indisponível
    C = combustível baixo
    P = alta prioridade
    """
    F = not modulo["sensor_ok"]
    E = modulo["criticidade"] >= 8
    R = not modulo["area_livre"]
    C = modulo["combustivel"] < 40
    P = modulo["prioridade"] <= 2

    return F, E, R, C, P


def executar_regra_booleana(F, E, R, C, P):
    """
    Regra de triagem:
    CRÍTICO = (F AND E) OR (R AND E) OR (C AND P)
    """
    return (F and E) or (R and E) or (C and P)


def analisar_alerta():
    """
    Executa a primeira camada de inteligência do NCAS:
    uma triagem determinística baseada em lógica booleana.
    """
    auxiliares.painel_titulo("ANÁLISE LÓGICA DOS ALERTAS")

    dados = carregar_dados()

    if not dados["alertas"]:
        auxiliares.msg_info("Nenhum alerta cadastrado para análise.")
        return

    houve_analise = False

    for alerta in dados["alertas"]:
        modulo = localizar_modulo(alerta["modulo_afetado"], dados)

        if modulo is None:
            auxiliares.msg_aviso(
                f"Módulo do alerta #{alerta['id_alerta']} não encontrado."
            )
            continue

        F, E, R, C, P = calcular_variaveis_logicas(modulo)

        falha_critica = executar_regra_booleana(F, E, R, C, P)

        alerta["resultado_logico"] = falha_critica
        houve_analise = True

        auxiliares.imprimir_analise_alerta(
            alerta["id_alerta"],
            modulo["nome"],
            modulo["criticidade"],
            modulo["prioridade"],
            F, E, R, C, P,
            falha_critica
        )

        resultado = "CRÍTICO" if falha_critica else "NORMAL"

        registrar_log(
            f"Alerta ID {alerta['id_alerta']} passou pela triagem lógica. "
            f"Resultado: {resultado}."
        )

    if houve_analise:
        salvar_dados(dados)
        auxiliares.msg_sucesso(
            "TRIAGEM BOOLEANA CONCLUÍDA"
        )

# ENGENHARIA DE PROMPT

def gerar_prompt(alerta, modulo, resultado_logico, memoria_relevante=""):
    """
    Constrói dinamicamente o contexto enviado ao modelo de IA simulado.
    """

    resultado = "CRÍTICO" if resultado_logico else "NORMAL"
    sensor = "OK" if modulo["sensor_ok"] else "FALHA"
    area = "LIVRE" if modulo["area_livre"] else "INDISPONÍVEL"

    prompt = f"""
[TIPO DE PROMPT: ZERO-SHOT]
Este prompt é aplicado diretamente ao alerta atual, sem nenhum exemplo
prévio de entrada/saída embutido nele (ver exemplo few-shot em
auxiliares.exibir_prompts, usado apenas como referência de padrão).

[SYSTEM PROMPT]
Você é o Núcleo Cognitivo da Aurora Siger (NCAS).
Sua função é apoiar decisões operacionais da colônia.
Você deve interpretar os dados fornecidos, explicar sua conclusão
e preservar a revisão humana em decisões críticas.

[CONTEXTO OPERACIONAL]
Módulo: {modulo["nome"]}
Tipo: {modulo["tipo"]}
Prioridade operacional: {modulo["prioridade"]}
Criticidade: {modulo["criticidade"]}/10
Combustível: {modulo["combustivel"]}%
Massa: {modulo["massa"]} toneladas
Hora de chegada: {modulo["hora_chegada"]}h
Sensor: {sensor}
Área: {area}

[EVENTO]
ID do alerta: {alerta["id_alerta"]}
Descrição: {alerta["descricao_alerta"]}

[RESULTADO DA TRIAGEM BOOLEANA]
{resultado}

[MEMÓRIA OPERACIONAL RELEVANTE]
{memoria_relevante if memoria_relevante else "Nenhum histórico adicional disponível."}

[INSTRUÇÕES DE ANÁLISE]
1. Avalie o risco operacional.
2. Considere o conjunto de dados, e não apenas uma variável.
3. Determine a prioridade de atendimento.
4. Recomende uma ação proporcional ao risco.
5. Explique os fatores utilizados.
6. Decisões críticas devem permanecer sujeitas à revisão humana.

[RESTRIÇÕES ÉTICAS]
- Não utilize atributos pessoais irrelevantes para a decisão.
- Não crie informações que não estejam disponíveis.
- Não oculte incertezas.
- Não substitua a supervisão humana em decisões críticas.

[STRUCTURED OUTPUT]
CLASSIFICAÇÃO:
PRIORIDADE:
JUSTIFICATIVA:
RECOMENDAÇÃO:
REVISÃO HUMANA:
"""

    return prompt.strip()


def obter_memoria_relevante(nome_modulo):
    """
    Recupera linhas anteriores relacionadas ao módulo.
    É uma memória textual simples e intencionalmente local.
    """
    memoria = ler_memoria()

    if not memoria:
        return ""

    linhas = memoria.splitlines()

    relevantes = [
        linha for linha in linhas
        if nome_modulo in linha
    ]

    # Mantém somente um pequeno contexto para não poluir o prompt.
    return "\n".join(relevantes[-5:])

# SIMULAÇÃO DE IA

def interpretar_como_ia(alerta, modulo):
    """
    Simula a saída de um modelo generativo local.

    Importante:
    esta função não é uma API de IA real. Ela representa uma camada
    cognitiva determinística que recebe o prompt/contexto e produz
    uma resposta estruturada.
    """

    resultado_logico = alerta.get("resultado_logico")

    # Se a lógica ainda não foi executada, executamos a triagem.
    if resultado_logico is None:
        F, E, R, C, P = calcular_variaveis_logicas(modulo)
        resultado_logico = executar_regra_booleana(F, E, R, C, P)
        alerta["resultado_logico"] = resultado_logico

    anomalias = []

    if not modulo["sensor_ok"]:
        anomalias.append("falha no sensor")

    if modulo["combustivel"] < 40:
        anomalias.append("combustível abaixo de 40%")

    if not modulo["area_livre"]:
        anomalias.append("área indisponível")

    if modulo["criticidade"] >= 8:
        anomalias.append("alta criticidade")

    if modulo["prioridade"] <= 2:
        anomalias.append("alta prioridade operacional")

    # Camada contextual: a IA considera fatores adicionais.
    if resultado_logico:
        classificacao = "ALERTA SEVERO"
        prioridade = "MÁXIMA"

        justificativa = (
            "A triagem lógica identificou uma combinação de condições "
            "críticas. Fatores relevantes: "
            + (", ".join(anomalias) if anomalias else "condições críticas detectadas")
            + "."
        )

        recomendacao = (
            "Acionar o protocolo operacional correspondente, "
            "preservando a supervisão humana antes de qualquer "
            "ação de alto impacto."
        )

        revisao_humana = "SIM"

    elif anomalias:
        classificacao = "ATENÇÃO"
        prioridade = "ALTA"

        justificativa = (
            "A regra booleana não classificou o alerta como crítico, "
            "porém a análise contextual identificou fatores que "
            "justificam acompanhamento. Fatores observados: "
            + ", ".join(anomalias) + "."
        )

        recomendacao = (
            f"Realizar inspeção preventiva no módulo {modulo['nome']} "
            f"e verificar o evento registrado: "
            f"'{alerta['descricao_alerta']}'."
        )

        revisao_humana = "SIM"

    else:
        classificacao = "ROTINA"
        prioridade = "BAIXA"

        justificativa = (
            "Os parâmetros operacionais disponíveis estão dentro "
            "dos limites considerados normais e não foram "
            "identificadas anomalias adicionais."
        )

        recomendacao = (
            "Manter monitoramento operacional e registrar novas "
            "ocorrências caso os parâmetros se alterem."
        )

        revisao_humana = "NÃO"

    return {
        "classificacao": classificacao,
        "prioridade": prioridade,
        "justificativa": justificativa,
        "recomendacao": recomendacao,
        "revisao_humana": revisao_humana
    }


def simular_respostas_ia():
    """
    Segunda camada do NCAS:
    constrói o prompt, consulta a memória e simula a interpretação
    cognitiva do cenário.
    """
    auxiliares.painel_titulo(
        "SIMULAÇÃO DE RESPOSTAS DA IA - CAMADA COGNITIVA"
    )

    dados = carregar_dados()

    if not dados["alertas"]:
        auxiliares.msg_info("Nenhum alerta disponível.")
        return

    processados = 0

    for alerta in dados["alertas"]:
        if alerta.get("resolvido"):
            continue

        modulo = localizar_modulo(alerta["modulo_afetado"], dados)

        if modulo is None:
            continue

        # Garante que a primeira camada já tenha sido executada.
        if alerta.get("resultado_logico") is None:
            F, E, R, C, P = calcular_variaveis_logicas(modulo)
            alerta["resultado_logico"] = executar_regra_booleana(F, E, R, C, P)

        memoria = obter_memoria_relevante(modulo["nome"])

        prompt = gerar_prompt(
            alerta,
            modulo,
            alerta["resultado_logico"],
            memoria
        )

        print()
        auxiliares.msg_info(
            f"Construindo contexto cognitivo para o alerta #{alerta['id_alerta']}..."
        )

        # Mostra o prompt durante a demonstração.
        auxiliares.imprimir_prompt(prompt)

        resposta = interpretar_como_ia(alerta, modulo)

        alerta["classificacao_ia"] = resposta["classificacao"]
        alerta["prioridade_ia"] = resposta["prioridade"]
        alerta["recomendacao_ia"] = resposta["recomendacao"]
        alerta["revisao_humana"] = resposta["revisao_humana"]

        auxiliares.imprimir_simulacao_ia(
            modulo["nome"],
            resposta["classificacao"],
            resposta["prioridade"],
            resposta["justificativa"],
            resposta["recomendacao"],
            resposta["revisao_humana"]
        )

        registrar_log(
            f"IA simulada analisou o alerta ID {alerta['id_alerta']}. "
            f"Classificação: {resposta['classificacao']}. "
            f"Prioridade: {resposta['prioridade']}. "
            f"Revisão humana: {resposta['revisao_humana']}."
        )

        processados += 1

    salvar_dados(dados)

    if processados == 0:
        auxiliares.msg_info(
            "Não existem alertas abertos aguardando interpretação."
        )
    else:
        auxiliares.msg_sucesso(
            f"{processados} alerta(s) interpretado(s) pela camada cognitiva."
        )

# LOG DOS REGISTROS

def consultar_registros():
    auxiliares.painel_titulo("MEMÓRIA OPERACIONAL DO NCAS")

    memoria = ler_memoria()

    if not memoria:
        auxiliares.msg_info("Nenhum registro encontrado.")
        return

    print()
    print(memoria)

# GERENCIAMENTO DE STATUS

def gerenciar_status_alerta():
    auxiliares.painel_titulo("GERENCIAMENTO DE ALERTAS")

    dados = carregar_dados()

    if not dados["alertas"]:
        auxiliares.msg_info("Nenhum alerta cadastrado.")
        return

    consultar_alertas()

    entrada = auxiliares.solicitar_input(
        "\nInforme o ID do alerta: "
    )

    if not entrada.isdigit():
        auxiliares.msg_erro("ID inválido.")
        return

    id_alerta = int(entrada)
    alerta = localizar_alerta(id_alerta, dados)

    if alerta is None:
        auxiliares.msg_erro("Alerta não encontrado.")
        return

    status_atual = "RESOLVIDO" if alerta["resolvido"] else "ABERTO"

    print(f"\n  Status atual: {status_atual}")
    print("  [1] Marcar como RESOLVIDO")
    print("  [2] Reabrir alerta")
    print("  [0] Cancelar")

    opcao = auxiliares.solicitar_input("Escolha: ")

    if opcao == "1":
        alerta["resolvido"] = True
        registrar_log(
            f"Alerta ID {id_alerta} marcado como RESOLVIDO pelo operador."
        )
        auxiliares.msg_sucesso("ALERTA MARCADO COMO RESOLVIDO")

    elif opcao == "2":
        alerta["resolvido"] = False
        registrar_log(
            f"Alerta ID {id_alerta} REABERTO pelo operador."
        )
        auxiliares.msg_sucesso("ALERTA REABERTO")

    else:
        auxiliares.msg_info("Operação cancelada.")
        return

    salvar_dados(dados)

# MENU PRINCIPAL NCAS

def menu():
    auxiliares.exibir_cabecalho()

    while True:
        exibir_dashboard()

        auxiliares.painel_titulo("MENU PRINCIPAL")
        auxiliares.exibir_menu_opcoes()

        opcao = auxiliares.solicitar_input(
            "\n  Escolha uma ação: "
        )

        if opcao == "1":
            cadastrar_alerta()

        elif opcao == "2":
            consultar_alertas()

        elif opcao == "3":
            analisar_alerta()

        elif opcao == "4":
            auxiliares.exibir_prompts()

        elif opcao == "5":
            consultar_registros()

        elif opcao == "6":
            simular_respostas_ia()

        elif opcao == "7":
            exibir_modulos()

        elif opcao == "8":
            gerenciar_status_alerta()

        elif opcao == "0":
            print("\n  Encerrando o sistema NCAS...\n")
            break

        else:
            auxiliares.msg_aviso("Opção inválida.")


if __name__ == "__main__":
    menu()
