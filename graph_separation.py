import networkx as nx


def graph_separation(G, threshold, output):
    if len(G.nodes()) < (threshold + 1):
        output.append(G)
        return output

    cut_value, xer = nx.stoer_wagner(G)
    H1 = G.subgraph(xer[0])
    H2 = G.subgraph(xer[1])
    graph_separation(H1, threshold, output)
    graph_separation(H2, threshold, output)

    return output


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Here we determine our graph
    G = nx.Graph()
    e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 12),('e','f',4)]
    G.add_weighted_edges_from(e)

    # Here we separate it to non-connected sub-graphs
    subgraphs = list(nx.connected_component_subgraphs(G))
    print('sub graphs', *[sub.nodes() for sub in subgraphs])

    final = []
    threshold = 3

    # For each sub-graph we make a cuts until the size of each sub-graph will not exceed threshold
    for i in range(len(subgraphs)):
        graph_separation(subgraphs[i], threshold, final)

    # As output we receive a list of sub-graphs which length doesn't exceed threshold.
    print('divided sub graphs', *[sub.nodes() for sub in final])
