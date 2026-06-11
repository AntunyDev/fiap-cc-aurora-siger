# modelo_previsao.py

import matplotlib.pyplot as plt
from dados_colonia import historico_clima

def treinar_modelo():
    """
    Calcula a Regressão Linear (y = mx + b) usando o método dos Mínimos Quadrados.
    Executa a extração dos dados históricos uma única vez.
    """
    x = historico_clima["vento"]
    y = historico_clima["energia"]
    n = len(x)

    # Cálculos necessários para a fórmula
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(val_x * val_y for val_x, val_y in zip(x, y))
    sum_x_quad = sum(val_x**2 for val_x in x)

    # Cálculo da Inclinação (m) e Intercepto (b)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_quad - sum_x**2)
    b = (sum_y - m * sum_x) / n

    return m, b

def prever_energia(vento_futuro):
    """Realiza a estimativa baseada na reta ajustada e aciona o gráfico."""
    m, b = treinar_modelo()
    previsao = (m * vento_futuro) + b
    previsao = max(0, previsao)

    print(f"\n--- MODELO DE PREVISÃO ENERGÉTICA ---")
    print(f"Equação da Reta Ajustada: y = {m:.2f}x + {b:.2f}")
    print(f"Entrada (Vento): {vento_futuro} m/s")
    print(f"Saída (Energia Estimada): {previsao:.2f} unidades")
    
    # CHAMA O GRÁFICO: Passa apenas o ponto que o usuário quer destacar!
    gerar_grafico_regressao(vento_futuro, previsao)
    
    return previsao

def gerar_grafico_regressao(vento_usuario, previsao_usuario):
    """Gera e salva o gráfico aproveitando os dados e cálculos existentes."""
    x = historico_clima["vento"]
    y = historico_clima["energia"]
    m, b = treinar_modelo()
    
    # Gera os pontos da linha azul de regressão
    energia_prevista = [m * val_x + b for val_x in x]
    
    # Monta o gráfico do Matplotlib
    plt.scatter(x, y, color='#e74c3c', zorder=4, label='Dados Históricos (NASA MEDA)')
    plt.plot(x, energia_prevista, color='#2980b9', linestyle='--', linewidth=2, label=f'Reta: y = {m:.2f}x + ({b:.2f})')
    
    # Destaca a velocidade do vento inputada pelo usuário com um ponto amarelo grande
    plt.scatter(vento_usuario, previsao_usuario, color='#f1c40f', edgecolors='black', 
                s=200, marker='o', zorder=5, label=f'Sua Previsão ({vento_usuario} m/s)')
    
    plt.title('Previsão: Velocidade do Vento vs Geração em Marte', fontsize=12, pad=15)
    plt.xlabel('Velocidade do Vento (m/s)', fontsize=10)
    plt.ylabel('Potência Estimada da Turbina (unidades)', fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')

    print(f"Aqui temos o gráfico destacando o ponto da velocidade atual.")
    plt.show()

    # Salva o gráfico de regressão
    nome_arquivo = 'grafico_regressao_marte.png'
    plt.savefig(nome_arquivo, bbox_inches='tight', dpi=300)
    plt.close() 
    

    