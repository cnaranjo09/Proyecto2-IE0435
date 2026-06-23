import pickle
import networkx as nx
import matplotlib.pyplot as plt
import os


# =====================================
# CARGAR RED
# =====================================

def cargar_red():

    with open("../data/network.pkl", "rb") as f:
        G = pickle.load(f)

    return G


# =====================================
# COSTO TOTAL
# =====================================

def calcular_costo(G, ruta):

    costo_total = 0

    for i in range(len(ruta) - 1):

        u = ruta[i]
        v = ruta[i + 1]

        costo_total += G[u][v]["cost"]

    return round(costo_total, 2)


# =====================================
# DIJKSTRA
# =====================================

def ejecutar_dijkstra(G, origen, destino):

    ruta = nx.dijkstra_path(
        G,
        source=origen,
        target=destino,
        weight="cost"
    )

    costo = nx.dijkstra_path_length(
        G,
        source=origen,
        target=destino,
        weight="cost"
    )

    return ruta, round(costo, 2)


# =====================================
# VISUALIZAR RUTA
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

    os.makedirs("../results", exist_ok=True)

    ruta_imagen = "../results/dijkstra_route.png"

    plt.title("Ruta encontrada por Dijkstra")

    plt.savefig(
        ruta_imagen,
        dpi=300
    )

    print(
        f"\nImagen guardada en: {ruta_imagen}"
    )



# =====================================
# Mostrar ruta
# =====================================

def mostrar_detalle_ruta(G, ruta):

    print("\nDetalle de la ruta:\n")

    total = 0

    for i in range(len(ruta)-1):

        u = ruta[i]
        v = ruta[i+1]

        costo = G[u][v]["cost"]

        total += costo

        print(f"{u} -> {v}   costo={costo}")

    print(f"\nCosto total = {round(total,2)}")





# =====================================
# MAIN
# =====================================

def main():

    print("Cargando red...")

    G = cargar_red()

    print("\nNodos disponibles:")

    print(list(G.nodes()))

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

    ruta, costo = ejecutar_dijkstra(
        G,
        origen,
        destino
    )

    print("\n===================")
    print("RESULTADO DIJKSTRA")
    print("===================")

    print("Ruta:", ruta)


    print("Costo total:", costo)

    print("Saltos:", len(ruta) - 1)
    mostrar_detalle_ruta(G, ruta)

    visualizar_ruta(
        G,
        ruta
    )


if __name__ == "__main__":
    main()