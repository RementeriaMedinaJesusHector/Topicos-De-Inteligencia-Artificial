import numpy as np
import random
import math
import matplotlib.pyplot as plt
import pandas as pd

# Quitar barra de herramientas
plt.rcParams['toolbar'] = 'none'

# Matriz de distancias
distancias = pd.read_excel("matriz_distancias.xlsx", header=0).iloc[1:,1:].values

# Matriz de costos de combustible
costos = pd.read_excel("matriz_costos_combustible.xlsx", header=0).iloc[1:,1:].values

def calcular_costo(ruta, matriz_distancias, matriz_costos):
    costo_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        distancia = matriz_distancias[origen][destino]
        costo_combustible = matriz_costos[origen][destino]
        costo_total += distancia * costo_combustible
    return costo_total

def generar_ruta_inicial(nodos):
    ruta = list(range(nodos))
    random.shuffle(ruta)
    return ruta

def generar_vecino(ruta):
    nueva_ruta = ruta.copy()
    i, j = random.sample(range(len(ruta)), 2)
    nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
    return nueva_ruta

def recorido_simulado(matriz_distancias, matriz_costos, iteraciones=1000, temp_inicial=100, alfa=0.99):
    nodos = len(matriz_distancias)
    ruta_actual = generar_ruta_inicial(nodos)
    costo_actual = calcular_costo(ruta_actual, matriz_distancias, matriz_costos)

    mejor_ruta = ruta_actual
    mejor_costo = costo_actual

    temperatura = temp_inicial
    historial_costos = []

    for _ in range(iteraciones):
        vecino = generar_vecino(ruta_actual)
        costo_vecino = calcular_costo(vecino, matriz_distancias, matriz_costos)

        # Aceptación de vecino
        if costo_vecino < costo_actual:
            ruta_actual, costo_actual = vecino, costo_vecino
        else:
            prob = math.exp(-(costo_vecino - costo_actual) / temperatura)
            if random.random() < prob:
                ruta_actual, costo_actual = vecino, costo_vecino

        # Actualizar mejor solución
        if costo_actual < mejor_costo:
            mejor_ruta, mejor_costo = ruta_actual, costo_actual

        historial_costos.append(mejor_costo)
        temperatura *= alfa  # enfriamiento

    return mejor_ruta, mejor_costo, historial_costos

print("Distancias shape:", distancias.shape)
print("Costos shape:", costos.shape)

mejor_ruta, mejor_costo, historial = recorido_simulado(distancias, costos)

print("Mejor ruta encontrada:", mejor_ruta)
print("Costo total:", mejor_costo)

plt.plot(historial)
plt.xlabel("Iteraciones")
plt.ylabel("Costo")
plt.title(f"Evolución del costo en Recocido Simulado\nCosto total óptimo: {mejor_costo}")
plt.show()
