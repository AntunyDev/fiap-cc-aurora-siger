from colorama import Fore, Back, Style, init
from estruturas import fila_espera, lista_pousados, pilha_alerta
from busca_ordenacao import *
from autorizacao import autorizar_pouso

# Inicializa o colorama com autoreset
init(autoreset=True)


def desenhar_divisor(estilo="normal"):
    cor_borda = Fore.MAGENTA
    if estilo == "duplo":
        print(cor_borda + "═" * 116)
    elif estilo == "header":
        print(cor_borda + "╔" + "═" * 114 + "╗")
    elif estilo == "footer":
        print(cor_borda + "╚" + "═" * 114 + "╝")
    else:
        print(cor_borda + "─" * 116)


def painel_titulo(texto):
    print("\n")
    desenhar_divisor("header")
    print(
        Fore.MAGENTA
        + "║"
        + Style.BRIGHT
        + Fore.YELLOW
        + f" {texto.center(112)} "
        + Fore.MAGENTA
        + "║"
    )
    desenhar_divisor("footer")


def exibir_cabecalho():
    print(
        Fore.MAGENTA
        + Style.BRIGHT
        + r"""
    ░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░░█████╗░  ░██████╗██╗░██████╗░███████╗██████╗░
    ██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝██║██╔════╝░██╔════╝██╔══██╗
    ███████║██║░░░██║██████╔╝██║░░██║██████╔╝███████║  ╚█████╗░██║██║░░██╗░█████╗░░██████╔╝
    ██╔══██║██║░░░██║██╔══██╗██║░░██║██╔══██╗██╔══██║  ░╚═══██╗██║██║░░╚██╗██╔══╝░░██╔══██╗
    ██║░░██║╚██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║  ██████╔╝██║╚██████╔╝███████╗██║░░██║
    ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝
    """
    )
    print(
        Fore.CYAN
        + Style.BRIGHT
        + "       MÓDULO DE GERENCIAMENTO DE POUSO E ESTABILIZAÇÃO DE BASE (MGPEB) - MISSÃO AURORA SIGER".center(
            116
        )
    )
    print("\n")


def exibir_modulos_fila_inicial():
    painel_titulo("FILA INICIAL DE MÓDULOS EM ÓRBITA")

    # Header widths: NOME(12), TIPO(15), PRIO(5), COMB(8), MASSA(8), CRIT(5), CHEGADA(10), SENSORES(10), ÁREA(8)
    header = f" │ {'NOME':<12} │ {'TIPO':<15} │ {'PRIO':<5} │ {'COMB':<8} │ {'MASSA':<8} │ {'CRIT':<5} │ {'CHEGADA':<10} │ {'SENSORES':<10} │ {'ÁREA':<8} │"
    print(Fore.MAGENTA + " ┌" + "─" * (len(header) - 4) + "┐")
    print(Fore.MAGENTA + " │" + Fore.CYAN + Style.BRIGHT + header[2:-2] + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + " ├" + "─" * (len(header) - 4) + "┤")

    for m in fila_espera:
        # Sensores e Área: Padded first, then colored
        s_raw = "OK" if m["sensor_ok"] else "FALHA"
        sensor_status = (Fore.CYAN if m["sensor_ok"] else Fore.YELLOW) + f"{s_raw:<10}"

        a_raw = "LIVRE" if m["area_livre"] else "OCUP."
        area_status = (Fore.CYAN if m["area_livre"] else Fore.YELLOW) + f"{a_raw:<8}"

        # Combustível: Padded first, then colored
        c_raw = f"{m['combustivel']}%"
        if m["combustivel"] > 50:
            comb_cor = Fore.CYAN
        elif m["combustivel"] > 25:
            comb_cor = Fore.YELLOW
        else:
            comb_cor = Fore.MAGENTA
        comb_status = comb_cor + f"{c_raw:>8}"

        row = (
            f" {Fore.MAGENTA}│ "
            f"{Fore.CYAN}{m['nome']:<12}{Fore.MAGENTA} │ "
            f"{Fore.CYAN}{m['tipo']:<15}{Fore.MAGENTA} │ "
            f"{Fore.YELLOW}{m['prioridade']:^5}{Fore.MAGENTA} │ "
            f"{comb_status}{Fore.MAGENTA} │ "
            f"{Fore.CYAN}{m['massa']:>6}t  {Fore.MAGENTA}│ "
            f"{Fore.CYAN}{m['criticidade']:^5}{Fore.MAGENTA} │ "
            f"{Fore.CYAN}{m['hora_chegada']:>8}h {Fore.MAGENTA}│ "
            f"{sensor_status}{Fore.MAGENTA} │ "
            f"{area_status}{Fore.MAGENTA} │"
        )
        print(row)
    
    print(Fore.MAGENTA + " └" + "─" * (len(header) - 4) + "┘")


def exibir_fila_ordenada(fila):
    painel_titulo("REORGANIZAÇÃO DA FILA POR PRIORIDADE")

    fila_ordenada = bubble_sort_prioridade(list(fila))

    for m in fila_ordenada:
        print(
            f"  {Fore.MAGENTA}║ {Fore.CYAN}{m['nome']:<12} {Fore.MAGENTA}│ "
            f"{Fore.YELLOW}Prio: {m['prioridade']:<2} {Fore.MAGENTA}│ "
            f"{Fore.CYAN}{m['tipo']}"
        )

    desenhar_divisor()
    return fila_ordenada


def processar_pousos(fila):
    painel_titulo("SEQUÊNCIA DE POUSO E ESTABILIZAÇÃO")

    print(Fore.MAGENTA + " ╔" + "═" * 60 + "╗")
    while fila:
        modulo = fila.pop(0)
        status = autorizar_pouso(modulo)

        if status == "POUSO AUTORIZADO":
            lista_pousados.append(modulo)
            cor = Fore.CYAN
            ícone = "✔"
        elif status == "ALERTA":
            pilha_alerta.append(modulo)
            cor = Fore.YELLOW
            ícone = "⚠"
        else:
            cor = Fore.MAGENTA
            ícone = "✖"

        content = f"{modulo['nome']:<12} → {ícone} {status}"
        print(f" {Fore.MAGENTA}║ {cor}{content:<58} {Fore.MAGENTA}║")

    print(Fore.MAGENTA + " ╚" + "═" * 60 + "╝")


def exibir_resultados():
    painel_titulo("STATUS FINAL DA OPERAÇÃO")

    # Resumo estatístico
    total = len(lista_pousados) + len(pilha_alerta)
    print(f"  {Fore.CYAN}Total de módulos processados: {Fore.YELLOW}{total}")
    print(f"  {Fore.CYAN}Status de estabilização: {Fore.CYAN}{'OPERACIONAL' if not pilha_alerta else 'ATENÇÃO'}")
    print(Fore.MAGENTA + "  " + "─" * 40)

    print(Fore.CYAN + Style.BRIGHT + "  [✔] MÓDULOS POUSADOS COM SUCESSO:")
    if not lista_pousados:
        print(Fore.MAGENTA + "      (Nenhum módulo pousado)")
    else:
        for m in lista_pousados:
            print(f"      {Fore.CYAN}● {m['nome']:<10} {Fore.CYAN}│ {m['tipo']}")

    print("\n" + Fore.YELLOW + Style.BRIGHT + "  [⚠] MÓDULOS EM ESTADO DE ALERTA:")
    if not pilha_alerta:
        print(Fore.CYAN + "      (Nenhum alerta detectado)")
    else:
        for m in pilha_alerta:
            print(f"      {Fore.YELLOW}▲ {m['nome']:<10} {Fore.WHITE}│ {m['tipo']}")

    print("\n")
    desenhar_divisor("footer")


def exibir_buscas(fila):
    painel_titulo("RELATÓRIO DE BUSCA E TELEMETRIA")

    menor = buscar_menor_combustivel(fila)
    print(f"  {Fore.YELLOW}┌── {Fore.CYAN}Análise de Combustível {Fore.YELLOW}──────────────────")
    print(f"  {Fore.YELLOW}│  {Fore.MAGENTA}CRÍTICO: {Fore.CYAN}{menor['nome']} {Fore.YELLOW}com {Fore.MAGENTA}{menor['combustivel']}%")
    print(f"  {Fore.YELLOW}└─────────────────────────────────────────────")

    print("\n")

    habitacao = buscar_por_tipo(fila, "Habitação")
    print(f"  {Fore.YELLOW}┌── {Fore.CYAN}Módulos de Habitação Detectados {Fore.YELLOW}─────────")
    for h in habitacao:
        print(f"  {Fore.YELLOW}│  {Fore.YELLOW}► {h['nome']:<12} {Fore.CYAN}│ {h['tipo']}")
    print(f"  {Fore.YELLOW}└─────────────────────────────────────────────")

    desenhar_divisor()
