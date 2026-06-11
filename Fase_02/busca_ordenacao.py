from collections import deque
from modulos import MODULOS_MISSAO

# 1. Busca linear — acha módulo por tipo
def buscar_por_tipo(fila, tipo):
    encontrados = []
    for m in fila:
        if m["tipo"] == tipo:
            encontrados.append(m)
    return encontrados
    
# 2. Busca linear — acha o módulo com menor combustível
def buscar_menor_combustivel(fila):
    menor = fila[0]  

    for m in fila:   
        if m["combustivel"] < menor["combustivel"]:
            menor = m  
    return menor

# 3. Ordenação - Ordenar Lista de módulos por nome para utilizar a Busca Binária
def ordenar_lista(lista):
    lista_ordenada = sorted(lista, key=lambda m: m["nome"])
    return lista_ordenada
    
# 4. Busca binária - acha o módulo pelo nome
def buscar_por_nome(lista_ordenada, nome):
    inicio = 0
    fim = len(lista_ordenada) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        nome_meio = lista_ordenada[meio]["nome"]

        if nome_meio == nome:
            return lista_ordenada[meio]   # achou!
        elif nome < nome_meio:
            fim = meio - 1               # descarta metade direita
        else:
            inicio = meio + 1            # descarta metade esquerda

    return None  # não encontrou

# 5. Ordenação - prioridade
def bubble_sort_prioridade(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["prioridade"] > lista[j+1]["prioridade"]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

# 6. Ordenação - menor combustível
def selection_sort_combustivel(lista):
    n = len(lista)
    for i in range(n):
        idx_menor = i
        for j in range(i+1, n):
            if lista[j]["combustivel"] < lista[idx_menor]["combustivel"]:
                idx_menor = j
        lista[i], lista[idx_menor] = lista[idx_menor], lista[i]
    return lista

