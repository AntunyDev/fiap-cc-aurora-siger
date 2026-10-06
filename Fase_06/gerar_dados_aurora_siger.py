"""
Gerador da base de dados SIMULADA da colônia Aurora Siger.

Este script NÃO é o sistema principal (o sistema é o notebook_projeto.ipynb).
Ele existe apenas para mostrar, de forma transparente, como a base
dados_aurora_siger.csv foi criada. Rodá-lo novamente gera exatamente a
mesma base, porque usamos uma semente aleatória fixa (SEED).

Como a base foi pensada:
- 12 módulos da colônia, cada um registrado em 30 ciclos (1 ciclo = 1 sol,
  o "dia marciano" de aproximadamente 24h39min);
- Entre os ciclos 12 e 16 acontece uma tempestade de poeira, que derruba a
  qualidade do sinal e a tensão dos painéis solares e aumenta a latência;
- A coluna latencia_prevista_ms é a estimativa da fórmula antiga da colônia,
  que NÃO leva em conta tempestades e picos. Por isso ela erra mais nesses
  momentos, e é isso que o SCIC vai analisar;
- Alguns "defeitos" foram inseridos de propósito (valores faltantes,
  linhas duplicadas e textos com maiúsculas e espaços inconsistentes) para
  demonstrar a etapa de limpeza de dados no notebook.

Execução:  python gerar_dados_aurora_siger.py
"""

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_CICLOS = 30
CICLOS_TEMPESTADE = range(12, 17)          # ciclos 12 a 16
HORAS_POR_SOL = 24.65                      # duração aproximada de 1 sol
DATA_INICIAL = date(2026, 9, 1)            # data terrestre de referência

# Cada módulo: nome, tipo, código do sensor (hexadecimal), prioridade base (1 a 5),
# latência base em ms, tensão nominal da alimentação (V), corrente base (A)
# e faixa de tráfego de dados (Mbps).
#
# Estrutura do código do sensor: 0xTMSS
#   T  = 1 dígito hex para o tipo do módulo
#   M  = 1 dígito hex para o número do módulo dentro do tipo
#   SS = 2 dígitos hex para o número do sensor
MODULOS = [
    ("Habitação Alfa",          "habitação",              "0x110A", 3,  40, 24, 1.8, (5, 25)),
    ("Habitação Beta",          "habitação",              "0x120B", 3,  45, 24, 1.7, (5, 25)),
    ("Agricultura Hidropônica", "agricultura",            "0x2103", 4,  60, 24, 2.2, (3, 15)),
    ("Comunicação Central",     "comunicação",            "0x310A", 5,  25, 48, 3.5, (40, 120)),
    ("Comunicação Orbital",     "comunicação",            "0x32F1", 5, 180, 48, 4.2, (30, 90)),
    ("Laboratório Geológico",   "laboratório",            "0x4107", 2,  70, 24, 1.5, (8, 35)),
    ("Laboratório Biológico",   "laboratório",            "0x4208", 2,  65, 24, 1.6, (8, 35)),
    ("Suporte Médico",          "suporte médico",         "0x51C2", 5,  30, 24, 2.0, (10, 40)),
    ("Armazenamento de Dados",  "armazenamento de dados", "0x61D4", 4,  35, 24, 2.6, (20, 80)),
    ("Energia Solar",           "energia",                "0x7105", 5,  55, 24, 1.2, (2, 10)),
    ("Comando Principal",       "comando",                "0x81A0", 5,  20, 12, 2.5, (15, 60)),
    ("Controle Ambiental",      "controle",               "0x82B3", 5,  30, 12, 2.1, (5, 30)),
]

MSG_ALERTA_TEMPESTADE = "Perda parcial de sinal durante tempestade de poeira"
MSG_ALERTA_PICO = "Pico de latência detectado no enlace"
MSG_ALERTA_LATENCIA = "Latência acima do limite previsto"
MSG_ALERTA_TENSAO = "Queda de tensão na alimentação do transmissor"
MSG_MANUTENCAO = ["Manutenção preventiva programada", "Recalibração do sensor de sinal"]


def gerar_base(rng: np.random.Generator) -> pd.DataFrame:
    """Gera os registros dos 12 módulos ao longo dos 30 ciclos."""
    registros = []
    for ciclo in range(1, N_CICLOS + 1):
        tempestade = 1 if ciclo in CICLOS_TEMPESTADE else 0
        for (nome, tipo, codigo, prioridade, lat_base, v_nom, i_base, faixa) in MODULOS:
            # Tráfego de dados do módulo no ciclo (Mbps)
            carga = rng.uniform(*faixa)

            # Qualidade do sinal (%): cai durante a tempestade; o enlace orbital sofre mais
            qualidade = rng.normal(93, 2.5)
            if tempestade:
                queda = rng.uniform(12, 22) * (1.5 if nome == "Comunicação Orbital" else 1.0)
                qualidade -= queda
            qualidade = float(np.clip(qualidade, 40, 100))

            # Temperatura do equipamento de comunicação (°C)
            temperatura = rng.normal(27, 4)

            # Latência "real" (observada): depende da carga, do sinal, da tempestade e do calor
            lat_real = (lat_base * (1 + 0.004 * carga)
                        + 1.2 * (100 - qualidade)
                        + tempestade * (0.35 * lat_base + 25)
                        + 0.8 * max(0.0, temperatura - 30)
                        + rng.normal(0, 0.06 * lat_base))
            pico = rng.random() < 0.04            # 4% de chance de pico/falha momentânea
            if pico:
                lat_real += rng.uniform(80, 200)

            # Latência prevista pela fórmula antiga (não considera tempestade nem picos)
            lat_prevista = lat_base * (1 + 0.004 * carga) + 1.2 * (100 - 93)

            # Alimentação elétrica: tensão cai na tempestade (menos geração solar)
            tensao = rng.normal(v_nom, 0.015 * v_nom) * (rng.uniform(0.91, 0.95) if tempestade else 1.0)
            corrente = i_base + 0.02 * carga + rng.normal(0, 0.05)
            fator_uso = rng.uniform(0.65, 0.80)   # fração do sol em que o equipamento opera em carga
            consumo_kwh = tensao * corrente * HORAS_POR_SOL * fator_uso / 1000

            # Status operacional e mensagem de alerta
            erro_rel = abs(lat_real - lat_prevista) / lat_real
            if pico:
                status, msg = "alerta", MSG_ALERTA_PICO
            elif tempestade and qualidade < 75:
                status, msg = "alerta", MSG_ALERTA_TEMPESTADE
            elif erro_rel > 0.35:
                status, msg = "alerta", MSG_ALERTA_LATENCIA
            elif tensao < 0.93 * v_nom:
                status, msg = "alerta", MSG_ALERTA_TENSAO
            elif rng.random() < 0.04:
                status, msg = "manutenção", str(rng.choice(MSG_MANUTENCAO))
            else:
                status, msg = "ativo", "Sem alerta"

            registros.append({
                "ciclo": ciclo,
                "data_registro": (DATA_INICIAL + timedelta(days=ciclo - 1)).isoformat(),
                "modulo": nome,
                "tipo_modulo": tipo,
                "codigo_sensor": codigo,
                "nivel_prioridade": prioridade,
                "carga_trafego_mbps": round(carga, 2),
                "qualidade_sinal_pct": round(qualidade, 1),
                "temperatura_equip_c": round(temperatura, 1),
                "tempestade_poeira": tempestade,
                "latencia_prevista_ms": round(lat_prevista, 1),
                "latencia_observada_ms": round(lat_real, 1),
                "tensao_v": round(tensao, 2),
                "corrente_a": round(corrente, 2),
                "consumo_kwh": round(consumo_kwh, 3),
                "status_operacional": status,
                "mensagem_alerta": msg,
            })
    return pd.DataFrame(registros)


def inserir_imperfeicoes(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Insere defeitos típicos de dados reais para demonstrar a limpeza no notebook."""
    df = df.copy()
    # 1) Valores faltantes na latência observada (falha de leitura do sensor)
    idx_nan = rng.choice(df.index, size=6, replace=False)
    df.loc[idx_nan, "latencia_observada_ms"] = np.nan
    # 2) Status escritos de forma inconsistente (maiúsculas e espaços extras)
    idx_txt = rng.choice(df.index, size=8, replace=False)
    df.loc[idx_txt, "status_operacional"] = df.loc[idx_txt, "status_operacional"].map(
        lambda s: rng.choice([s.upper(), f" {s.capitalize()} "]))
    # 3) Linhas duplicadas (o mesmo registro enviado duas vezes pela rede)
    duplicadas = df.sample(3, random_state=SEED)
    df = pd.concat([df, duplicadas]).sort_values(["ciclo", "modulo"], kind="stable")
    return df.reset_index(drop=True)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    base = inserir_imperfeicoes(gerar_base(rng), rng)
    destino = Path(__file__).parent / "dados_aurora_siger.csv"
    base.to_csv(destino, index=False, encoding="utf-8")
    print(f"Base gerada com {len(base)} registros em: {destino}")
