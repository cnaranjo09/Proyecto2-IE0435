import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import pickle


# =====================================
# CONFIGURACIÓN
# =====================================

NUM_NODOS = 50
ENLACES_POR_NODO = 3

ALPHA = 0.7   # peso latencia
BETA = 0.3    # peso congestión


# =====================================
# GENERAR RED
# =====================================

def generar_red(
        num_nodos=NUM_NODOS,
        enlaces_por_nodo=ENLACES_POR_NODO,
        seed=None
):
    """
    Genera una red tipo Barabasi-Albert.
    """

    G = nx.barabasi_albert_graph(
        n=num_nodos,
        m=enlaces_por_nodo,
        seed=seed
)

    return G


# =====================================
# ASIGNAR COSTOS
# =====================================

def asignar_costos(G):
    """
    Asigna:
        latencia
        congestion
        costo
    a cada enlace.
    """

    for u, v in G.edges():

        latencia = random.randint(1, 50)

        congestion = round(
            random.uniform(0, 1),
            2
        )

        costo = (
            ALPHA * latencia +
            BETA * (congestion * 100)
        )

        G[u][v]["latency"] = latencia
        G[u][v]["congestion"] = congestion
        G[u][v]["cost"] = round(costo, 2)


# =====================================
# GENERAR GRAFO COMPLETO
# =====================================

def generar_grafo(
        num_nodos=NUM_NODOS,
        enlaces_por_nodo=ENLACES_POR_NODO,
        seed=None
):

    if seed is not None:
        random.seed(seed)

    G = generar_red(
        num_nodos,
        enlaces_por_nodo,
        seed
    )

    asignar_costos(G)

    return G



# =====================================
# MOSTRAR INFORMACIÓN
# =====================================

def mostrar_resumen(G):

    print("\n==========================")
    print("RESUMEN DE LA RED")
    print("==========================")

    print("Nodos:", G.number_of_nodes())
    print("Enlaces:", G.number_of_edges())

    print("\nPrimeros enlaces:\n")

    contador = 0

    for u, v, data in G.edges(data=True):

        print(
            f"{u} <-> {v} | "
            f"latencia={data['latency']} ms | "
            f"congestion={data['congestion']} | "
            f"cost={data['cost']}"
        )

        contador += 1

        if contador >= 10:
            break


# =====================================
# DIBUJAR RED
# =====================================

def visualizar_red(G):

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(
        G,
        seed=42
    )

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700
    )

    labels = nx.get_edge_attributes(
        G,
        "cost"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels
    )

    plt.title("Red simulada")

    os.makedirs("../results", exist_ok=True)

    ruta = "../results/network.png"

    plt.savefig(ruta, dpi=300)

    print(f"\nImagen guardada en: {ruta}")


# =====================================
# GUARDAR RED
# =====================================

def guardar_red(G):

    with open(
        "../data/network.pkl",
        "wb"
    ) as f:

        pickle.dump(G, f)

    print(
        "\nRed guardada en:"
        " ../data/network.pkl"
    )



# =====================================
# MAIN
# =====================================

def main():

    print("Generando red...")

    G = generar_grafo(seed=2)

    mostrar_resumen(G)

    guardar_red(G)

    visualizar_red(G)


if __name__ == "__main__":
    main()