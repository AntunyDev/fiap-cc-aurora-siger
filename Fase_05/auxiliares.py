# auxiliares.py
import builtins
import os
import textwrap

if os.name == "nt":
    # Habilita a interpretação de sequências ANSI no console do Windows
    # (cmd.exe/PowerShell), dispensando a biblioteca externa colorama.
    os.system("")


class _CorTexto:
    """Substitui colorama.Fore/Style usando códigos ANSI puros (stdlib)."""
    MAGENTA = "\033[35m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT = "\033[1m"


Fore = _CorTexto
Style = _CorTexto
_RESET = "\033[0m"


def print(*args, **kwargs):
    """print() com reset automático de cor ao final (equivalente a colorama autoreset=True)."""
    builtins.print(*args, _RESET, **kwargs)


LARGURA = 116


# ============================================================
# ELEMENTOS VISUAIS
# ============================================================

def desenhar_divisor(estilo="normal"):
    cor = Fore.MAGENTA

    if estilo == "duplo":
        print(cor + "═" * LARGURA)
    elif estilo == "header":
        print(cor + "╔" + "═" * (LARGURA - 2) + "╗")
    elif estilo == "footer":
        print(cor + "╚" + "═" * (LARGURA - 2) + "╝")
    else:
        print(cor + "─" * LARGURA)


def painel_titulo(texto):
    print()
    desenhar_divisor("header")
    print(
        Fore.MAGENTA + "║" +
        Style.BRIGHT + Fore.YELLOW +
        f" {texto.center(LARGURA - 4)} " +
        Fore.MAGENTA + "║"
    )
    desenhar_divisor("footer")


def exibir_cabecalho():
    print(
        Fore.MAGENTA + Style.BRIGHT + r"""
     ███╗   ██╗ ██████╗ █████╗ ███████╗
     ████╗  ██║██╔════╝██╔══██╗██╔════╝
     ██╔██╗ ██║██║     ███████║███████╗
     ██║╚██╗██║██║     ██╔══██║╚════██║
     ██║ ╚████║╚██████╗██║  ██║███████║
     ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝
        """
    )
    print(
        Fore.CYAN + Style.BRIGHT +
        "NÚCLEO COGNITIVO DA AURORA SIGER (NCAS)".center(LARGURA)
    )
    print(
        Fore.CYAN +
        "SISTEMA DE ANÁLISE E APOIO À DECISÃO DA COLÔNIA".center(LARGURA)
    )
    print()


# ============================================================
# MENSAGENS E INPUT
# ============================================================

def msg_erro(texto):
    print(Fore.MAGENTA + f"  [✖] {texto}")


def msg_aviso(texto):
    print(Fore.YELLOW + f"  [⚠] {texto}")


def msg_info(texto):
    print(Fore.CYAN + f"  [i] {texto}")


def msg_sucesso(texto):
    largura = len(texto) + 6
    print("\n" + Fore.CYAN + "  ┌" + "─" * largura + "┐")
    print(Fore.CYAN + f"  │  ✔ {texto}  │")
    print(Fore.CYAN + "  └" + "─" * largura + "┘")


def solicitar_input(pergunta):
    return input(Fore.CYAN + f"  {pergunta}").strip()


# ============================================================
# TABELAS E PAINÉIS
# ============================================================

def imprimir_tabela_modulos(modulos):
    if not modulos:
        msg_aviso("Nenhum módulo cadastrado.")
        return

    print()
    print(Fore.MAGENTA + " ┌" + "─"*14 + "┬" + "─"*15 + "┬" + "─"*7 + "┬" + "─"*8 + "┬" + "─"*8 + "┬" + "─"*7 + "┬" + "─"*10 + "┬" + "─"*10 + "┬" + "─"*9 + "┐")
    
    col_nome = "NOME".ljust(12)
    col_tipo = "TIPO".ljust(13)
    col_prio = "PRIO".center(5)
    col_comb = "COMB".center(6)
    col_massa = "MASSA".center(6)
    col_crit = "CRIT".center(5)
    col_chegada = "CHEGADA".center(8)
    col_sensor = "SENSOR".center(8)
    col_area = "ÁREA".center(7)

    print(Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_nome + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_tipo + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_prio + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_comb + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_massa + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_crit + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_chegada + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_sensor + Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + col_area + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + " ├" + "─"*14 + "┼" + "─"*15 + "┼" + "─"*7 + "┼" + "─"*8 + "┼" + "─"*8 + "┼" + "─"*7 + "┼" + "─"*10 + "┼" + "─"*10 + "┼" + "─"*9 + "┤")

    for modulo in modulos:
        comb = modulo["combustivel"]
        if comb > 50:
            cor_comb = Fore.CYAN
        elif comb > 25:
            cor_comb = Fore.YELLOW
        else:
            cor_comb = Fore.MAGENTA

        sensor_text = "OK" if modulo["sensor_ok"] else "FALHA"
        cor_sensor = Fore.CYAN if modulo["sensor_ok"] else Fore.YELLOW
        
        area_text = "LIVRE" if modulo["area_livre"] else "OCUP."
        cor_area = Fore.CYAN if modulo["area_livre"] else Fore.YELLOW

        print(
            Fore.MAGENTA + " │ " + Fore.CYAN + f"{modulo['nome']}".ljust(12) + 
            Fore.MAGENTA + " │ " + Fore.CYAN + f"{modulo['tipo']}".ljust(13) + 
            Fore.MAGENTA + " │ " + Fore.YELLOW + f"{modulo['prioridade']}".center(5) + 
            Fore.MAGENTA + " │ " + cor_comb + f"{comb}%".rjust(6) + 
            Fore.MAGENTA + " │ " + Fore.CYAN + f"{modulo['massa']}t".rjust(6) + 
            Fore.MAGENTA + " │ " + Fore.CYAN + f"{modulo['criticidade']}".center(5) + 
            Fore.MAGENTA + " │ " + Fore.CYAN + f"{modulo['hora_chegada']}h".rjust(8) + 
            Fore.MAGENTA + " │ " + cor_sensor + sensor_text.center(8) + 
            Fore.MAGENTA + " │ " + cor_area + area_text.center(7) + 
            Fore.MAGENTA + " │"
        )

    print(Fore.MAGENTA + " └" + "─"*14 + "┴" + "─"*15 + "┴" + "─"*7 + "┴" + "─"*8 + "┴" + "─"*8 + "┴" + "─"*7 + "┴" + "─"*10 + "┴" + "─"*10 + "┴" + "─"*9 + "┘")


def imprimir_alerta(alerta):
    resultado = alerta.get("resultado_logico")

    if resultado is True:
        texto_status = "⚠ CRÍTICO (LÓGICA)"
        cor_status = Fore.YELLOW + Style.BRIGHT
    elif resultado is False:
        texto_status = "✔ NORMAL (LÓGICA)"
        cor_status = Fore.CYAN + Style.BRIGHT
    else:
        texto_status = "○ PENDENTE DE ANÁLISE"
        cor_status = Fore.MAGENTA

    situacao = "RESOLVIDO" if alerta.get("resolvido") else "ABERTO"
    classificacao_ia = alerta.get("classificacao_ia") or "PENDENTE"

    print(Fore.MAGENTA + " ┌" + "─" * 63 + "┐")
    print(Fore.MAGENTA + " │ " + Fore.CYAN + Style.BRIGHT + f"ALERTA #{alerta['id_alerta']}".ljust(61) + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + " ├" + "─" * 63 + "┤")
    print(Fore.MAGENTA + " │ " + Fore.CYAN + f"Módulo:            {alerta['modulo_afetado']}".ljust(61) + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + " │ " + Fore.CYAN + f"Descrição:         {alerta['descricao_alerta']}".ljust(61) + Fore.MAGENTA + " │")
    
    # Resolve o problema das cores do status calculando os espaços baseados na string sem cor
    linha_resultado = f"Resultado lógico:  {texto_status}"
    espacos = " " * max(0, 61 - len(linha_resultado))
    print(Fore.MAGENTA + " │ " + Fore.CYAN + "Resultado lógico:  " + cor_status + texto_status + espacos + Fore.MAGENTA + " │")
    
    print(Fore.MAGENTA + " │ " + Fore.CYAN + f"Avaliação IA:      {classificacao_ia}".ljust(61) + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + " │ " + Fore.CYAN + f"Situação:          {situacao}".ljust(61) + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + " └" + "─" * 63 + "┘")


def imprimir_analise_alerta(alerta_id, modulo_nome, criticidade, prioridade, F, E, R, C, P, falha_critica):
    print()
    print(Fore.MAGENTA + " ╔" + "═" * 60 + "╗")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + Style.BRIGHT + f"ANÁLISE BOOLEANA DO ALERTA #{alerta_id}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + f"Módulo: {modulo_nome}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + f"Criticidade: {criticidade}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + f"Prioridade: {prioridade}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")
    print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"F = Falha no sensor:       {str(F)}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"E = Alta criticidade:      {str(E)}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"R = Área indisponível:     {str(R)}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"C = Combustível baixo:     {str(C)}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"P = Alta prioridade:       {str(P)}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + "REGRA: (F AND E) OR (R AND E) OR (C AND P)".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")

    resultado = "CRÍTICO" if falha_critica else "NORMAL"
    cor = Fore.YELLOW if falha_critica else Fore.CYAN

    print(Fore.MAGENTA + " ║ " + cor + Style.BRIGHT + f"RESULTADO DA TRIAGEM: {resultado}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╚" + "═" * 60 + "╝")


def imprimir_prompt(prompt):
    print()
    print(Fore.MAGENTA + " ╔" + "═" * 60 + "╗")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + Style.BRIGHT + "PROMPT GERADO PELO NCAS".center(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")

    for linha in prompt.splitlines():
        linhas = textwrap.wrap(linha, width=58) or [""]
        for parte in linhas:
            print(Fore.MAGENTA + " ║ " + Fore.WHITE + f"{parte}".ljust(58) + Fore.MAGENTA + " ║")

    print(Fore.MAGENTA + " ╚" + "═" * 60 + "╝")


def imprimir_simulacao_ia(modulo_nome, classificacao, prioridade, justificativa, recomendacao, revisao_humana):
    print()
    print(Fore.MAGENTA + " ╔" + "═" * 60 + "╗")
    print(Fore.MAGENTA + " ║ " + Fore.CYAN + Style.BRIGHT + "ANÁLISE COGNITIVA DO NCAS".center(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╠" + "═" * 60 + "╣")
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + f"Módulo: {modulo_nome}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + " " * 58 + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + f"CLASSIFICAÇÃO: {classificacao}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + f"PRIORIDADE: {prioridade}".ljust(58) + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + " " * 58 + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + "JUSTIFICATIVA:".ljust(58) + Fore.MAGENTA + " ║")

    for linha in textwrap.wrap(justificativa, width=58):
        print(Fore.MAGENTA + " ║ " + Fore.YELLOW + f"{linha}".ljust(58) + Fore.MAGENTA + " ║")

    print(Fore.MAGENTA + " ║ " + " " * 58 + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + "RECOMENDAÇÃO:".ljust(58) + Fore.MAGENTA + " ║")

    for linha in textwrap.wrap(recomendacao, width=58):
        print(Fore.MAGENTA + " ║ " + Fore.CYAN + f"{linha}".ljust(58) + Fore.MAGENTA + " ║")

    print(Fore.MAGENTA + " ║ " + " " * 58 + Fore.MAGENTA + " ║")

    cor_revisao = Fore.YELLOW if revisao_humana == "SIM" else Fore.CYAN
    linha_revisao = f"REVISÃO HUMANA: {revisao_humana}"
    espacos = " " * max(0, 58 - len(linha_revisao))
    
    print(Fore.MAGENTA + " ║ " + Fore.WHITE + "REVISÃO HUMANA: " + cor_revisao + revisao_humana + espacos + Fore.MAGENTA + " ║")
    print(Fore.MAGENTA + " ╚" + "═" * 60 + "╝")


def imprimir_dashboard(total_modulos, total_alertas, criticos, pendentes, revisoes):
    painel_titulo("STATUS OPERACIONAL DA COLÔNIA")

    # Força exatos 20 caracteres por coluna para não quebrar alinhamento
    col1_1 = f" MÓDULOS: {total_modulos}".ljust(20)
    col2_1 = f" ALERTAS: {total_alertas}".ljust(20)
    col3_1 = f" CRÍTICOS: {criticos}".ljust(20)

    col1_2 = f" PENDENTES: {pendentes}".ljust(20)
    col2_2 = f" REVISÕES IA: {revisoes}".ljust(20)
    col3_2 = f" NCAS: ATIVO".ljust(20)

    print(Fore.MAGENTA + " ┌" + "─"*20 + "┬" + "─"*20 + "┬" + "─"*20 + "┐")
    print(Fore.MAGENTA + " │" + Fore.CYAN + col1_1 + Fore.MAGENTA + "│" + Fore.CYAN + col2_1 + Fore.MAGENTA + "│" + Fore.YELLOW + col3_1 + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + " ├" + "─"*20 + "┼" + "─"*20 + "┼" + "─"*20 + "┤")
    print(Fore.MAGENTA + " │" + Fore.YELLOW + col1_2 + Fore.MAGENTA + "│" + Fore.YELLOW + col2_2 + Fore.MAGENTA + "│" + Fore.CYAN + col3_2 + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + " └" + "─"*20 + "┴" + "─"*20 + "┴" + "─"*20 + "┘")


# ============================================================
# PROMPTS E MENU
# ============================================================

def exibir_prompts():
    painel_titulo("PROMPTS UTILIZADOS PELO NCAS")

    print(Fore.YELLOW + Style.BRIGHT + "\n  [1] ZERO-SHOT PROMPT")
    print(Fore.WHITE +
          "  Prompt aplicado diretamente a um alerta novo, sem nenhum exemplo de "
          "entrada/saída embutido (ver saída completa na opção 6 do menu).")

    print(Fore.CYAN + Style.BRIGHT + "\n  [2] SYSTEM PROMPT")
    print(Fore.WHITE +
          "  Define o papel do NCAS como núcleo cognitivo responsável por analisar eventos operacionais.")

    print(Fore.CYAN + Style.BRIGHT + "\n  [3] CONTEXT PROMPT")
    print(Fore.WHITE +
          "  Reúne os dados do módulo, o alerta registrado e o resultado da triagem booleana.")

    print(Fore.CYAN + Style.BRIGHT + "\n  [4] STRUCTURED OUTPUT")
    print(Fore.WHITE +
          "  Exige uma resposta padronizada com classificação, prioridade, justificativa, recomendação e revisão humana.")

    print(Fore.CYAN + Style.BRIGHT + "\n  [5] ETHICAL CONSTRAINTS")
    print(Fore.WHITE +
          "  Determina que a recomendação utilize somente dados operacionais relevantes e preserve a revisão humana em decisões críticas.")

    print(Fore.YELLOW + Style.BRIGHT + "\n  [6] FEW-SHOT PROMPT / EXEMPLO")
    print(Fore.WHITE +
          "  Demonstra ao modelo o padrão esperado de resposta para melhorar consistência e interpretação.")


def exibir_menu_opcoes():
    print(Fore.CYAN + "  [1] " + Fore.WHITE + "Cadastrar Registro de Alerta")
    print(Fore.CYAN + "  [2] " + Fore.WHITE + "Consultar Registros de Alerta")
    print(Fore.YELLOW + "  [3] " + Fore.WHITE + "Executar Análise Lógica")
    print(Fore.CYAN + "  [4] " + Fore.WHITE + "Exibir Prompts")
    print(Fore.CYAN + "  [5] " + Fore.WHITE + "Consultar Memória e Logs")
    print(Fore.YELLOW + "  [6] " + Fore.WHITE + "Simular Respostas da IA")
    print(Fore.CYAN + "  [7] " + Fore.WHITE + "Visualizar Módulos")
    print(Fore.CYAN + "  [8] " + Fore.WHITE + "Gerenciar Status dos Alertas")
    print(Fore.MAGENTA + "  [0] " + Fore.WHITE + "Sair")
    desenhar_divisor()