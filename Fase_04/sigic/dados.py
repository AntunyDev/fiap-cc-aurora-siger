"""
Dados centrais da colonia Aurora Siger.

Estruturas usadas:
- Dicionarios para organizar atributos dos modulos por chave.
- Tuplas para representar conexoes fixas entre vertices da rede.
"""


MODULOS = {
    "HAB": {
        "nome": "Habitacao",
        "consumo": 42,
        "prioridade": 10,
        "armazenamento": 18,
        "comunicacao": "Alta",
        "status": "ativo",
        "descricao": "Acomodacao da tripulacao e suporte basico de sobrevivencia.",
    },
    "CTL": {
        "nome": "Centro de Controle",
        "consumo": 36,
        "prioridade": 10,
        "armazenamento": 12,
        "comunicacao": "Muito alta",
        "status": "ativo",
        "descricao": "Monitoramento e gerenciamento operacional da colonia.",
    },
    "ENE": {
        "nome": "Armazenamento de Energia",
        "consumo": 14,
        "prioridade": 9,
        "armazenamento": 220,
        "comunicacao": "Alta",
        "status": "ativo",
        "descricao": "Baterias e distribuicao inteligente de energia.",
    },
    "AGR": {
        "nome": "Agricultura",
        "consumo": 48,
        "prioridade": 7,
        "armazenamento": 70,
        "comunicacao": "Media",
        "status": "ativo",
        "descricao": "Cultivo de alimentos e reciclagem parcial de recursos.",
    },
    "LAB": {
        "nome": "Laboratorio Cientifico",
        "consumo": 32,
        "prioridade": 5,
        "armazenamento": 25,
        "comunicacao": "Media",
        "status": "manutencao",
        "descricao": "Pesquisas de materiais, solo e condicoes marcianas.",
    },
    "COM": {
        "nome": "Comunicacao",
        "consumo": 28,
        "prioridade": 8,
        "armazenamento": 10,
        "comunicacao": "Muito alta",
        "status": "ativo",
        "descricao": "Troca de dados entre modulos e contato com a Terra.",
    },
    "MED": {
        "nome": "Suporte Medico",
        "consumo": 30,
        "prioridade": 9,
        "armazenamento": 35,
        "comunicacao": "Alta",
        "status": "alerta",
        "descricao": "Atendimento medico e monitoramento da saude da tripulacao.",
    },
    "OXI": {
        "nome": "Producao de Oxigenio",
        "consumo": 52,
        "prioridade": 10,
        "armazenamento": 95,
        "comunicacao": "Alta",
        "status": "ativo",
        "descricao": "Geracao e distribuicao de oxigenio para a base.",
    },
}


# Formato: (origem, destino, distancia_km, perda_percentual).
CONEXOES = [
    ("ENE", "CTL", 2.0, 3.0),
    ("ENE", "HAB", 2.5, 4.0),
    ("ENE", "OXI", 1.8, 2.5),
    ("CTL", "COM", 1.2, 1.5),
    ("CTL", "LAB", 2.4, 3.8),
    ("HAB", "MED", 0.9, 1.0),
    ("HAB", "AGR", 3.1, 5.2),
    ("AGR", "OXI", 2.2, 3.5),
    ("LAB", "COM", 1.7, 2.2),
    ("MED", "OXI", 1.6, 2.0),
    ("COM", "OXI", 2.9, 4.8),
]
