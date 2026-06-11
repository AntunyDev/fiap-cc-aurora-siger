# 🌌 Aurora Siger - Sistema Inteligente de Gerenciamento Colonial

Este sistema foi desenvolvido como projeto integrador da **Fase 3**, consolidando os conhecimentos de **Estrutura de Dados**, **Lógica de Programação** e **Modelagem Matemática (Regressão)** para simular o funcionamento autônomo e preditivo de uma colônia espacial.

---

## 🛠️ Tecnologias e Conceitos Aplicados

O projeto foi construído em **Python** utilizando apenas bibliotecas nativas, focando em:
1.  **Estruturas de Dados Hierárquicas:** Organização de sistemas e subsistemas em dicionários aninhados, permitindo navegação recursiva.
2.  **Lógica de Decisão por Prioridade:** Algoritmo que gerencia o consumo baseado na importância vital de cada setor (ex: Suporte à Vida vs. Entretenimento).
3.  **Regressão Linear (Mínimos Quadrados):** Implementação manual da fórmula matemática para previsão de geração de energia ($y = mx + b$).
4.  **Gestão de Fluxo Energético:** Sistema dinâmico de carga/descarga de baterias e controle de estabilidade da rede elétrica.

---

## 🚀 Funcionalidades Principais

- **Painel de Controle Interativo:** Interface via terminal que permite simular diferentes cenários climáticos.
- **Protocolo de Blackout:** Proteção automática que desliga sistemas não essenciais para preservar o suporte à vida quando a energia é crítica.
- **Restauração Inteligente:** Priorização da estabilidade da rede antes de iniciar o carregamento das reservas (Baterias).
- **Previsão Preditiva:** Estimativa de geração futura baseada em dados históricos de vento.

---

## 📂 Organização do Código

- `main.py`: Interface do usuário e coordenação central.
- `dados_colonia.py`: Base de dados e estado global da colônia.
- `regras_decisao.py`: Motor de decisão e navegação em árvores de sistemas.
- `modelo_previsao.py`: Módulo matemático para cálculos de regressão linear.
- `analise_energetica.py`: Lógica de transbordo de energia, bateria e estabilidade.

---

## 📈 Exemplo de Fluxo Operacional

1.  **Entrada:** Vento de 25 m/s detectado.
2.  **Ação:** O sistema gera superávit de energia.
3.  **Processamento:** A rede estabiliza em 100% e o excesso carrega a bateria.
4.  **Cenário de Crise:** Vento cai para 2 m/s. O sistema detecta o déficit, usa a reserva da bateria e, se necessário, desliga laboratórios de pesquisa para manter o oxigênio ligado.

---

## 📝 Como Executar

Certifique-se de ter o Python 3 instalado em sua máquina.

1. Navegue até a pasta do projeto:
   ```bash
   cd FASE_3_CC
   ```
2. Execute o programa:
   ```bash
   python main.py
   ```

---
*Desenvolvido para fins acadêmicos - FIAP 2026*
