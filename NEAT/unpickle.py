import pickle
import neat
import networkx as nx
import matplotlib.pyplot as plt


def unpickle_genome(filename):
    with open(filename, "rb") as f:
        best_genome = pickle.load(f)
    return best_genome


def draw_net(
    config,
    genome,
    view=True,
    filename=None,
    node_names=None,
    show_disabled=True,
    node_size=500,
):

    G = nx.DiGraph()

    inputs = config.genome_config.input_keys
    outputs = config.genome_config.output_keys
    hidden_nodes = [
        node
        for node in genome.nodes.keys()
        if node not in inputs and node not in outputs
    ]

    G.add_nodes_from(inputs, color="#03fc62")
    G.add_nodes_from(outputs, color="#00ffff")
    G.add_nodes_from(hidden_nodes, color="#fcffa3")

    # Add edges (connections)
    for connection in genome.connections.values():
        if connection.enabled or show_disabled:
            color = "black" if connection.enabled else "gray"
            G.add_edge(
                connection.key[0],
                connection.key[1],
                color=color,
                weight=connection.weight,
            )

    pos = {}

    # Inputs on the left
    for i, node in enumerate(inputs):
        pos[node] = (-1, i)

    # Outputs on the right
    for i, node in enumerate(outputs):
        pos[node] = (1, i)

    # Hidden nodes in the middle
    num_hidden = len(hidden_nodes)
    for i, node in enumerate(hidden_nodes):
        pos[node] = (0, i - num_hidden / 2)

    labels = {}
    if node_names:
        labels = {key: node_names.get(key, key) for key in G.nodes()}
    else:
        labels = {key: key for key in G.nodes()}

    edges = G.edges()
    colors = [G[u][v]["color"] for u, v in edges]
    weights = [abs(G[u][v]["weight"]) for u, v in edges]

    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_color=[G.nodes[n]["color"] for n in G],
        edge_color=colors,
        width=weights,
        node_size=node_size,
    )

    if filename:
        plt.savefig(filename)
    if view:
        plt.show()
    plt.close()


config_path = "NEAT/config-feedforward.txt"
pkl_file = "NEAT/best-genome.pkl"
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path,
)

best_genome = unpickle_genome(pkl_file)

node_names = {
    -1: "X",
    -2: "Y",
    -3: "Rocket\nAngle",
    -4: "Velocity X",
    -5: "Velocity Y",
    -6: "Distance",
    -7: "Angle to\nTarget",
    0: "Thrust",
    1: "Turn\nLeft",
    2: "Turn\nRight",
}

draw_net(config, best_genome, view=True, node_names=node_names, node_size=4000)
