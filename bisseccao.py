
import math
import matplotlib.pyplot as plt

#Calcula f(R) para encontrar a resistência desejada
def funcao(R, L, C, t):

    #varifica se o valor dentro da raiz é positivo
    discriminante = 1 / (L * C) - (R / (2 * L)) ** 2
    if discriminante < 0: 
        raise ValueError("Discriminante negativo.")
    w = math.sqrt(discriminante)

    #retorna a função do problema
    return math.exp(-R * t / (2 * L)) * math.cos(w * t) - 0.01

#Encontra a raiz utilizando o método da bisseção.
def bissecao(inicio, fim, L, C, t, tolerancia):

    #Calcula se os intervalos definidos são validos
    f_inicio = funcao(inicio, L, C, t)
    f_fim = funcao(fim, L, C, t)

    if f_inicio * f_fim > 0: #f(inicial)*f(final) pracisa ser negativo. Se for postivo retorna intervalo invalido.
        raise ValueError("O intervalo não contém uma raiz garantida.")

    print("\n--- MÉTODO DA BISSEÇÃO ---")
    
    print(
        f"{'iteracao':^5} | "
        f"{'inicio':^12} | "
        f"{'fim':^12} | "
        f"{'R':^12} | "
        f"{'f(inicio)':^12} | "
        f"{'f(fim)':^12} | "
        f"{'f(R)':^12} | "
        f"{'Erro%':^12} | "
    )

    """Espera-se um erro menor ou igual o erro de tolerancia definido. 
    Enquanto o erro for maior que a tolerancia, continua o loop"""
    iteracao = 0
    erro_calculado = 100
    while erro_calculado > tolerancia:

        meio = (inicio + fim) / 2 #Calcula um valor canditado a ser raiz 
        f_meio = funcao(meio, L, C, t) #Calcula a função para o valor
        
        if iteracao != 0: # a primeira iteração nao possui calculo de erro. O erro aparece da segunda em diante
            erro_calculado = abs(((meio_antigo-meio)/meio_antigo)*100)

        iteracao += 1

        print(
            f"{iteracao:^8} | "
            f"{inicio:^12.6f} | "
            f"{fim:^12.6f} | "
            f"{meio:^12.6f} | "
            f"{f_inicio:^12.8f} | "
            f"{f_fim:^12.8f} | "
            f"{f_meio:^12.8f} | "
            f"{erro_calculado:^12.8f} | "
        )

        #Se f(R) for zero, adotamos o valor atual de R como raiz
        if f_meio == 0:
            return meio, iteracao

        #No intervalo [a,b], se f(a)*f(m) < 0, o intevalo passa a ser [a,m]
        if f_inicio * f_meio < 0:
            fim = meio
            meio_antigo = meio
            f_fim = f_meio
        #No intervalo [a,b], se f(a)*f(m) > 0, o intevalo passa a ser [m,b]
        else:
            inicio = meio
            meio_antigo = meio
            f_inicio = f_meio

    #iteração onde o erro calculado se torna menor que a teloreancia definida, retorna a raiz para função
    return meio, iteracao

def main():

    # Dados fornecidos pelo trabalho
    L = 5.0
    C = 10**-4
    t = 0.05

    # Intervalo inicial válido
    inicio = 300.0
    fim = 400.0
    tolerancia = 0.01 #Definir valor como porcentagem

    print("TRABALHO DE CÁLCULO NUMÉRICO")
    print("Problema: Zero de Raízes")
    print("Método: Bisseção")
    print(f"Indutância: {L} H")
    print(f"Capacitância: {C} F")
    print(f"Tempo: {t} s")
    print("Objetivo: q(t)/q0 = 0.01")

    #executa o a função da bissecção para os valores definidos
    try:
        R, iteracoes = bissecao(
            inicio, fim, L, C, t, tolerancia
        )

        print("\n--- RESULTADO FINAL ---")
        print(f"Resistência encontrada: {R:.6f} ohms")
        print(f"Iterações realizadas: {iteracoes}")
        print(f"f(R): {funcao(R, L, C, t):.10f}")
        print(
            "Razão q(t)/q0: "
            f"{funcao(R, L, C, t) + 0.01:.10f}"
        )
        # Gera valores de resistência para desenhar a curva
        valores_R = [
            inicio + i * (fim - inicio) / 500
            for i in range(501)
        ]

        # Calcula f(R) para cada valor de resistência
        valores_f = [
            funcao(valor, L, C, t)
            for valor in valores_R
        ]

        # Desenha a função
        plt.figure(figsize=(10, 6))
        plt.plot(
            valores_R,
            valores_f,
            label="f(R)",
            linewidth=2
        )

        # Linha horizontal correspondente a f(R) = 0
        plt.axhline(
            y=0,
            linestyle="--",
            label="f(R) = 0"
        )

        # Marca a raiz encontrada pela bisseção
        plt.scatter(
            [R],
            [funcao(R, L, C, t)],
            zorder=5,
            label=f"Raiz aproximada: {R:.6f} Ω"
        )

        # Identifica o ponto encontrado
        plt.annotate(
            f"R = {R:.6f} Ω",
            xy=(R, funcao(R, L, C, t)),
            xytext=(10, 20),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->"}
        )

        plt.title("Método da Bisseção - Circuito RLC")
        plt.xlabel("Resistência R (Ω)")
        plt.ylabel("f(R)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Exibe o gráfico
        plt.show()

    #caso tenha erro, retona o erro encontrado durante a operação
    except ValueError as erro:
        print(f"Erro: {erro}")

if __name__ == "__main__":
    main()
