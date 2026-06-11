# 🚀 Aurora Siger 

MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base

---

## 🛰️ Descrição do Projeto

Este projeto foi desenvolvido como parte da **Missão Aurora Siger**, com o objetivo de simular um sistema inteligente de controle de pouso de módulos em uma colônia em Marte.

---

## 🧠 Sobre o Projeto

O **MGPEB (Módulo de Gerenciamento de Pouso e Estabilização de Base)** funciona como uma **torre de controle orbital**, responsável por:

- 📌 Gerenciar o fluxo de módulos
- 📌 Priorizar pousos críticos
- 📌 Garantir segurança operacional
- 📌 Tomar decisões com base em dados de telemetria

O sistema simula um ambiente realista onde diferentes módulos competem por autorização de pouso com base em critérios técnicos.

---

## ✨ Funcionalidades

### 🔩 Modelagem de Módulos
Cada módulo possui atributos essenciais:

- 🌟 Combustível  
- 🌟 Massa  
- 🌟 Prioridade  
- 🌟 Criticidade  
- 🌟 Hora de chegada  
- 🌟 Status dos sensores  
- 🌟 Disponibilidade da área  

---

### 🎲 Estruturas de Dados

O sistema utiliza:

- **Fila (FIFO)** → gerenciamento da ordem de chegada  
- **Pilha (LIFO)** → controle de alertas  
- **Lista** → módulos já processados  

---

### 🧮 Algoritmos de Ordenação

Implementação manual de algoritmos clássicos:

- ⚠️ **Bubble Sort** → ordenação por prioridade  
- ⚠️ **Selection Sort** → ordenação por combustível  

---

### 🔍 Algoritmos de Busca

- 🔎 Busca linear por tipo  
- ⛽ Identificação do menor combustível  
- 🔤 Busca binária por nome  

---

### ⚙️ Lógica de Decisão

Sistema baseado em regras:

- ✅ **AUTORIZADO** → condições ideais  
- ⚠️ **ALERTA** → situação crítica controlada  
- ❌ **NEGADO** → risco elevado  

Utilizando operadores:

- `if`
- `and`
- `or`
- `not`


## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **colorama**
- **collections (deque)**

---

## ⚙️ Como Executar

## 1. Clone o repositório

git clone https://github.com/AntunyDev/Aurora-Siger-MGPEB.git

## 2. Baixar requisições 

pip install -r requirements.txt

## 3. Execute o arquivo main.py

py main.py

## 4. Vídeo Explicativo do Código / Algoritmo
https://youtu.be/vBuxA1uMLa0

