# SCIC: Sistema de Comunicação Interplanetária da Colônia

**Atividade Integradora · Fase 6 · Colônia Aurora Siger**

**Equipe:** AI Team

| Integrante | RM |
|---|---|
| Antuny Marques de Menezes | 572105 |
| Éric Yuiti Nissi | 573495 |
| Vinícius Pelogia do Nascimento | 572675 |

## Objetivo

O SCIC é um protótipo em Python que apoia a equipe da colônia **Aurora Siger** (Marte) na gestão da sua rede de comunicação. O sistema:

1. carrega e **limpa** uma base simulada com dados operacionais e de comunicação de 12 módulos ao longo de 30 ciclos (sóis);
2. calcula **indicadores** (potência P = V × I, eficiência Mbps/W, disponibilidade, latência média e máxima, consumo);
3. mede o **erro absoluto** e o **erro relativo** entre a latência prevista e a observada, e discute **ponto flutuante** e precisão;
4. simula a recuperação do enlace após uma tempestade de poeira com o **método de Euler**;
5. treina um **modelo de previsão de latência** e o avalia com **MAE, MSE, RMSE e R²**, comparando-o com um **baseline**, além de usar **Grid Search** e **AIC/BIC**;
6. **prioriza alertas** com um **max-heap** implementado do zero (heapify-up e heapify-down);
7. faz **buscas por prefixo** com uma **trie** (módulos, códigos de sensores e palavras-chave de alertas);
8. relaciona o sistema com **dispositivos de entrada e saída, bases numéricas** (hexadecimal, binário e decimal) e **eletricidade básica**;
9. oferece um **menu de navegação** e uma **análise final** de apoio à decisão.

## Arquivos da entrega

| Arquivo / pasta | Descrição |
|---|---|
| `notebook_projeto.ipynb` | **Arquivo principal do sistema.** Notebook com todo o código, comentários, gráficos e o menu |
| `dados_aurora_siger.csv` | Base de dados simulada (363 registros brutos, com defeitos inseridos de propósito para demonstrar a limpeza) |
| `gerar_dados_aurora_siger.py` | Script auxiliar que gerou a base simulada (semente fixa = 42, reprodutível). **Não é preciso executá-lo**, porque o CSV já está na pasta |
| `relatorio_tecnico.md` | Relatório técnico completo do projeto |
| `README.md` | Este arquivo |
| `link_video.txt` | Link do vídeo de apresentação no YouTube (não listado) |
| `graficos_ou_imagens/` | Gráficos gerados automaticamente pelo notebook |

## Dependências

Foram usadas **somente** as bibliotecas estudadas na fase e módulos da biblioteca padrão do Python:

| Biblioteca | Uso |
|---|---|
| `pandas` | Leitura, limpeza e agregação dos dados |
| `numpy` | Cálculos numéricos e demonstrações de ponto flutuante |
| `matplotlib` / `seaborn` | Gráficos |
| `scikit-learn` | Divisão treino/validação/teste, modelos (DummyRegressor, LinearRegression, DecisionTreeRegressor), GridSearchCV e métricas |
| Biblioteca padrão (`heapq`, `math`, `random`, `time`, `unicodedata`, `pathlib`) | Conferência do heap, cálculos, medição de tempo e normalização de texto |
| `jupyter` | Execução do notebook |

Versões usadas no desenvolvimento: Python 3.14, pandas 3.0, numpy 2.4, matplotlib 3.10, seaborn 0.13, scikit-learn 1.8. O código também deve funcionar com versões recentes anteriores (Python ≥ 3.10, pandas ≥ 2.0).

Instalação:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn notebook
```

## Como executar

1. Mantenha `notebook_projeto.ipynb` e `dados_aurora_siger.csv` **na mesma pasta**.
2. Abra o notebook no Jupyter (`jupyter notebook notebook_projeto.ipynb`), no VS Code ou no Google Colab. No Colab, faça o upload do CSV para a sessão.
3. Execute tudo: **Kernel → Restart & Run All** (no VS Code, **Run All**).
4. Os gráficos são salvos automaticamente em `graficos_ou_imagens/`.

### Menu interativo

A seção 10 do notebook tem o menu do SCIC. Por padrão, ele roda com **entradas pré-programadas**, para que a execução completa não fique parada esperando digitação. Para usá-lo de forma interativa, altere na última célula de código:

```python
MODO_INTERATIVO = True
```

e execute a célula. Opções disponíveis:

```
 1 - Carregar (recarregar) dados da colônia     7 - Analisar alertas de comunicação (heap)
 2 - Consultar registros de um módulo           8 - Buscar por prefixo (trie)
 3 - Ver painel de indicadores                  9 - Cadastrar novo alerta manual
 4 - Ver resumo dos erros numéricos            10 - Decodificar código de sensor (bases numéricas)
 5 - Executar previsão de latência             11 - Exibir análise final
 6 - Avaliar desempenho do modelo               0 - Sair
```

## Estrutura do notebook

| Seção | Conteúdo |
|---|---|
| 0 | Contexto da comunicação interplanetária e configuração |
| 1 | Leitura e limpeza dos dados |
| 2 | Análise exploratória |
| 3 | Indicadores operacionais e de comunicação |
| 4 | Erro absoluto, erro relativo e ponto flutuante |
| 5 | Simulação numérica (Euler) |
| 6 | Modelo de previsão e métricas |
| 7 | Priorização de alertas com heap |
| 8 | Busca por prefixo com trie |
| 9 | Dispositivos, bases numéricas e eletricidade |
| 10 | Sistema integrado e menu |
| 11 | Análise final, gerenciamento inteligente e reflexão social |
