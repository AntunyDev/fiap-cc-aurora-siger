# Aurora-Siger

Sistema de telemetria para verificação de decolagem de espaçonaves.

## Descrição do Projeto

Este projeto simula um sistema de monitoramento de telemetria para decidir se uma espaçonave está pronta para decolagem. Inclui leitura de dados, verificações de segurança, análise energética e consulta a IA para anomalias.

## Funcionalidades

- Visualização de dados de telemetria
- Atualização manual de dados
- Análise energética com cálculo de autonomia
- Verificação de segurança com decisão de decolagem
- Geração de relatório CSV
- Análise assistida por IA (Gemini)

## Pré-requisitos

- Python 3.x
- Bibliotecas: `tabulate`, `colorama`, `google-generativeai`
- Chave API do Google Gemini (configurada em function.py)

## Como Executar

1. Instale as dependências: `pip install tabulate colorama google-generativeai`
2. Execute o script principal: `python main.py`
3. Navegue pelo menu interativo.

## Prints de Execução

### Menu Principal
```
======== HUB - Pré-Decolagem ==========

[1] Visualizar dados Telemetria
[2] Atualizar dados Telemetria manualmente
[3] Executar Análise energética
[4] Executar verificação de segurança
[5] Gerar relatório de pré-decolagem em csv
[6] Consultar análise por IA
[0] Sair
```

### Exemplo de Visualização de Dados
```
+--------------------------------+----------------+
| Parâmetro                      | Valor          |
+================================+================+
| Temperatura Interna            | 35.5 °C        |
| Temperatura Externa            | 80.2 °C        |
| Integridade Estrutural         | 1 (0/1)        |
| Nivel Energia                  | 85.0 %         |
| Pressao Tanques                | 4500 kPa       |
| Status Modulos Criticos        | 1 (0/1)        |
| Nivel                          | 85.0 %         |
| Capacidade Total Kwh           | 500 kWh        |
| Consumo Decolagem Kwh          | 220 kWh        |
| Perdas Energeticas             | 8 %            |
+--------------------------------+----------------+
```

### Verificação de Segurança
```
Temperatura interna dentro do limite.
Temperatura externa dentro do limite.
Estrutura íntegra.
Pressão dos tanques adequada.
Módulos críticos operacionais.

STATUS FINAL: PRONTO PARA DECOLAR
```

## Estrutura do Projeto

- `main.py`: Script principal com menu interativo
- `data.py`: Dados de telemetria
- `function.py`: Funções auxiliares
- `aurora_siger.ipynb`: Notebook Jupyter com demonstração
- `relatorio_telemetria.csv`: Relatório gerado
