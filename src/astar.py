import pickle
import networkx as nx
import matplotlib.pyplot as plt
import math
import os


# =====================================
# CARGAR RED
# =====================================

def cargar_red():

    with open("../data/network.pkl", "rb") as f:
        G = pickle.load(f)

    return G


# =====================================
# HEURÍSTICA
# =====================================

def heuristica(a, b, posiciones):

    x1, y1 = posiciones[a]
    x2, y2 = posiciones[b]

    return math.sqrt(
        (x2 - x1)**2 +
        (y2 - y1)**2
    )


# =====================================
# EJECUTAR A*
# =====================================

def ejecutar_astar(G, origen, destino):

    posiciones = nx.spring_layout(
        G,
        seed=42
    )

    ruta = nx.astar_path(
        G,
        origen,
        destino,
        heuristic=lambda a, b:
        heuristica(a, b, posiciones),
        weight="cost"
    )

    costo = nx.path_weight(
        G,
        ruta,
        weight="cost"
    )

    return ruta, round(costo, 2)


# =====================================
# DETALLE DE RUTA
# =====================================

def mostrar_detalle_ruta(G, ruta):

    print("\nDetalle de la ruta:\n")

    total = 0

    for i in range(len(ruta)-1):

        u = ruta[i]
        v = ruta[i+1]

        costo = G[u][v]["cost"]

        total += costo

        print(
            f"{u} -> {v}   costo={costo}"
        )

    print(
        f"\nCosto total = {round(total,2)}"
    )


# =====================================
# VISUALIZACIÓN
# =====================================

def visualizar_ruta(G, ruta):

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

    ruta_edges = list(
        zip(
            ruta[:-1],
            ruta[1:]
        )
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=ruta_edges,
        width=4
    )

    os.makedirs(
        "../results",
        exist_ok=True
    )

    archivo = (
        "../results/astar_route.png"
    )

    plt.title(
        "Ruta encontrada por A*"
    )

    plt.savefig(
        archivo,
        dpi=300
    )

    print(
        f"\nImagen guardada en: {archivo}"
    )


# =====================================
# MAIN
# =====================================

def main():

    G = cargar_red()

    print(
        "\nNodos disponibles:"
    )

    print(
        list(G.nodes())
    )

    origen = int(
        input(
            "\nNodo origen: "
        )
    )

    destino = int(
        input(
            "Nodo destino: "
        )
    )

    ruta, costo = ejecutar_astar(
        G,
        origen,
        destino
    )

    print("\n================")
    print("RESULTADO A*")
    print("================")

    print("Ruta:", ruta)

    print("Costo:", costo)

    print(
        "Saltos:",
        len(ruta)-1
    )

    mostrar_detalle_ruta(
        G,
        ruta
    )

    visualizar_ruta(
        G,
        ruta
    )


if __name__ == "__main__":
    main()