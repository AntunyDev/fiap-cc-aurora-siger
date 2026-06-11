from collections import deque

def autorizar_pouso(modulo):
    combustivel = modulo["combustivel"]
    sensor_ok = modulo["sensor_ok"]
    area_livre = modulo["area_livre"]
    criticidade = modulo["criticidade"]

    # 1. Condições críticas (NEGADO)
    if combustivel < 15 or not sensor_ok or not area_livre:
        return "POUSO NEGADO"

    # 2. Situação de alerta
    elif combustivel < 30 or criticidade >= 9:
        return "ALERTA"

    # 3. Caso ideal
    else:
        return "POUSO AUTORIZADO"