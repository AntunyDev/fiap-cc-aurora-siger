# main.py

import os
from dados_colonia import estado_colonia
from regras_decisao import gerenciar_consumo, exibir_status_geral
from analise_energetica import analisar_fluxo_energia, calcular_consumo_real
from modelo_previsao import prever_energia

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    while True:
        limpar_tela()
        # Atualiza o consumo real antes de exibir o menu
        estado_colonia['consumo_atual'] = calcular_consumo_real()
        print("\n" + "="*60)

        print(r"""
  ____  _     ____  ____  ____  ____    ____  _  _____ _____ ____ 
 /  _ \/ \ /\/  __\/  _ \/  __\/  _ \  / ___\/ \/  __//  __//  __\
 | / \|| | |||  \/|| / \||  \/|| / \|  |    \| || |  _|  \  |  \/|
 | |-||| \_/||    /| \_/||    /| |-||  \___ || || |_//|  /_ |    /
 \_/ \|\____/\_/\_\\____/\_/\_\\_/ \|  \____/\_/\____\\____\\_/\_\
        """)
        print(" PAINEL DE CONTROLE ENERGÉTICO ".center(60))
        print("="*60)
        print(f" GERAÇÃO: {estado_colonia['geracao_estimada']} | CONSUMO: {estado_colonia['consumo_atual']} | REDE: {estado_colonia['energia_atual']:.1f}% | BATERIA: {estado_colonia['reserva_bateria']:.1f}%")
        print("-" * 60)
        print("1. Ver Hierarquia e Status dos Sistemas")
        print("2. Aplicar Regras de Decisão (Modo Automático)")
        print("3. Analisar Fluxo Energético e Bateria")
        print("4. Executar Previsão de Geração (Regressão)")
        print("5. Alterar Condições Climáticas (Vento)")
        print("0. Sair")
        print("="*60)
        
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Encerrando sistema...")
            break
            
        # Limpa para mostrar apenas o resultado da opção
        limpar_tela()

        if opcao == "1":
            exibir_status_geral()
        
        elif opcao == "2":
            gerenciar_consumo()
        
        elif opcao == "3":
            analisar_fluxo_energia()
        
        elif opcao == "4":
            try:
                print("--- PREVISÃO DE ENERGIA ---")
                input_vento = input("Digite a velocidade do vento esperada (m/s): ")
                vento = float(input_vento)
                if vento < 0:
                    print("Erro: A velocidade do vento não pode ser negativa.")
                else:
                    prever_energia(vento)
            except ValueError:
                print(f"Erro: '{input_vento}' não é um número válido.")
        
        elif opcao == "5":
            try:
                print("--- AJUSTE CLIMÁTICO ---")
                input_novo = input("Digite a velocidade atual do vento (m/s): ")
                novo_vento = float(input_novo)
                if novo_vento < 0:
                    print("Erro: Velocidade negativa não é válida para este modelo.")
                else:
                    from modelo_previsao import treinar_modelo
                    m, b = treinar_modelo()
                    estado_colonia['geracao_estimada'] = round((m * novo_vento) + b, 2)
                    print(f"\n[SUCESSO] Condições atualizadas.")
                    print(f"Nova Geração Estimada: {estado_colonia['geracao_estimada']} unidades.")
            except ValueError:
                print(f"Erro: '{input_novo}' não é um valor numérico válido.")
        
        else:
            print("Opção inválida!")
        
        print("\n" + "-"*60)
        input("Pressione Enter para voltar ao menu...")

if __name__ == "__main__":
    menu_principal()
