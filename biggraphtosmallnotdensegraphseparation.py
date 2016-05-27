import networkx as nx

def graph_separation(G,sizetreshold,output,septreshold,notseparate):
    
    if len(G.nodes())<(sizetreshold+1):
        output.append(G)
        return output

    cut_value,xer=nx.stoer_wagner(G)
    H1=G.subgraph(xer[0])
    H2=G.subgraph(xer[1])
    if nx.average_node_connectivity(H1)>septreshold:
        notseparate.append(H1)
    else:
        graph_separation(H1,treshold,output,notseparate)
    if nx.average_node_connectivity(H2)>septreshold:
        notseparate.append(H2)
    else:
        graph_separation(H2,treshold,output,notseparate)        
   
    return output,notseparate


#Here we determine our graph
G = nx.Graph()
final=[]
notseparate=[]
treshold=2
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 2),('d','e',7),('e', 'k', 5),('d','k',6),('c','e',2)]
G.add_weighted_edges_from(e)

#Here we separate it to nonconnected subgraphs whis is not very dense
subgraphs=list(nx.connected_component_subgraphs(G))

#For each subgraph we make a cuts until the size of each subgraph will not exceed 6

for i in range(len(subgraphs)):
    graph_separation(subgraphs[i],treshold,final,notseparate)