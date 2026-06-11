from auxiliares import (
    exibir_cabecalho,
    exibir_modulos_fila_inicial,
    exibir_buscas,
    exibir_fila_ordenada,
    processar_pousos,
    exibir_resultados
)
from estruturas import fila_espera
from colorama import Fore, Style

def main():
    # 1. Cabeçalho e Identificação da Missão
    exibir_cabecalho()
    
    # 2. Exibição da situação atual da órbita
    exibir_modulos_fila_inicial()

    # 3. Análises de Telemetria e Buscas
    exibir_buscas(list(fila_espera))

    # 4. Reorganização Estratégica
    fila_ordenada = exibir_fila_ordenada(fila_espera)

    # 5. Execução do Protocolo de Pouso
    processar_pousos(fila_ordenada)

    # 6. Relatório Final de Estabilização
    exibir_resultados()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\n\n[!] Operação interrompida pelo operador.")
    except Exception as e:
        print(Fore.MAGENTA + Style.BRIGHT + f"\n\n[X] Erro crítico no MGPEB: {Fore.CYAN}{e}")