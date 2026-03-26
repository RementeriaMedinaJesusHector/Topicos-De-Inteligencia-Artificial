import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Quitar barra de herramientas
plt.rcParams['toolbar'] = 'none'

def costo(solucion):
    conflictos = 0
    n = len(solucion)
    for i in range(n):
        for j in range(i + 1, n):
            if solucion[i] == solucion[j] or abs(solucion[i] - solucion[j]) == abs(i - j):
                conflictos += 1
    return conflictos


def generar_vecinos(solucion):
    vecinos = []
    n = len(solucion)
    for fila in range(n):
        for col in range(n):
            if col != solucion[fila]:
                vecino = solucion[:]
                vecino[fila] = col
                vecinos.append(vecino)
    return vecinos


def busqueda_tabu(n=8, max_iter=200, tabu_tam=30):
    solucion = [random.randint(0, n - 1) for _ in range(n)]
    mejor_sol = solucion[:]
    mejor_costo = costo(solucion)
    lista_tabu = []
    movimientos = 0
    estados = [solucion[:]]

    inicio = time.time()

    for _ in range(max_iter):
        vecinos = generar_vecinos(solucion)
        vecinos = sorted(vecinos, key=costo)

        for vecino in vecinos:
            if vecino not in lista_tabu:
                solucion = vecino
                movimientos += 1
                estados.append(solucion[:])
                break

        c = costo(solucion)
        if c < mejor_costo:
            mejor_sol = solucion[:]
            mejor_costo = c

        lista_tabu.append(solucion)
        if len(lista_tabu) > tabu_tam:
            lista_tabu.pop(0)

        if mejor_costo == 0:
            break

    fin = time.time()
    tiempo = fin - inicio

    return mejor_sol, mejor_costo, tiempo, movimientos, estados


def dibujar_tablero(solucion, ax, tiempo, movimientos):
    n = len(solucion)
    ax.clear()
    # Dibujar tablero
    for i in range(n):
        for j in range(n):
            color = 'white' if (i + j) % 2 == 0 else 'gray'
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=color))
    # Dibujar reinas
    for fila, col in enumerate(solucion):
        ax.text(col + 0.5, fila + 0.5, '♛', ha='center', va='center', fontsize=20, color='red')
    # Texto con métricas
    ax.set_title(f"Tiempo: {tiempo:.4f} seg | Movimientos: {movimientos}", fontsize=12, color="blue")
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([])
    ax.set_yticks([])


def animar(estados, tiempo, movimientos):
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(
        fig,
        lambda i: dibujar_tablero(estados[i], ax, tiempo, movimientos),
        frames=len(estados),
        interval=500,
        repeat=False
    )
    plt.show()


# Ejecución
sol, c, t, m, estados = busqueda_tabu()
print("Solución encontrada:", sol)
print("Conflictos:", c)
print("Tiempo de ejecución:", t, "segundos")
print("Movimientos realizados:", m)

animar(estados, t, m)
