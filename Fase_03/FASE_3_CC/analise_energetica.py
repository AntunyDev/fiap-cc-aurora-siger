# analise_energetica.py

from dados_colonia import estado_colonia, sistemas_colonia

def calcular_consumo_real():
    """Soma o consumo apenas dos sistemas que estão ligados."""
    total = 0
    for categoria in sistemas_colonia.values():
        for sub in categoria["subsistemas"].values():
            if sub["status"]:
                total += sub["consumo"]
    return total

def analisar_fluxo_energia():
    """
    Analisa a geração vs consumo e gerencia a reserva de bateria E a estabilidade da rede.
    Lógica de Transbordo: Bateria primeiro, Estabilidade depois.
    """
    geracao = estado_colonia["geracao_estimada"]
    consumo = calcular_consumo_real()
    bateria = estado_colonia["reserva_bateria"]
    energia_rede = estado_colonia["energia_atual"]
    
    max_bateria = estado_colonia["capacidade_max_bateria"]
    max_estabilidade = 100.0

    saldo = geracao - consumo
    
    print(f"\n--- ANÁLISE DE FLUXO ENERGÉTICO ---")
    print(f"Geração: {geracao:.2f} | Consumo Real: {consumo:.2f} | Saldo: {saldo:.2f}")
    
    if saldo > 0:
        # 1. Prioridade: Estabilizar a Rede primeiro (tirar do Blackout)
        if energia_rede < max_estabilidade:
            ganho_rede = min(saldo, max_estabilidade - energia_rede)
            estado_colonia["energia_atual"] += ganho_rede
            saldo -= ganho_rede
            print(f"Ação: Restabelecendo estabilidade da rede (+{ganho_rede:.2f}).")
            if estado_colonia["energia_atual"] >= 100:
                print("REDE ESTABILIZADA: Iniciando recarga das baterias.")
        
        # 2. Se sobrar após estabilizar a rede, carrega a Bateria
        if saldo > 0 and bateria < max_bateria:
            carga = min(saldo, max_bateria - bateria)
            estado_colonia["reserva_bateria"] += carga
            print(f"Ação: Carregando reserva de bateria (+{carga:.2f}).")
            if estado_colonia["reserva_bateria"] >= 100:
                print("AVISO: Sistema em capacidade máxima total!")

    elif saldo < 0:
        deficit = abs(saldo)
        
        # 1. Descarrega Bateria
        if bateria > 0:
            descarga = min(deficit, bateria)
            estado_colonia["reserva_bateria"] -= descarga
            deficit -= descarga
            print(f"Ação: Usando reserva de bateria (-{descarga:.2f}).")
        
        # 2. Se ainda faltar, cai a estabilidade da rede
        if deficit > 0:
            perda_rede = min(deficit, energia_rede)
            estado_colonia["energia_atual"] -= perda_rede
            print(f"ALERTA: Queda de estabilidade na rede (-{perda_rede:.2f})!")
            
            # Mensagens de alerta baseadas no nível
            if estado_colonia["energia_atual"] <= 0:
                print("\n" + "!"*60)
                print(" BLACKOUT TOTAL: A colônia está às escuras! ".center(60, "!"))
                print("!"*60)
                print("Ação: Iniciando geradores de emergência apenas para OXIGÊNIO.")
            elif estado_colonia["energia_atual"] <= 20:
                print("PERIGO: Colapso iminente da rede elétrica!")

    else:
        print("Resultado: Sistema equilibrado.")

    # Atualiza o estado global
    estado_colonia["consumo_atual"] = consumo

