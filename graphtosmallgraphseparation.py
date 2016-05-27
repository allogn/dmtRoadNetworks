import networkx as nx

def graph_separation(G,treshold,output):
    
    if len(G.nodes())<(treshold+1):
        output.append(G)
        return output

    cut_value,xer=nx.stoer_wagner(G)
    H1=G.subgraph(xer[0])
    H2=G.subgraph(xer[1])
    graph_separation(H1,treshold,output)
    graph_separation(H2,treshold,output)
        
    return output


#Here we determine our graph
G = nx.Graph()
final=[]
treshold=3
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 2),('d','e',7),('e', 'k', 5),('d','k',6),('c','e',2)]
G.add_weighted_edges_from(e)

#Here we separate it to nonconnected subgraphs
subgraphs=list(nx.connected_component_subgraphs(G))

#For each subgraph we make a cuts until the size of each subgraph will not exceed 6

for i in range(len(subgraphs)):
    graph_separation(subgraphs[i],treshold,final)

    
#As output we receive a list of subgraphs which lenght doesn't exceed 6. Below is some example of this list elements:

print final[0].nodes()