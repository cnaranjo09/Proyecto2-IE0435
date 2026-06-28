import pickle
import networkx as nx
import random
import matplotlib.pyplot as plt
import os


# =====================================
# CARGAR RED
# =====================================

def cargar_red():
    with open("../data/network.pkl", "rb") as f:
        return pickle.load(f)


# =====================================
# GENERAR RUTA ALEATORIA
# =====================================

def generar_ruta(G, origen, destino, max_intentos=50):
    """
    Genera una ruta aleatoria válida usando caminata aleatoria.
    """

    for _ in range(max_intentos):

        actual = origen
        ruta = [actual]

        while actual != destino:

            vecinos = list(G.neighbors(actual))

            if not vecinos:
                break

            siguiente = random.choice(vecinos)

            if siguiente in ruta:
                break

            ruta.append(siguiente)
            actual = siguiente

        if ruta[-1] == destino:
            return ruta

    return None


# =====================================
# FITNESS
# =====================================
def fitness(G, ruta, destino):

    if ruta[-1] != destino:
        return float("inf")
    costo = 0

    for i in range(len(ruta) - 1):

        u = ruta[i]
        v = ruta[i + 1]

        # VALIDACIÓN IMPORTANTE
        if not G.has_edge(u, v):
            return float("inf")  # ruta inválida

        costo += G[u][v]["cost"]

    return costo

# =====================================
# INICIALIZAR ENJAMBRE
# =====================================

def inicializar_enjambre(G, origen, destino, n_particulas=20):

    enjambre = []

    for _ in range(n_particulas):

        ruta = generar_ruta(G, origen, destino)

        if ruta is None:
            continue
        fit = fitness(G, ruta, destino)

        if fit == float("inf"):
            continue

        enjambre.append({
            "ruta": ruta,
            "fitness": fit,
            "pbest": ruta,
            "pbest_fitness": fit
        })

    return enjambre


# =====================================
# MUTACIÓN SIMPLE
# =====================================

def mutar_ruta(G, ruta, destino):

    if len(ruta) < 3:
        return ruta

    idx = random.randint(1, len(ruta)-2)

    prefijo = ruta[:idx]

    nodo_actual = prefijo[-1]

    nueva_ruta = prefijo.copy()

    visitados = set(nueva_ruta)

    while nodo_actual != destino:

        vecinos = [
            v for v in G.neighbors(nodo_actual)
            if v not in visitados
        ]

        if not vecinos:
            return None

        siguiente = random.choice(vecinos)

        nueva_ruta.append(siguiente)

        visitados.add(siguiente)

        nodo_actual = siguiente

    return nueva_ruta

# =====================================
# PSO
# =====================================

def pso(G, origen, destino,
        iteraciones=30,
        n_particulas=20):

    enjambre = inicializar_enjambre(G, origen, destino, n_particulas)

    gbest = min(enjambre, key=lambda x: x["fitness"])
    gbest_ruta = gbest["ruta"].copy()
    gbest_fitness = gbest["fitness"]

    for it in range(iteraciones):

        for particula in enjambre:

            nueva_ruta = mutar_ruta(G, particula["ruta"], destino)

            if nueva_ruta is None:
                continue

            nuevo_fitness = fitness(G, nueva_ruta, destino)
            if nuevo_fitness == float("inf"):
                continue

            particula["ruta"] = nueva_ruta
            particula["fitness"] = nuevo_fitness

            # actualizar pbest
            if nuevo_fitness < particula["pbest_fitness"]:
                particula["pbest"] = nueva_ruta
                particula["pbest_fitness"] = nuevo_fitness

        # actualizar gbest
        mejor_local = min(enjambre, key=lambda x: x["fitness"])

        if mejor_local["fitness"] < gbest_fitness:
            gbest_fitness = mejor_local["fitness"]
            gbest_ruta = mejor_local["ruta"].copy()

        print(f"Iteración {it+1} | Mejor costo: {gbest_fitness:.2f}")

    return gbest_ruta, gbest_fitness


# =====================================
# VISUALIZAR
# =====================================

def visualizar(G, ruta):

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=True, node_size=700)

    labels = nx.get_edge_attributes(G, "cost")

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    edges = list(zip(ruta[:-1], ruta[1:]))

    nx.draw_networkx_edges(G, pos, edgelist=edges, width=4)

    os.makedirs("../results", exist_ok=True)

    plt.title("Ruta encontrada por PSO")

    plt.savefig("../results/pso_route.png", dpi=300)

    print("\nImagen guardada en: ../results/pso_route.png")


# =====================================
# MAIN
# =====================================

def main():

    G = cargar_red()

    print("\nNodos disponibles:", list(G.nodes()))

    origen = int(input("\nNodo origen: "))
    destino = int(input("Nodo destino: "))

    ruta, costo = pso(G, origen, destino)

    print("\n====================")
    print("RESULTADO PSO")
    print("====================")

    print("Ruta:", ruta)
    print("Costo:", round(costo, 2))
    print("Saltos:", len(ruta) - 1)

    visualizar(G, ruta)


if __name__ == "__main__":
    main()