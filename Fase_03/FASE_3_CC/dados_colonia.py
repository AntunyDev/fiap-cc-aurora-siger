# dados_colonia.py

# Estado Inicial da Colônia
estado_colonia = {
    "energia_atual": 60.0,      # Unidades de energia
    "consumo_atual": 40.0,      # Demanda atual
    "reserva_bateria": 50.0,    # Capacidade atual de armazenamento (0-100)
    "capacidade_max_bateria": 100.0,
    "geracao_estimada": 45.0    # Geração baseada no clima atual
}

# Dados Históricos para Regressão (Vento vs Energia Gerada)
historico_clima = {
    "vento": [5, 8, 10, 12, 15],
    "energia": [10, 21, 26, 30, 39]
}

# Estrutura Hierárquica dos Sistemas
# Cada sistema tem um status (ligado/desligado) e uma prioridade (1: Baixa, 10: Crítica)
sistemas_colonia = {
    "suporte_vida": {
        "nome": "Suporte à Vida",
        "prioridade": 10,
        "subsistemas": {
            "oxigenio": {"status": True, "consumo": 15},
            "agua": {"status": True, "consumo": 10},
            "temperatura": {"status": True, "consumo": 5}
        }
    },
    "energia": {
        "nome": "Gestão Energética",
        "prioridade": 9,
        "subsistemas": {
            "solar": {"status": True, "consumo": 2},
            "eolico": {"status": True, "consumo": 2}
        }
    },
    "pesquisa": {
        "nome": "Laboratórios de Pesquisa",
        "prioridade": 3,
        "subsistemas": {
            "botanica": {"status": True, "consumo": 8},
            "geologia": {"status": True, "consumo": 5}
        }
    },
    "conforto": {
        "nome": "Sistemas de Conforto",
        "prioridade": 1,
        "subsistemas": {
            "iluminacao_decorativa": {"status": True, "consumo": 5},
            "entretenimento": {"status": True, "consumo": 10}
        }
    }
}

