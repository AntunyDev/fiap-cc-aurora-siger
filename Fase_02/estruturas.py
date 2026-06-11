from collections import deque
from modulos import MODULOS_MISSAO

# 1. Fila de Espera - todos os módulos aguardando autorização
fila_espera = deque(MODULOS_MISSAO)

# 2. Fila de Pousados - inicia-se vazia
lista_pousados = []

# 3. Pilha de alertas - começa vazia (list normal serve, pois usaremos .append e .pop)
pilha_alerta = []