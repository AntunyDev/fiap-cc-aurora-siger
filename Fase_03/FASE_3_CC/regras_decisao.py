# regras_decisao.py

from dados_colonia import sistemas_colonia, estado_colonia

def navegar_sistemas(hierarquia, nivel=0):
    """
    Navega recursivamente entre subsistemas da colônia.
    Exemplo de Estrutura de Dados Hierárquica.
    """
    for chave, valor in hierarquia.items():
        espaco = "  " * nivel
        if isinstance(valor, dict) and "subsistemas" in valor:
            print(f"{espaco}[+] {valor['nome']} (Prioridade: {valor['prioridade']})")
            navegar_sistemas(valor["subsistemas"], nivel + 1)
        elif isinstance(valor, dict) and "status" in valor:
            status = "LIGADO" if valor["status"] else "DESLIGADO"
            print(f"{espaco}  - {chave}: {status} (Consumo: {valor['consumo']})")

def gerenciar_consumo():
    """
    Lógica de Decisão: Prioriza sistemas essenciais e desliga os não essenciais
    se a energia estiver baixa.
    """
    energia = estado_colonia["energia_atual"]
    bateria = estado_colonia["reserva_bateria"]
    
    print(f"\n--- LÓGICA DE DECISÃO ---")
    print(f"Status: Energia {energia}% | Bateria {bateria}%")

    # Regra: Se energia total (atual + bateria) for crítica
    if (energia + bateria) < 40:
        print("ALERTA CRÍTICO: Ativando protocolo de economia extrema.")
        # Desliga sistemas com prioridade menor que 5
        for cat, dados in sistemas_colonia.items():
            if dados["prioridade"] < 5:
                print(f"  > Desligando setor: {dados['nome']}")
                for sub in dados["subsistemas"]:
                    sistemas_colonia[cat]["subsistemas"][sub]["status"] = False
    
    elif (energia + bateria) < 70:
        print("ALERTA: Reduzindo consumo de sistemas não essenciais.")
        # Desliga sistemas com prioridade menor que 2
        for cat, dados in sistemas_colonia.items():
            if dados["prioridade"] < 2:
                print(f"  > Desligando setor: {dados['nome']}")
                for sub in dados["subsistemas"]:
                    sistemas_colonia[cat]["subsistemas"][sub]["status"] = False
    else:
        print("SITUAÇÃO NORMAL: Todos os sistemas operacionais.")
        # Garante que tudo esteja ligado
        for cat, dados in sistemas_colonia.items():
            for sub in dados["subsistemas"]:
                sistemas_colonia[cat]["subsistemas"][sub]["status"] = True

def exibir_status_geral():
    print("\n--- HIERARQUIA E STATUS DOS SISTEMAS ---")
    navegar_sistemas(sistemas_colonia)