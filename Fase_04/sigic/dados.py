"""
Dados centrais da colonia Aurora Siger.

Estruturas de dados utilizadas e justificativas:
- Dicionarios (MODULOS): acesso O(1) por sigla do modulo, ideal para
  consultas rapidas durante execucao dos algoritmos de rede.
- Listas de tuplas (CONEXOES): conexoes sao imutaveis por natureza;
  tuplas garantem integridade dos dados e semântica posicional clara.
"""


# -------------------------------------------------------------------------
# MODULOS: dicionario que mapeia a sigla de cada modulo a seus atributos.
# Cada chave e uma string de 3 letras (sigla unica do modulo).
# Cada valor e um dicionario com os dados operacionais do modulo.
# -------------------------------------------------------------------------
MODULOS = {
    # --- Habitacao ---
    # Prioridade maxima: sem ela, a tripulacao nao sobrevive.
    "HAB": {
        "nome": "Habitacao",
        "consumo": 42,          # unidades de energia por hora
        "prioridade": 10,       # escala 1-10; 10 = missao critica
        "armazenamento": 18,    # capacidade de recursos locais (unidades)
        "comunicacao": "Alta",  # frequencia de troca de dados com outros modulos
        "status": "ativo",      # situacao: ativo | manutencao | alerta
        "descricao": "Acomodacao da tripulacao e suporte basico de sobrevivencia.",
    },
    # --- Centro de Controle ---
    # Cerebro da operacao: coordena todos os outros modulos.
    "CTL": {
        "nome": "Centro de Controle",
        "consumo": 36,
        "prioridade": 10,
        "armazenamento": 12,
        "comunicacao": "Muito alta",  # maior frequencia de dados da rede
        "status": "ativo",
        "descricao": "Monitoramento e gerenciamento operacional da colonia.",
    },
    # --- Armazenamento de Energia ---
    # Hub central de distribuicao: maior capacidade de armazenamento da rede.
    # Ponto de origem para todas as simulacoes de envio de energia.
    "ENE": {
        "nome": "Armazenamento de Energia",
        "consumo": 14,          # baixo consumo proprio; foca em distribuir
        "prioridade": 9,
        "armazenamento": 220,   # maior reserva de energia da colonia
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
}  # fim de MODULOS


# -------------------------------------------------------------------------
# CONEXOES: lista de tuplas representando as arestas do grafo.
# Cada tupla contem: (origem, destino, distancia_km, perda_percentual)
# - origem / destino : siglas dos modulos conectados (vertice -> vertice)
# - distancia_km     : peso primario da aresta (km entre os modulos)
# - perda_percentual : perda energetica ao transmitir pela conexao (%)
# O grafo e nao-dirigido: cada aresta e valida nos dois sentidos.
# -------------------------------------------------------------------------
CONEXOES = [
    ("ENE", "CTL", 2.0, 3.0),  # hub de energia -> controle central
    ("ENE", "HAB", 2.5, 4.0),  # energia -> habitacao (rota de sobrevivencia)
    ("ENE", "OXI", 1.8, 2.5),  # energia -> oxigenio (rota mais curta e critica)
    ("CTL", "COM", 1.2, 1.5),  # controle -> comunicacao (menor perda da rede)
    ("CTL", "LAB", 2.4, 3.8),  # controle -> laboratorio
    ("HAB", "MED", 0.9, 1.0),  # habitacao -> medico (menor distancia; resposta rapida)
    ("HAB", "AGR", 3.1, 5.2),  # habitacao -> agricultura (maior perda da rede)
    ("AGR", "OXI", 2.2, 3.5),  # agricultura <-> oxigenio (ciclo de ar e agua)
    ("LAB", "COM", 1.7, 2.2),  # laboratorio -> comunicacao (envio de dados)
    ("MED", "OXI", 1.6, 2.0),  # medico <-> oxigenio (suporte vital direto)
    ("COM", "OXI", 2.9, 4.8),  # comunicacao -> oxigenio (redundancia de rede)
]
