import os
import time
import random

from generate_graph import generar_grafo

import pandas as pd
import matplotlib.pyplot as plt

from dijkstra import ejecutar_dijkstra
from astar import ejecutar_astar
from pso import pso


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

N_REDES = 10
N_CASOS = 20
N_CORRIDAS_PSO = 10


random.seed(42)


# ==========================================================
# CARGAR RED
# ==========================================================



# def cargar_red():

#    with open("../data/network.pkl", "rb") as f:
#        G = pickle.load(f)

#    return G


# ==========================================================
# GENERAR CASOS ALEATORIOS
# ==========================================================

def generar_casos(G, n_casos):

    nodos = list(G.nodes())

    casos = []

    while len(casos) < n_casos:

        origen = random.choice(nodos)
        destino = random.choice(nodos)

        if origen != destino:
            casos.append((origen, destino))

    return casos


# ==========================================================
# EVALUAR UN CASO
# ==========================================================

def evaluar_caso(G, origen, destino):

    resultados = []

    # ------------------------------------------------------
    # DIJKSTRA
    # ------------------------------------------------------

    inicio = time.perf_counter()

    ruta_d, costo_d = ejecutar_dijkstra(
        G,
        origen,
        destino
    )

    tiempo_d = (
        time.perf_counter() - inicio
    ) * 1000

    resultados.append({

        "algoritmo": "Dijkstra",

        "ruta": ruta_d,

        "costo": costo_d,

        "saltos": len(ruta_d) - 1,

        "tiempo": tiempo_d,

        "error": 0

    })


    # ------------------------------------------------------
    # A*
    # ------------------------------------------------------

    inicio = time.perf_counter()

    ruta_a, costo_a = ejecutar_astar(
        G,
        origen,
        destino
    )

    tiempo_a = (
        time.perf_counter() - inicio
    ) * 1000

    error_a = (
        (costo_a - costo_d)
        / costo_d
    ) * 100

    resultados.append({

        "algoritmo": "A*",

        "ruta": ruta_a,

        "costo": costo_a,

        "saltos": len(ruta_a) - 1,

        "tiempo": tiempo_a,

        "error": error_a

    })
    # ------------------------------------------------------
    # PSO
    # ------------------------------------------------------

    mejor_costo = float("inf")
    mejor_ruta = None

    tiempos = []

    for _ in range(N_CORRIDAS_PSO):

        inicio = time.perf_counter()

        ruta_pso, costo_pso = pso(
            G,
            origen,
            destino
        )

        tiempo = (
            time.perf_counter() - inicio
        ) * 1000

        tiempos.append(tiempo)

        if costo_pso < mejor_costo:

            mejor_costo = costo_pso
            mejor_ruta = ruta_pso.copy()

    tiempo_promedio = sum(tiempos) / len(tiempos)

    error_pso = (
        (mejor_costo - costo_d)
        / costo_d
    ) * 100

    resultados.append({

        "algoritmo": "PSO",

        "ruta": mejor_ruta,

        "costo": mejor_costo,

        "saltos": len(mejor_ruta) - 1,

        "tiempo": tiempo_promedio,

        "error": error_pso

    })

    return resultados
# ==========================================================
# GUARDAR RESULTADOS
# ==========================================================

def guardar_resultados(resultados):

    df = pd.DataFrame(resultados)

    columnas = [
        "red",
        "caso",
        "origen",
        "destino",
        "algoritmo",
        "costo",
        "saltos",
        "tiempo",
        "error"
    ]

    df = df[columnas]

    os.makedirs("../results", exist_ok=True)

    archivo = "../results/evaluation.csv"

    df.to_csv(
        archivo,
        index=False
    )

    print("\nResultados guardados en:")
    print(archivo)

    return df


# ==========================================================
# ESTADÍSTICAS
# ==========================================================

def calcular_estadisticas(df):

    resumen = df.groupby("algoritmo").agg({

        "costo": ["mean", "min", "max", "std"],

        "tiempo": ["mean", "min", "max", "std"],

        "saltos": ["mean"],

        "error": ["mean"]

    })

    print("\n")
    print("=" * 60)
    print("RESUMEN ESTADÍSTICO")
    print("=" * 60)

    print(resumen)

    return resumen


# ==========================================================
# RESUMEN EN CONSOLA
# ==========================================================

def imprimir_resumen(df):

    print("\n")
    print("=" * 60)
    print("RESULTADOS FINALES")
    print("=" * 60)

    for algoritmo in df["algoritmo"].unique():

        datos = df[
            df["algoritmo"] == algoritmo
        ]

        print(f"\n{algoritmo}")
        print("-" * 40)

        print(
            f"Costo promedio : "
            f"{datos['costo'].mean():.2f}"
        )

        print(
            f"Tiempo promedio: "
            f"{datos['tiempo'].mean():.3f} ms"
        )

        print(
            f"Saltos promedio: "
            f"{datos['saltos'].mean():.2f}"
        )

        print(
            f"Error promedio : "
            f"{datos['error'].mean():.2f}%"
        )

# ==========================================================
# GENERAR GRÁFICAS
# ==========================================================

def generar_graficas(df):

    os.makedirs("../results", exist_ok=True)

    # -----------------------------------------
    # Tiempo promedio
    # -----------------------------------------

    tiempo = df.groupby(
        "algoritmo"
    )["tiempo"].mean()

    plt.figure(figsize=(7,5))

    plt.bar(
        tiempo.index,
        tiempo.values
    )

    plt.title("Tiempo promedio")

    plt.ylabel("Tiempo (ms)")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        "../results/time_comparison.png",
        dpi=300
    )

    plt.close()


    # -----------------------------------------
    # Costo promedio
    # -----------------------------------------

    costo = df.groupby(
        "algoritmo"
    )["costo"].mean()

    plt.figure(figsize=(7,5))

    plt.bar(
        costo.index,
        costo.values
    )

    plt.title("Costo promedio")

    plt.ylabel("Costo")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        "../results/cost_comparison.png",
        dpi=300
    )

    plt.close()


    # -----------------------------------------
    # Error promedio
    # -----------------------------------------

    error = df.groupby(
        "algoritmo"
    )["error"].mean()

    plt.figure(figsize=(7,5))

    plt.bar(
        error.index,
        error.values
    )

    plt.title("Error promedio")

    plt.ylabel("Error (%)")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        "../results/error_comparison.png",
        dpi=300
    )

    plt.close()

    print("\nGráficas guardadas en ../results/")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("EVALUACIÓN DE ALGORITMOS")
    print("=" * 60)

    todos_resultados = []

    # =====================================
    # Evaluar varias redes
    # =====================================

    for red in range(N_REDES):

        print("\n" + "=" * 60)
        print(f"RED {red+1}/{N_REDES}")
        print("=" * 60)

        G = generar_grafo(seed=red)

        casos = generar_casos(
            G,
            N_CASOS
        )

        # -----------------------------
        # Casos de prueba de esta red
        # -----------------------------

        for i, (origen, destino) in enumerate(casos):

            print(
                f"Caso {i+1}/{N_CASOS}: "
                f"{origen} -> {destino}"
            )

            resultados = evaluar_caso(
                G,
                origen,
                destino
            )

            for r in resultados:

                r["red"] = red + 1
                r["caso"] = i + 1
                r["origen"] = origen
                r["destino"] = destino

                todos_resultados.append(r)

    print("\nEvaluación finalizada.")

    df = guardar_resultados(
        todos_resultados
    )

    calcular_estadisticas(df)

    generar_graficas(df)

    imprimir_resumen(df)

    return df


if __name__ == "__main__":

    df = main()

    print("\nPrimeros resultados:\n")

    print(df.head())