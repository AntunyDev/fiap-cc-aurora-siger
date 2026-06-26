<div align="center">

# 🚀 SIGIC — Aurora Siger
### Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FIAP](https://img.shields.io/badge/FIAP-Ciência%20da%20Computação-ED1C24?style=for-the-badge)](https://www.fiap.com.br/)
[![Fase](https://img.shields.io/badge/Fase-04-FF6B35?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Operacional-00C851?style=for-the-badge)]()

> **Computacionalmente modelando a infraestrutura de uma colônia marciana para garantir a sobrevivência da Aurora Siger.**

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Infraestrutura da Colônia](#-infraestrutura-da-colônia)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Estruturas de Dados](#-estruturas-de-dados)
- [Algoritmos Implementados](#-algoritmos-implementados)
- [Modelagem Matemática](#-modelagem-matemática)
- [Sustentabilidade e Governança ESG](#-sustentabilidade-e-governança-esg)
- [Como Executar](#-como-executar)
- [Funcionalidades do Menu](#-funcionalidades-do-menu)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)

---

## 🌌 Sobre o Projeto

O **SIGIC** (Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia) é o cérebro computacional da **Aurora Siger**, uma base marciana fictícia desenvolvida como projeto integrador da Fase 04 do curso de Ciência da Computação da FIAP.

O sistema foi construído inteiramente em Python puro — sem dependências externas — e integra conceitos de:

| Disciplina | Aplicação no Projeto |
|---|---|
| **Grafos e Algoritmos de Redes** | Modelagem da infraestrutura como grafo ponderado |
| **BFS / DFS / Dijkstra** | Exploração e otimização de rotas entre módulos |
| **Estruturas de Dados** | Listas, matrizes, tuplas e dicionários |
| **Modelagem Matemática** | Fórmula de energia necessária por rota |
| **Otimização Computacional** | Roteamento por menor perda energética |
| **Smart Grids / ESG** | Governança e sustentabilidade da rede energética |

---

## 🏗️ Infraestrutura da Colônia

A Aurora Siger é composta por **8 módulos** interligados em uma rede energética gerenciada pelo SIGIC:

| Sigla | Módulo | Prioridade | Consumo (u/h) | Status |
|:---:|---|:---:|:---:|:---:|
| `HAB` | Habitação | 10 | 42 | 🟢 Ativo |
| `CTL` | Centro de Controle | 10 | 36 | 🟢 Ativo |
| `ENE` | Armazenamento de Energia | 9 | 14 | 🟢 Ativo |
| `AGR` | Agricultura | 7 | 48 | 🟢 Ativo |
| `LAB` | Laboratório Científico | 5 | 32 | 🟡 Manutenção |
| `COM` | Comunicação | 8 | 28 | 🟢 Ativo |
| `MED` | Suporte Médico | 9 | 30 | 🔴 Alerta |
| `OXI` | Produção de Oxigênio | 10 | 52 | 🟢 Ativo |

### Topologia da Rede

```
ENE ──2.0km──▶ CTL ──1.2km──▶ COM ──1.7km──▶ LAB
 │                                              │
1.8km          2.4km                            │
 │              └──────────────────────────────►┘
 ▼
OXI ◄──2.2km── AGR ◄──3.1km── HAB ──0.9km──▶ MED
 ▲                                              │
 └──────────────────────────────────────────────┘
                                              1.6km
```

> Cada aresta possui dois pesos: **distância (km)** e **perda energética (%)**.
> O módulo `ENE` funciona como hub central de distribuição de energia.

**Justificativa da topologia:**
- `ENE`, `CTL` e `OXI` ficam mais centrais por serem sistemas críticos de sobrevivência.
- `HAB` se conecta diretamente a `MED` para minimizar o tempo de resposta médica.
- `AGR` fica ligada a `HAB` e `OXI` por depender de ar, água e suporte humano.
- `COM` possui redundância com `CTL`, `LAB` e `OXI` para garantir comunicação mesmo em falhas.

---

## 🏛️ Arquitetura do Sistema

```
Fase_04/
│
├── codigo_fonte.py          # Ponto de entrada — executa menu_principal()
│
└── sigic/                   # Pacote principal do SIGIC
    ├── __init__.py          # Inicialização do pacote
    ├── dados.py             # Dados dos módulos e conexões (MODULOS + CONEXOES)
    ├── grafo.py             # Montagem do grafo — lista e matriz de adjacência
    ├── algoritmos.py        # BFS, DFS e Dijkstra
    ├── simulacao.py         # Modelagem matemática, simulações e indicadores
    └── interface.py         # Menu de terminal e exibição dos resultados
```

### Fluxo de dados

```
dados.py (MODULOS + CONEXOES)
       │
       ▼
grafo.py (montar_lista_adjacencia / montar_matriz_adjacencia)
       │
       ├──▶ algoritmos.py (BFS / DFS / Dijkstra)
       │
       └──▶ simulacao.py (modelagem, conexões críticas, indicadores)
                    │
                    ▼
             interface.py (menu_principal → exibe resultados ao usuário)
                    │
                    ▼
             codigo_fonte.py (entry point)
```

---

## 🗃️ Estruturas de Dados

O SIGIC utiliza as quatro estruturas fundamentais estudadas, cada uma com sua justificativa:

### 📌 Dicionários — `MODULOS` e `GRAFO`
```python
MODULOS = {
    "HAB": {"nome": "Habitacao", "consumo": 42, "prioridade": 10, ...},
    "ENE": {"nome": "Armazenamento de Energia", "consumo": 14, ...},
    ...
}
```
> **Justificativa:** Acesso O(1) por chave (sigla do módulo), ideal para consulta rápida de atributos em um sistema com muitos nós.

### 📌 Tuplas — `CONEXOES`
```python
CONEXOES = [
    ("ENE", "CTL", 2.0, 3.0),  # (origem, destino, distancia_km, perda_%)
    ("HAB", "MED", 0.9, 1.0),
    ...
]
```
> **Justificativa:** Dados de conexão são imutáveis por definição — tuplas garantem integridade e semântica posicional clara.

### 📌 Listas — Adjacência, caminhos e visitados
```python
GRAFO = {
    "ENE": [("CTL", 2.0, 3.0), ("HAB", 2.5, 4.0), ("OXI", 1.8, 2.5)],
    ...
}
visitados = []  # usado em BFS e DFS
caminho   = []  # reconstrução do caminho no Dijkstra
```
> **Justificativa:** Estrutura dinâmica para percurso sequencial de nós durante busca e reconstrução de rotas.

### 📌 Matrizes (Lista de Listas) — Adjacência ponderada
```python
matriz = [[0, 2.0, 0, ...],   # ENE → CTL = 2.0 km
          [2.0, 0, 1.2, ...], # CTL → COM = 1.2 km
          ...]
```
> **Justificativa:** Representação tabular das distâncias entre módulos — facilita visualização e análise de densidade da rede.

---

## ⚙️ Algoritmos Implementados

### 🔍 BFS — Busca em Largura
Explora a rede nível a nível a partir de um módulo de origem. Útil para identificar todos os módulos alcançáveis e a ordem de cobertura da rede.

```
Origem: ENE
BFS → ENE → CTL → HAB → OXI → COM → MED → LAB → AGR
```

### 🔍 DFS — Busca em Profundidade
Explora cada ramificação até o fim antes de retroceder. Útil para detectar componentes conexos e caminhos alternativos.

```
Origem: ENE
DFS → ENE → CTL → COM → LAB → OXI → AGR → HAB → MED
```

### 🎯 Dijkstra — Caminho Mínimo
Encontra a rota de menor custo entre dois módulos quaisquer. O SIGIC suporta dois critérios de otimização:

| Critério | Objetivo |
|---|---|
| `distancia` | Minimizar km percorridos |
| `perda` | Minimizar desperdício energético |

**Exemplo — Menor perda de ENE até MED:**
```
ENE → HAB → MED  |  Distância: 3.4 km  |  Perda: 5.0%
```

### 🔴 Detecção de Conexões Críticas
Remove arestas uma a uma e verifica se a rede se fragmenta (aumento de componentes conexos). Conexões entre módulos de prioridade ≥ 9 também são marcadas como críticas.

---

## 📐 Modelagem Matemática

### Fórmula de Energia Necessária por Rota

$$E(d, p) = D \cdot \left(1 + \frac{p}{100}\right) + 0{,}8 \cdot d$$

| Variável | Significado |
|---|---|
| `D` | Demanda energética base do módulo destino (u/h) |
| `p` | Perda energética acumulada ao longo da rota (%) |
| `d` | Distância total percorrida na rota (km) |
| `E` | Energia total necessária a ser fornecida (u/h) |

### Análise Qualitativa

- A função **cresce monotonicamente** com `d` e `p`, confirmando que rotas mais longas e com maior perda exigem mais energia bruta.
- O termo `D · (p/100)` representa a **compensação por perda em trânsito** — quanto maior a perda, mais energia precisa ser injetada na origem.
- O fator `0,8 · d` representa a **resistência de percurso** — cabo mais longo dissipa mais calor.
- O critério de otimização do Dijkstra por perda mínima é o que **minimiza diretamente `E`**, reduzindo o desperdício operacional.

### Índice de Eficiência Global

```
Eficiência = 100 - (perda_média × 8) - (consumo_total / armazenamento_total × 10)
```

---

## 🌱 Sustentabilidade e Governança ESG

O SIGIC incorpora princípios **ESG (Environmental, Social and Governance)** no gerenciamento da colônia:

### ♻️ Environmental — Uso Sustentável de Energia
- Monitoramento contínuo de perdas por conexão
- Priorização de rotas com menor desperdício energético
- Desligamento automático de cargas não essenciais em modo de alerta

### 👥 Social — Priorização de Sistemas Críticos
- Habitação, Oxigênio, Energia e Suporte Médico recebem **prioridade máxima (9-10)**
- O algoritmo garante fornecimento para módulos críticos mesmo em restrição de energia
- Módulos em alerta (`MED`) recebem atenção operacional diferenciada

### 🏛️ Governance — Governança Tecnológica
- Toda decisão automatizada registra o **critério utilizado** (distância, perda ou prioridade)
- Expansão da colônia deve seguir protocolo: novos módulos conectados a `CTL`, `ENE` ou `OXI` com redundância
- Conexões críticas identificadas e documentadas para planejamento de rotas alternativas

---

## ▶️ Como Executar

### Pré-requisitos
- Python **3.10** ou superior
- Sem bibliotecas externas — apenas stdlib Python (`collections`, `heapq`, `os`)

### Execução

```bash
# Clone ou extraia o projeto na pasta desejada
# Navegue até a pasta raiz Fase_04/

python codigo_fonte.py
```

### Exemplo de saída

```
========================================================================
                          SIGIC - AURORA SIGER
    Sistema Inteligente de Gerenciamento da Infraestrutura da Colonia
========================================================================

1. Visualizar rede da colonia
2. Listar modulos
3. Consultar modulo
4. Executar BFS, DFS e Dijkstra
5. Simular distribuicao de energia
6. Detectar conexoes criticas
7. Analisar eficiencia e modelagem matematica
8. Sustentabilidade e governanca ESG
0. Sair

Escolha uma opcao:
```

---

## 🖥️ Funcionalidades do Menu

| Opção | Funcionalidade | Algoritmo / Módulo |
|:---:|---|---|
| `1` | Visualizar rede — lista de adjacência + matriz de distâncias + justificativa | `grafo.py` |
| `2` | Listar todos os módulos com consumo, prioridade e status | `dados.py` |
| `3` | Consultar módulo específico com todos os atributos e conexões | `interface.py` |
| `4` | Executar BFS, DFS e Dijkstra entre dois módulos escolhidos | `algoritmos.py` |
| `5` | Simular distribuição de energia de ENE até módulo alvo | `simulacao.py` |
| `6` | Detectar conexões críticas que fragmentariam a rede | `simulacao.py` |
| `7` | Analisar eficiência operacional + modelagem matemática | `simulacao.py` |
| `8` | Exibir análise de sustentabilidade e governança ESG | `interface.py` |
| `0` | Sair do sistema | — |

---

## 📁 Estrutura de Arquivos

```text
Fase_04/
├── codigo_fonte.py              # Arquivo principal de execução
├── README.md                    # Documentação do projeto
├── sigic/                       # Pacote principal do sistema
│   ├── __init__.py              # Inicialização do pacote
│   ├── dados.py                 # Dados dos módulos e conexões
│   ├── grafo.py                 # Lista e matriz de adjacência
│   ├── algoritmos.py            # BFS, DFS e Dijkstra
│   ├── simulacao.py             # Modelagens, indicadores e simulações
│   └── interface.py             # Menu e interação no terminal
└── scripts/                     # Scripts auxiliares opcionais
    └── gerar_rede_pdf.py        # Gera rede_colonia.pdf quando necessário
```

Arquivos como `rede_colonia.pdf`, `documentacao_complementar.pdf`, `.zip`, `__pycache__/` e ambientes virtuais são artefatos gerados localmente e ficam fora do versionamento pelo `.gitignore`.

---

## Vídeo Explicativo do Código / Algoritmo
https://youtu.be/Q0DMWrPxRoA

---

<div align="center">

**🚀 Aurora Siger — Onde a tecnologia encontra Marte**

*Desenvolvido com Python • Sem dependências externas • FIAP 2026*

</div>

