import random
import time
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os
from dijkstra import ejecutar_dijkstra
from astar import ejecutar_astar
from pso import pso


# =====================================
# CONFIGURACIÓN
# =====================================

N_CASOS = 20
N_CORRIDAS_PSO = 10

random.seed(42)


# =====================================
# CARGAR RED
# =====================================

def cargar_red():

    with open("../data/network.pkl", "rb") as f:
        G = pickle.load(f)

    return G


# =====================================
# GENERAR CASOS DE PRUEBA
# =====================================

def generar_casos(G, n_casos):

    nodos = list(G.nodes())

    casos = []

    while len(casos) < n_casos:

        origen = random.choice(nodos)
        destino = random.choice(nodos)

        if origen != destino:

            casos.append((origen, destino))

    return casos


# =====================================
# EJECUTAR UN CASO
# =====================================

def evaluar_caso(G, origen, destino):

    resultados = []

    # =====================================
    # DIJKSTRA
    # =====================================

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

        "saltos": len(ruta_d)-1,

        "tiempo": tiempo_d,

        "error": 0

    })

# =====================================
# GUARDAR RESULTADOS
# =====================================

def guardar_resultados(resultados):

    df = pd.DataFrame(resultados)

    columnas = [
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
   


    # =====================================
    # A*
    # =====================================

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
        (costo_a-costo_d)
        /costo_d
    )*100

    resultados.append({

        "algoritmo": "A*",

        "ruta": ruta_a,

        "costo": costo_a,

        "saltos": len(ruta_a)-1,

        "tiempo": tiempo_a,

        "error": error_a

    })

# =====================================
# ESTADÍSTICAS
# =====================================

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

# =====================================
# GRÁFICAS
# =====================================

def generar_graficas(df):

    os.makedirs("../results", exist_ok=True)

    # -------------------------
    # Tiempo
    # -------------------------

    tiempo = df.groupby(
        "algoritmo"
    )["tiempo"].mean()

    plt.figure(figsize=(7,5))

    plt.bar(
        tiempo.index,
        tiempo.values
    )

    plt.title("Tiempo promedio")

    plt.ylabel("ms")

    plt.tight_layout()

    plt.savefig(
        "../results/time_comparison.png",
        dpi=300
    )

    plt.close()


    # -------------------------
    # Costo
    # -------------------------

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

    plt.tight_layout()

    plt.savefig(
        "../results/cost_comparison.png",
        dpi=300
    )

    plt.close()


    # -------------------------
    # Error
    # -------------------------

    error = df.groupby(
        "algoritmo"
    )["error"].mean()

    plt.figure(figsize=(7,5))

    plt.bar(
        error.index,
        error.values
    )

    plt.title("Error promedio")

    plt.ylabel("%")

    plt.tight_layout()

    plt.savefig(
        "../results/error_comparison.png",
        dpi=300
    )

    plt.close()

    print("\nGráficas generadas.")


# =====================================
# RESUMEN
# =====================================

def imprimir_resumen(df):

    print("\n")
    print("=" * 60)
    print("RESULTADOS FINALES")
    print("=" * 60)

    for algoritmo in df["algoritmo"].unique():

        datos = df[df["algoritmo"] == algoritmo]

        print(f"\n{algoritmo}")

        print("-" * 35)

        print(f"Costo promedio : {datos['costo'].mean():.2f}")

        print(f"Tiempo promedio: {datos['tiempo'].mean():.3f} ms")

        print(f"Saltos promedio: {datos['saltos'].mean():.2f}")

        print(f"Error promedio : {datos['error'].mean():.2f}%")

# =====================================
# PSO
# =====================================

mejor_costo = float("inf")
mejor_ruta = None

tiempos = []

for _ in range(N_CORRIDAS_PSO):

    inicio = time.perf_counter()

    ruta, costo = pso(
        G,
        origen,
        destino
    )

    tiempo = (
        time.perf_counter() - inicio
    ) * 1000

    tiempos.append(tiempo)

    if costo < mejor_costo:

        mejor_costo = costo
        mejor_ruta = ruta

# Tiempo promedio de las corridas
tiempo_promedio = sum(tiempos) / len(tiempos)

error = (
    (mejor_costo - costo_d)
    / costo_d
) * 100

resultados.append({

    "algoritmo": "PSO",

    "ruta": mejor_ruta,

    "costo": mejor_costo,

    "saltos": len(mejor_ruta) - 1,

    "tiempo": tiempo_promedio,

    "error": error

})


# =====================================
# MAIN
# =====================================

def main():

    print("="*60)
    print("EVALUACIÓN DE ALGORITMOS")
    print("="*60)

    G = cargar_red()

    casos = generar_casos(
        G,
        N_CASOS
    )

    todos_resultados = []

    for i, (origen, destino) in enumerate(casos):

        print(
            f"\nCaso {i+1}/{N_CASOS}: "
            f"{origen} -> {destino}"
        )

        resultados = evaluar_caso(
            G,
            origen,
            destino
        )

        for r in resultados:

            r["caso"] = i+1
            r["origen"] = origen
            r["destino"] = destino

            todos_resultados.append(r)

    print("\nEvaluación finalizada.")

    df = guardar_resultados(todos_resultados)

    calcular_estadisticas(df)

    generar_graficas(df)

    imprimir_resumen(df)

    return df


if __name__ == "__main__":

    resultados = main()

    df = main()

    print("\nPrimeros resultados:\n")

    print(df.head())

    print()

    for r in resultados:

        print(
            f"Caso {r['caso']:2d} | "
            f"{r['algoritmo']:10s} | "
            f"Costo={r['costo']:7.2f} | "
            f"Saltos={r['saltos']:2d} | "
            f"Tiempo={r['tiempo']:8.3f} ms"
        )