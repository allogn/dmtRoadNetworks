
# coding: utf-8

# In[8]:

import cPickle, gzip, math, random
import numpy as np
from numba import autojit
import networkx as nx
import xml.sax
import copy
import matplotlib.pyplot as plt
import smopy
get_ipython().magic(u'matplotlib inline')

def getGraph(Z,x1,y1,x2,y2,delta=0.000025):

#     """
#     Read graphs in Open Street Maps osm format
#     Based on osm.py from brianw's osmgeocode
#     http://github.com/brianw/osmgeocode, which is based on osm.py from
#     comes from Graphserver:
#     http://github.com/bmander/graphserver/tree/master and is copyright (c)
#     2007, Brandon Martin-Anderson under the BSD License
#     """

    import xml.sax
    import copy
    import networkx

    def download_osm(left,bottom,right,top,highway_cat):
#         """
#         Downloads OSM street (only highway-tagged) Data using a BBOX, 
#         plus a specification of highway tag values to use

#         Parameters
#         ----------
#         left,bottom,right,top : BBOX of left,bottom,right,top coordinates in WGS84
#         highway_cat : highway tag values to use, separated by pipes (|), for instance 'motorway|trunk|primary'

#         Returns
#         ----------
#         stream object with osm xml data

#         """

        #Return a filehandle to the downloaded data."""
        from urllib import urlopen
        #fp = urlopen( "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f"%(left,bottom,right,top) )
        #fp = urlopen( "http://www.overpass-api.de/api/xapi?way[highway=*][bbox=%f,%f,%f,%f]"%(left,bottom,right,top) )
        print "trying to download osm data from "+str(left),str(bottom),str(right),str(top)+" with highways of categories"+highway_cat
        try:    
            print "downloading osm data from "+str(left),str(bottom),str(right),str(top)+" with highways of categories"+highway_cat
            fp = urlopen( "http://www.overpass-api.de/api/xapi?way[highway=%s][bbox=%f,%f,%f,%f]"%(highway_cat,left,bottom,right,top) )
            #slooww only ways,and in ways only "highways" (i.e. roads)
            #fp = urlopen( "http://open.mapquestapi.com/xapi/api/0.6/way[highway=*][bbox=%f,%f,%f,%f]"%(left,bottom,right,top) )
            return fp
        except:
            print "osm data download unsuccessful"

    def read_osm(filename_or_stream, only_roads=True):
#         """Read graph in OSM format from file specified by name or by stream object.

#         Parameters
#         ----------
#         filename_or_stream : filename or stream object

#         Returns
#         -------
#         G : Graph

#         Examples
#         --------
#         >>> G=nx.read_osm(nx.download_osm(-122.33,47.60,-122.31,47.61))
#         >>> plot([G.node[n]['data'].lat for n in G], [G.node[n]['data'].lon for n in G], ',')

#         """
        osm = OSM(filename_or_stream)
        G = networkx.DiGraph()

        for w in osm.ways.itervalues():
            if only_roads and 'highway' not in w.tags:
                continue
            G.add_path(w.nds, id=w.id, highway = w.tags['highway'])#{str(k): type(v) for k,v in w.tags.items()})

            if 'oneway' not in w.tags and  w.tags['highway'] != 'motorway':
                G.add_path(reversed(w.nds), id=w.id, highway = w.tags['highway'])

            elif w.tags['oneway'] != 'yes' and w.tags['oneway'] != '-1' and  w.tags['highway'] != 'motorway':
                G.add_path(reversed(w.nds), id=w.id, highway = w.tags['highway'])


        for n_id in G.nodes_iter():
            n = osm.nodes[n_id]
            G.node[n_id] = dict(lon=n.lon,lat=n.lat)
        return G


    class Node:
        def __init__(self, id, lon, lat):
            self.id = id
            self.lon = lon
            self.lat = lat
            self.tags = {}

    class Way:
        def __init__(self, id, osm):
            self.osm = osm
            self.id = id
            self.nds = []
            self.tags = {}

        def split(self, dividers):
            # slice the node-array using this nifty recursive function
            def slice_array(ar, dividers):
                for i in range(1,len(ar)-1):
                    if dividers[ar[i]]>1:
                        #print "slice at %s"%ar[i]
                        left = ar[:i+1]
                        right = ar[i:]

                        rightsliced = slice_array(right, dividers)

                        return [left]+rightsliced
                return [ar]


            slices = slice_array(self.nds, dividers)

            # create a way object for each node-array slice
            ret = []
            i=0
            for slice in slices:
                littleway = copy.copy( self )
                littleway.id += "-%d"%i
                littleway.nds = slice
                ret.append( littleway )
                i += 1           
            return ret
    class OSM:
        def __init__(self, filename_or_stream):
            """ File can be either a filename or stream/file object."""
            nodes = {}
            ways = {}

            superself = self

            class OSMHandler(xml.sax.ContentHandler):
                @classmethod
                def setDocumentLocator(self,loc):
                    pass

                @classmethod
                def startDocument(self):
                    pass

                @classmethod
                def endDocument(self):
                    pass

                @classmethod
                def startElement(self, name, attrs):
                    if name=='node':
                        self.currElem = Node(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                    elif name=='way':
                        self.currElem = Way(attrs['id'], superself)
                    elif name=='tag':
                        self.currElem.tags[attrs['k']] = attrs['v']
                    elif name=='nd':
                        self.currElem.nds.append( attrs['ref'] )

                @classmethod
                def endElement(self,name):
                    if name=='node':
                        nodes[self.currElem.id] = self.currElem
                    elif name=='way':
                        ways[self.currElem.id] = self.currElem

                @classmethod
                def characters(self, chars):
                    pass

            xml.sax.parse(filename_or_stream, OSMHandler)

            self.nodes = nodes
            self.ways = ways
            #"""   
            #count times each node is used
            node_histogram = dict.fromkeys( self.nodes.keys(), 0 )
            for way in self.ways.values():
                if len(way.nds) < 2:       #if a way has only one node, delete it out of the osm collection
                    del self.ways[way.id]
                else:
                    for node in way.nds:
                        node_histogram[node] += 1

            #use that histogram to split all ways, replacing the member set of ways
            new_ways = {}
            for id, way in self.ways.iteritems():
                split_ways = way.split(node_histogram)
                for split_way in split_ways:
                    new_ways[split_way.id] = split_way
            self.ways = new_ways
#########################################################################################
    p=[x1,y1,x2,y2]
    highway_cat = 'motorway|trunk|primary|secondary|tertiary|road|residential|service|motorway_link|trunk_link|primary_link|secondary_link|teriary_link'
    G=read_osm(download_osm(p[0],p[1],p[2],p[3],highway_cat))
    def dist(a,b):
        return np.math.sqrt((a['lat']-b['lat'])*(a['lat']-b['lat'])+(a['lon']-b['lon'])*(b['lon']-b['lon']))
    def unite(lists,nodes,Edges,weights):
        labels={}
        for n in nodes:
            labels[n]=0
        for i in range(len(lists)):
            if len(lists[i])>1:
                for j in range(len(lists[i])):
                    labels[lists[i][j]]=i+1
        for i in range(len(lists)):
            if len(lists[i])<2:
                continue
            lat=0
            lon=0
            for j in range(len(lists[i])):
                lat+=nodes[lists[i][j]]['lat']
                lon+=nodes[lists[i][j]]['lon']
                d=[]
                for k1 in range(len(Edges[lists[i][j]])):
                    e=Edges[lists[i][j]][k1]
                    if labels[e[0]]==labels[e[1]]:
                        d.append(e)
                        continue
                    if e[0]==lists[i][j]:
                        Edges[lists[i][0]].append((lists[i][0],e[1]))
                        weights[(lists[i][0],e[1])]=weights[e]
                        n=e[1]
                    if e[1]==lists[i][j]:
                        Edges[lists[i][0]].append((e[0],lists[i][0]))
                        weights[(e[0],lists[i][0])]=weights[e]
                        n=e[0]
                    for k2 in range(len(Edges[n])):
                        ee=Edges[n][k2]
                        if ee[0]==lists[i][j]:
                            Edges[n][k2]=(lists[i][0],ee[1])
                        else:
                            if ee[1]==lists[i][j]:
                                Edges[n][k2]=(ee[0],lists[i][0])
                for k in range(len(d)):
                    Edges[lists[i][j]].remove(d[k])
                if j>0:
                    Edges[lists[i][j]]=[]
            nodes[lists[i][0]]['lat']=lat/len(lists[i])
            nodes[lists[i][0]]['lon']=lon/len(lists[i])
        return Edges
#     delta=0.000005
    cut=0
    edges=G.edges()
    weights={}
    edges=G.edges()
    for e in edges:
        weights[e]=dist(G.node[e[0]],G.node[e[1]])
    xx1=[]
    yy1=[]
    xx2=[]
    yy2=[]
    Edges={}
    for n in G.node:
        Edges[n]=[]
    for e in edges:
        if e[0]!=e[1]:
            Edges[e[0]].append(e)
            Edges[e[1]].append(e)
    for n in Edges:
        d=[]
        for e in Edges[n]:
            if e[0]==e[1]:
                d.append(e)
        for i in range(len(d)):
            Edges[n].remove(d[i])
    for i in range(len(edges)):
        xx1.append(G.node[edges[i][0]]['lat'])
        yy1.append(G.node[edges[i][0]]['lon'])
        xx2.append(G.node[edges[i][1]]['lat'])
        yy2.append(G.node[edges[i][1]]['lon'])
    degree=G.degree()
    print len(G.node),'nodes'
    print len(edges),'edges'
    for i in (degree):
        if degree[i]<=4:
            a1=[]
            a2=[]
            d=[]
            for e in Edges[i]:
                if e[0]==i:
                    a2.append(e[1])#out
                    d.append(e)
                else:
                    if e[1]==i:
                        a1.append(e[0])#in
                        d.append(e)
            if (len(a1)==len(a2) and len(a1)==2):
                a1.sort()
                a2.sort()
                if (a1[0]==a2[0] and a1[1]==a2[1] and len(d)==4):
                    Edges[d[0][0]].remove(d[0])
                    Edges[d[0][1]].remove(d[0])
                    Edges[d[1][0]].remove(d[1])
                    Edges[d[1][1]].remove(d[1])
                    Edges[d[2][0]].remove(d[2])
                    Edges[d[2][1]].remove(d[2])
                    Edges[d[3][0]].remove(d[3])
                    Edges[d[3][1]].remove(d[3])
                    Edges[a1[0]].append((a1[0],a1[1]))
                    Edges[a1[1]].append((a1[0],a1[1]))
                    Edges[a1[0]].append((a1[1],a1[0]))
                    Edges[a1[1]].append((a1[1],a1[0]))
                    weights[a1[0],a2[1]]=weights[(a1[0],i)]+weights[(i,a2[1])]
                    weights[a1[1],a2[0]]=weights[(a1[1],i)]+weights[(i,a2[0])]
            if (len(a1)==len(a2) and len(a1)==1 and len(d)==2 and a1[0]!=a2[0]):
                Edges[d[0][0]].remove(d[0])
                Edges[d[0][1]].remove(d[0])
                Edges[d[1][0]].remove(d[1])
                Edges[d[1][1]].remove(d[1])
                Edges[a1[0]].append((a1[0],a2[0]))
                Edges[a2[0]].append((a1[0],a2[0]))
                weights[a1[0],a2[0]]=weights[(a1[0],i)]+weights[(i,a2[0])]
    sch=0
    sch1=0
    for n in Edges:
        if len(Edges[n])>0:
            sch1+=1
        for e in Edges[n]:
            if e[0]==n:
                sch+=1
    print sch1,'nodes'
    print sch,'edges'
    labels={}
    for n in Edges:
        labels[n]=0
    free=1
    used=0
    for n in Edges:
        if len(Edges[n])==0:
            continue
        if labels[n]!=0:
            continue
        stack=[(n,0)]
        while len(stack)>0:
            (now,count)=stack[len(stack)-1]
            stack.pop()
            for e in Edges[now]:
                if weights[e]+count<delta:
                    if e[0]==now:
                        new=e[1]
                    else:
                        new=e[0]
                    if labels[new]!=0:
                        continue
                    labels[new]=free
                    used=1
                    labels[n]=free
                    stack.append((new,weights[e]+count))
        if used==1:
            free+=1
    lists=[]
    for i in range(free):
        lists.append([])
    for n in labels:
        if labels[n]!=0:
            lists[labels[n]].append(n)
            G.node[n]
    unite(lists,G.node,Edges,weights)
    for n in Edges:
        d=[]
        for e in Edges[n]:
            if e[0]==e[1]:
                d.append(e)
        for i in range(len(d)):
            Edges[n].remove(d[i])
    edges=[]
    sch=0
    sch1=0
    for n in Edges:
        if len(Edges[n])>0:
            sch1+=1
        for e in Edges[n]:
            if e[0]==n:
                sch+=1
    print sch1,'nodes'
    print sch,'edges'
    while 1:
        wasDeleted=0
        for n in Edges:
            if len(Edges[n])<=2:
                if (len(Edges[n])==2 and((Edges[n][0][0]==n and Edges[n][1][1]==n)or(Edges[n][1][0]==n and Edges[n][0][1]==n)))or(len(Edges[n])==1):
                    wasDeleted=1
                    for nn in Edges[n]:
                        if nn[0]==n:
                            nnn=nn[1]
                        else:
                            nnn=nn[0]
                        d=[]
                        for k in range(len(Edges[nnn])):
                            if Edges[nnn][k][0]==n or Edges[nnn][k][1]==n:
                                d.append(Edges[nnn][k])
                        for k in range(len(d)):
                            Edges[nnn].remove(d[k])
                    Edges[n]=[]
        if wasDeleted==0:
            break
    sch=0
    sch1=0
    for n in Edges:
        if len(Edges[n])>0:
            sch1+=1
        for e in Edges[n]:
            if e[0]==n:
                sch+=1
    print sch1,'nodes'
    print sch,'edges'
    groups={}
    for n in Edges:
        groups[n]=0
    cool=1
    free=1
    count=0
    for n in Edges:
        if len(Edges[n])==0:
            continue
        if groups[n]!=0:
            continue
        stack=[n]
        while len(stack)>0:
            if count==0:
                count=1
                cool=free
            else:
                if cool==free:
                    count+=1
                else:
                    count-=1
            now=stack[len(stack)-1]
            groups[now]=free
            stack.pop()
            for e in Edges[now]:
                if e[0]==now:
                    new=e[1]
                else:
                    new=e[0]
                if groups[new]!=0:
                    continue
                groups[new]=free
                stack.append(new)
        free+=1        
    newNodes=[]
    for n in Edges:
        if groups[n]!=cool:
            Edges[n]=[]
        else:
            newNodes.append(n)
    sch=0
    sch1=0
    for n in Edges:
        if len(Edges[n])>0:
            sch1+=1
        for e in Edges[n]:
            if e[0]==n:
                sch+=1
    print sch1,'nodes'
    print sch,'edges'
    nG=nx.DiGraph()
    for n in newNodes:
        nG.add_node(n,lon=G.node[n]['lon'],lat=G.node[n]['lat'])
    for n in Edges:
        for e in Edges[n]:
            nG.add_edge(e[0],e[1],weight=weights[e])
    map = smopy.Map(p[1],p[0],p[3],p[2],z=Z,margin=.1)
    return (nG,map)


def plotGraph(map,nG,roads=[]):
    xx1=[]
    yy1=[]
    xx2=[]
    yy2=[]
    edges=[]
    for i in range(len(nG.edges())):
        xx1.append(nG.node[nG.edges()[i][0]]['lat'])
        yy1.append(nG.node[nG.edges()[i][0]]['lon'])
        xx2.append(nG.node[nG.edges()[i][1]]['lat'])
        yy2.append(nG.node[nG.edges()[i][1]]['lon'])       
    plt.figure(figsize=(20,20))
    map.show_mpl(figsize=(20,20))
    px=np.array([nG.node[n]['lon'] for n in nG.node])
    py=np.array([nG.node[n]['lat'] for n in nG.node])
    (px,py)=map.to_pixels(py,px)
    X1=np.array(xx1)
    X2=np.array(xx2)
    Y1=np.array(yy1)
    Y2=np.array(yy2)
    (Y1,X1)=map.to_pixels(X1,Y1)
    (Y2,X2)=map.to_pixels(X2,Y2)
    plt.plot(px, py, 'r.')
    plt.plot([Y1,Y2],[X1,X2], color='k', linestyle='-', linewidth=0.5)
    for i in range(len(roads)):
        xx=[]
        yy=[]
        for j in range(len(roads[i][0])):
            roads[i][0][j]
            xx.append(G.node[roads[i][0][j]]['lat'])
            yy.append(G.node[roads[i][0][j]]['lon'])
        xx=np.array(xx)
        yy=np.array(yy)
        (xx,yy)=map.to_pixels(xx,yy)
        plt.plot(xx,yy,color=roads[i][1],linewidth=roads[i][2])


# 37.1839,55.5617,37.9440,55.9234#tropar
#37.3182,55.7003,37.3305,55.7078,highway_cat))#trekgorka
# 61.5784,55.0847,61.7015,55.14836,highway_cat))#kopeisk
#61.2124,55.0272,61.6093,55.2783,highway_cat))#chelyabinsk
#7.3535,55.5636,37.8548,55.9184moscow


# In[9]:




# In[1]:

# @autojit
def preCalculation(G,n1=30,n2=100,n3=100,n4=6000,c1=30,c2=70,c3=70,c4=4,cc2=3,cc3=2,cc4=2):

    
    
    
    
    
    
    ################################################################################
    ## WARNING!!! UGLY CODE, BUT WORKS PERFECTLY!!! PLEASE DO NOT LOOK AT THIS !!!##
    ################################################################################
    
    Numbers=[n1]
    heaps={}
    Edges={}
    edges=[]
    weights={}
    for n in G.nodes():
        Edges[n]=[]
    for e in G.edges():
        Edges[e[0]].append(e)
        Edges[e[1]].append(e)
        edges.append(e)
    for n in G.nodes():
        for n2 in G.edge[n]:
            weights[(n,n2)]=G.edge[n][n2]['weight']
            weights[(n2,n)]=G.edge[n][n2]['weight']
    for n in Edges:
        heaps[n]=0
    free=0
    for n in Edges:
        if len(Edges[n])==0:
            continue
        if heaps[n]<1:
            free+=1
            queue=[n]
            count=0
            pts=[]
            p1=0
            p2=1
            while p2>p1 and count<Numbers[0]:
                now=queue[p1]
                p1+=1
                if heaps[now]>0:
                    continue
                count+=1
                pts.append(now)
                heaps[now]=free
                for nn in Edges[now]:
                    if nn[0]==now:
                        new=nn[1]
                    else:
                        new=nn[0]
                    if heaps[new]<1 and len(Edges[new])>0:
                        queue.append(new)
                        p2+=1
            if count<c1:
                free-=1
                for p in pts:
                    heaps[p]=-1
    was={}
    for n in Edges:
        was[n]='1'
    for n in Edges:
        if heaps[n]==-1:
            queue=[n]
            p1=0
            p2=1
            while p2>p1:
                now=queue[p1]
                was[now]=n
                if heaps[now]>0:
                    heaps[n]=heaps[now]
                    break
                for nn in Edges[now]:
                    if nn[0]==now:
                        new=nn[1]
                    else:
                        new=nn[0]
                    if len(Edges[new])>0 and was[new]!=n:
                        queue.append(new)
                        p2+=1
                p1+=1
    for n in Edges:
        if heaps[n]==-1:
            print n,Edges[n],groups[n],cool
    free+=1
    Heaps=[]
    for i in range(free):
        Heaps.append([])
    for n in Edges:
        if heaps[n]>0:
            Heaps[heaps[n]].append(n)
    Borders=[]
    PersonalBorders=[]
    for i in range(len(Heaps)):
        PersonalBorders.append([])
        Borders.append([])
        for j in range(len(Heaps)):
            Borders[i].append([])
    for e in edges:
        if heaps[e[0]]!=heaps[e[1]] and heaps[e[0]]>0 and heaps[e[1]]>0:
            Borders[heaps[e[0]]][heaps[e[1]]].append((e[0],e[1]))
            Borders[heaps[e[1]]][heaps[e[0]]].append((e[1],e[0]))
            PersonalBorders[heaps[e[0]]].append(e[0])
            PersonalBorders[heaps[e[1]]].append(e[1])
            inf=100000000000.
            Paths=[]
            Ids=[]
            ids=[]
            for h in range(len(Heaps)):
                Paths.append([])
                Ids.append({})
                ids.append({})
                for i in range(len(Heaps[h])):
                    Ids[h][i]=Heaps[h][i]
                    ids[h][Heaps[h][i]]=i
                for i in range(len(Heaps[h])):
                    Paths[h].append([])
                    for j in range(len(Heaps[h])):
                        if i==j:
                            Paths[h][i].append((0,[Ids[h][i]]))
                        else:
                            Paths[h][i].append((inf,[]))
                    for e in Edges[Ids[h][i]]:
                        if e[0]==Ids[h][i] and (heaps[e[1]]==h and heaps[e[0]]==h):######
                            Paths[h][i][ids[h][e[1]]]=(weights[e],[e[0],e[1]])
                for k in range(len(Heaps[h])):
                    for i in range(len(Heaps[h])):
                        for j in range(len(Heaps[h])):
                            if Paths[h][i][j][0]>Paths[h][i][k][0]+Paths[h][k][j][0]:
                                newPath=list(Paths[h][i][k][1])
                                newPath.pop()
                                newPath.extend(Paths[h][k][j][1])
                                Paths[h][i][j]=(Paths[h][i][k][0]+Paths[h][k][j][0],newPath)            


    Numbers=[n1,n2]
    heaps2={}
    for i in range(len(Heaps)):
        heaps2[i]=0
    free=0
    for i in range(len(Heaps)):
        if heaps2[i]<1:
            free+=1
            queue=[i]
            count=0
            count2=0
            pts=[]
            p1=0
            p2=1
            while p2>p1 and count<Numbers[1]:
                now=queue[p1]
                p1+=1
                if heaps2[now]>0:
                    continue
                count+=len(PersonalBorders[now])
                count2+=1
                pts.append(now)
                heaps2[now]=free
                for j in range(len(Heaps)):
                    if len(Borders[i][j])>0:
                        if heaps2[j]<1:
                            queue.append(j)    
                            p2+=1
            if count<c1 or count2<cc2 or count>500:
                free-=1
                for p in pts:
                    heaps2[p]=-1
    #find closest heaps for everybody
    was={}
    for i in range(len(Heaps)):
        was[i]=-1
    for i in range(1,len(Heaps)):
        if heaps2[i]==-1:
            queue=[i]
            p1=0
            p2=1
            while p2>p1:
                now=queue[p1]
                was[now]=i
                if heaps2[now]>0:
                    heaps2[i]=heaps2[now]
                    break
                for j in range(len(Heaps)):
                    if len(Borders[i][j])>0:
                        if was[j]!=i:
                            queue.append(j)    
                            p2+=1
                p1+=1
            if heaps2[i]==-1:
                free+=1
                heaps2[i]=free
    #ok
    free+=1
    Heaps2=[]
    for i in range(free):
        Heaps2.append([])
    for i in range(len(Heaps)):
#         if heaps2[i]>0:
        for j in range(len(PersonalBorders[i])):
            Heaps2[heaps2[i]].append(PersonalBorders[i][j])
    for i in range(len(Heaps2)):
        distinct={}
        for j in range(len(Heaps2[i])):
            distinct[Heaps2[i][j]]=1
        Heaps2[i]=[]
        for n in distinct:
            Heaps2[i].append(n)
    
    Borders2=[]
    PersonalBorders2=[]
    for i in range(len(Heaps2)):
        PersonalBorders2.append([])
        Borders2.append([])
        for j in range(len(Heaps2)):
            Borders2[i].append([])
    NewNodes={}
    for i in range(len(Heaps)):
        for j in range(len(PersonalBorders[i])):
            NewNodes[PersonalBorders[i][j]]=1
    for e in edges:
        if heaps2[heaps[e[0]]]!=heaps2[heaps[e[1]]]:#something very extra has been added
            NewNodes[e[0]]=1
            NewNodes[e[1]]=1


            Borders2[heaps2[heaps[e[0]]]][heaps2[heaps[e[1]]]].append((e[0],e[1]))
            Borders2[heaps2[heaps[e[1]]]][heaps2[heaps[e[0]]]].append((e[1],e[0]))

            PersonalBorders2[heaps2[heaps[e[0]]]].append(e[0])
            PersonalBorders2[heaps2[heaps[e[1]]]].append(e[1])
            
    Paths2=[]
    Ids2=[]
    ids2=[]
    for h in range(len(Heaps2)):
        Paths2.append([])
        Ids2.append({})
        ids2.append({})
        for i in range(len(Heaps2[h])):
            Ids2[h][i]=Heaps2[h][i]
            ids2[h][Heaps2[h][i]]=i
        for i in range(len(Heaps2[h])):
            Paths2[h].append([])
            for j in range(len(Heaps2[h])):
                if i==j:
                    Paths2[h][i].append((0,[Ids2[h][i]]))
                else:
                    Paths2[h][i].append((inf,[]))
        for i in range(len(Heaps)):
            for j in range(len(PersonalBorders[i])):
                if heaps2[heaps[PersonalBorders[i][0]]]==h:
                    for k in range(len(PersonalBorders[i])):
                        if j!=k:                        
                            Paths2[h][ids2[h][PersonalBorders[i][j]]][ids2[h][PersonalBorders[i][k]]]=Paths[i][ids[i][PersonalBorders[i][j]]][ids[i][PersonalBorders[i][k]]]
            for j in range(len(Borders[i])):
                for k in range(len(Borders[i][j])):
                    if heaps2[heaps[Borders[i][j][k][0]]]==h:
                        Paths2[h][ids2[h][Borders[i][j][k][0]]][ids2[h][Borders[i][j][k][1]]]=(weights[Borders[i][j][k]],[Borders[i][j][k][0],Borders[i][j][k][1]])
    for h in range(len(Heaps2)):
        for k in range(len(Heaps2[h])):
            for i in range(len(Heaps2[h])):
                for j in range(len(Heaps2[h])):
                    if Paths2[h][i][j][0]>Paths2[h][i][k][0]+Paths2[h][k][j][0]:
                        newPath=list(Paths2[h][i][k][1])
                        newPath.pop()
                        newPath.extend(Paths2[h][k][j][1])
                        Paths2[h][i][j]=(Paths2[h][i][k][0]+Paths2[h][k][j][0],newPath)
                        
    Numbers=[n1,n2,n3]
    heaps3={}
    for i in range(len(Heaps2)):
        heaps3[i]=0
    free=0
    for i in range(len(Heaps2)):
        if heaps3[i]<1:
            free+=1
            queue=[i]
            count=0
            count2=0
            pts=[]
            p1=0
            p2=1
            while p2>p1 and count<Numbers[2]:
                now=queue[p1]
                p1+=1
                if heaps3[now]>0:
                    continue
                count+=len(PersonalBorders2[now])
                count2+=1
                pts.append(now)
                heaps3[now]=free
                for j in range(len(Heaps2)):
                    if len(Borders2[i][j])>0:
                        if heaps3[j]<1:
                            queue.append(j)    
                            p2+=1
            if count<c3 or count2<cc3 or count>500:
                free-=1
                for p in pts:
                    heaps3[p]=-1
    #find closest heaps for everybody
    was={}
    for i in range(len(Heaps2)):
        was[i]=-1
    for i in range(1,len(Heaps2)):
        if heaps3[i]==-1:
            queue=[i]
            p1=0
            p2=1
            while p2>p1:
                now=queue[p1]
                was[now]=i
                if heaps3[now]>0:
                    heaps3[i]=heaps3[now]
                    break
                for j in range(len(Heaps2)):
                    if len(Borders2[i][j])>0:
                        if was[j]!=i:
                            queue.append(j)    
                            p2+=1
                p1+=1
            if heaps3[i]==-1:
                free+=1
                heaps3[i]=free
    #ok
    free+=1
    Heaps3=[]
    for i in range(free):
        Heaps3.append([])
    for i in range(len(Heaps2)):
        if heaps3[i]>0:
            for j in range(len(PersonalBorders2[i])):
                Heaps3[heaps3[i]].append(PersonalBorders2[i][j])
    for i in range(len(Heaps3)):
        distinct={}
        for j in range(len(Heaps3[i])):
            distinct[Heaps3[i][j]]=1
        Heaps3[i]=[]
        for n in distinct:
            Heaps3[i].append(n)

    Borders3=[]
    PersonalBorders3=[]
    for i in range(len(Heaps3)):
        PersonalBorders3.append([])
        Borders3.append([])
        for j in range(len(Heaps3)):
            Borders3[i].append([])
    NewNodes={}
    for i in range(len(Heaps)):
        for j in range(len(PersonalBorders[i])):
            NewNodes[PersonalBorders[i][j]]=1
    for e in edges:
        if heaps2[heaps[e[0]]]!=-1 and heaps2[heaps[e[1]]]!=-1 and heaps3[heaps2[heaps[e[0]]]]!=heaps3[heaps2[heaps[e[1]]]]:#something very extra has been added
            NewNodes[e[0]]=1
            NewNodes[e[1]]=1

            Borders3[heaps3[heaps2[heaps[e[0]]]]][heaps3[heaps2[heaps[e[1]]]]].append(e[0])
            Borders3[heaps3[heaps2[heaps[e[1]]]]][heaps3[heaps2[heaps[e[0]]]]].append(e[1])

            PersonalBorders3[heaps3[heaps2[heaps[e[0]]]]].append(e[0])
            PersonalBorders3[heaps3[heaps2[heaps[e[1]]]]].append(e[1])


    Paths3=[]
    Ids3=[]
    ids3=[]
    for h in range(len(Heaps3)):
        Paths3.append([])
        Ids3.append({})
        ids3.append({})
        for i in range(len(Heaps3[h])):
            Ids3[h][i]=Heaps3[h][i]
            ids3[h][Heaps3[h][i]]=i
        for i in range(len(Heaps3[h])):
            Paths3[h].append([])
            for j in range(len(Heaps3[h])):
                if i==j:
                    Paths3[h][i].append((0,[Ids3[h][i]]))
                else:
                    Paths3[h][i].append((inf,[]))

    for h in range(len(Heaps3)):
        for i in range(len(Heaps2)):
                for j in range(len(PersonalBorders2[i])):
                    if heaps2[heaps[PersonalBorders2[i][0]]]==h:
                        for k in range(len(PersonalBorders2[i])):
                            if j!=k:                        
                                Paths3[h][ids3[h][PersonalBorders2[i][j]]][ids3[h][PersonalBorders2[i][k]]]=Paths2[i][ids2[i][PersonalBorders2[i][j]]][ids2[i][PersonalBorders2[i][k]]]
                for j in range(len(Borders2[i])):
                    for k in range(len(Borders2[i][j])):
                        if heaps3[heaps2[heaps[Borders2[i][j][k][0]]]]==h:
                            Paths3[h][ids3[h][Borders2[i][j][k][0]]][ids3[h][Borders2[i][j][k][1]]]=(weights[Borders2[i][j][k]],[Borders2[i][j][k][0],Borders2[i][j][k][1]])


        for k in range(len(Heaps3[h])):
            for i in range(len(Heaps3[h])):
                for j in range(len(Heaps3[h])):
                    if Paths3[h][i][j][0]>Paths3[h][i][k][0]+Paths3[h][k][j][0]:
                        newPath=list(Paths3[h][i][k][1])
                        newPath.pop()
                        newPath.extend(Paths3[h][k][j][1])
                        Paths3[h][i][j]=(Paths3[h][i][k][0]+Paths3[h][k][j][0],newPath)

    
    
    Numbers=[n1,n2,n3,n4]
    heaps4={}
    for i in range(len(Heaps3)):
        heaps4[i]=0
    free=0
    for i in range(len(Heaps3)):
        if heaps4[i]<1:
            free+=1
            queue=[i]
            count=0
            count2=0
            pts=[]
            p1=0
            p2=1
            while p2>p1 and count<Numbers[3]:
                now=queue[p1]
                p1+=1
                if heaps4[now]>0:
                    continue
                count+=len(PersonalBorders3[now])
                count2+=1
                pts.append(now)
                heaps4[now]=free
                for j in range(len(Heaps3)):
                    if len(Borders3[i][j])>0:
                        if heaps4[j]<1:
                            queue.append(j)    
                            p2+=1
            if count<c4 or count2<cc4 or count<400:
                free-=1
                for p in pts:
                    heaps4[p]=-1
    #find closest heaps for everybody
    was={}
    for i in range(len(Heaps3)):
        was[i]=-1
    for i in range(1,len(Heaps3)):
        if heaps4[i]==-1:
            queue=[i]
            p1=0
            p2=1
            while p2>p1:
                now=queue[p1]
                was[now]=i
                if heaps4[now]>0:
                    heaps4[i]=heaps4[now]
                    break
                for j in range(len(Heaps3)):
                    if len(Borders3[i][j])>0:
                        if was[j]!=i:
                            queue.append(j)    
                            p2+=1
                p1+=1
            if heaps4[i]==-1:
                free+=1
                heaps4[i]=free
    #ok
    free+=1
    Heaps4=[]
    for i in range(free):
        Heaps4.append([])
    for i in range(len(Heaps3)):
        if heaps4[i]>0:
            for j in range(len(PersonalBorders3[i])):
                Heaps4[heaps4[i]].append(PersonalBorders3[i][j])
    for i in range(len(Heaps4)):
        distinct={}
        for j in range(len(Heaps4[i])):
            distinct[Heaps4[i][j]]=1
        Heaps4[i]=[]
        for n in distinct:
            Heaps4[i].append(n)
    Borders4=[]
    PersonalBorders4=[]
    for i in range(len(Heaps4)):
        PersonalBorders4.append([])
        Borders4.append([])
        for j in range(len(Heaps4)):
            Borders4[i].append([])
    NewNodes={}
    for i in range(len(Heaps)):
        for j in range(len(PersonalBorders[i])):
            NewNodes[PersonalBorders[i][j]]=1
    for e in edges:
        if heaps2[heaps[e[0]]]!=-1 and heaps2[heaps[e[1]]]!=-1 and heaps4[heaps3[heaps2[heaps[e[0]]]]]!=heaps4[heaps3[heaps2[heaps[e[1]]]]]:#something very extra has been added
            NewNodes[e[0]]=1
            NewNodes[e[1]]=1


            Borders4[heaps4[heaps3[heaps2[heaps[e[0]]]]]][heaps4[heaps3[heaps2[heaps[e[1]]]]]].append(e[0])
            Borders4[heaps4[heaps3[heaps2[heaps[e[1]]]]]][heaps4[heaps3[heaps2[heaps[e[0]]]]]].append(e[1])

            PersonalBorders4[heaps4[heaps3[heaps2[heaps[e[0]]]]]].append(e[0])
            PersonalBorders4[heaps4[heaps3[heaps2[heaps[e[1]]]]]].append(e[1])
            
    Paths4=[]
    Ids4=[]
    ids4=[]
    for h in range(len(Heaps4)):
        Paths4.append([])
        Ids4.append({})
        ids4.append({})
        for i in range(len(Heaps4[h])):
            Ids4[h][i]=Heaps4[h][i]
            ids4[h][Heaps4[h][i]]=i
        for i in range(len(Heaps4[h])):
            Paths4[h].append([])
            for j in range(len(Heaps4[h])):
                if i==j:
                    Paths4[h][i].append((0,[Ids4[h][i]]))
                else:
                    Paths4[h][i].append((inf,[]))
 
        for i in range(len(Heaps3)):
                for j in range(len(PersonalBorders3[i])):
                    if heaps2[heaps[PersonalBorders3[i][0]]]==h:
                        for k in range(len(PersonalBorders3[i])):
                            if j!=k:                        
                                Paths4[h][ids4[h][PersonalBorders3[i][j]]][ids4[h][PersonalBorders3[i][k]]]=Paths3[i][ids3[i][PersonalBorders3[i][j]]][ids3[i][PersonalBorders3[i][k]]]
                for j in range(len(Borders3[i])):
                    for k in range(len(Borders3[i][j])):
                        if heaps4[heaps3[heaps2[heaps[Borders2[i][j][k][0]]]]]==h:
                            Paths4[h][ids4[h][Borders3[i][j][k][0]]][ids4[h][Borders3[i][j][k][1]]]=(weights[Borders3[i][j][k]],[Borders3[i][j][k][0],Borders3[i][j][k][1]])
    
        for k in range(len(Heaps4[h])):
            for i in range(len(Heaps4[h])):
                for j in range(len(Heaps4[h])):
                    if Paths4[h][i][j][0]>Paths4[h][i][k][0]+Paths4[h][k][j][0]:
                        newPath=list(Paths4[h][i][k][1])
                        newPath.pop()
                        newPath.extend(Paths4[h][k][j][1])
                        Paths4[h][i][j]=(Paths4[h][i][k][0]+Paths4[h][k][j][0],newPath)
    res={'PersonalBorders':PersonalBorders,'PersonalBorders2':PersonalBorders2,'PersonalBorders3':PersonalBorders3,'PersonalBorders4':PersonalBorders4}
    res['Paths4']=Paths4
    res['Paths3']=Paths3
    res['Paths2']=Paths2
    res['Paths']=Paths
    res['ids4']=ids4
    res['ids3']=ids3
    res['ids2']=ids2
    res['ids']=ids
    res['Ids4']=Ids4
    res['Ids3']=Ids3
    res['Ids2']=Ids2
    res['Ids']=Ids
    res['Heaps4']=Heaps4
    res['Heaps3']=Heaps3
    res['Heaps2']=Heaps2
    res['Heaps']=Heaps
    res['heaps4']=heaps4
    res['heaps3']=heaps3
    res['heaps2']=heaps2
    res['heaps']=heaps
    return res

def shortestPath(calc,start,finish):
    heaps=calc['heaps']
    heaps2=calc['heaps2']
    heaps3=calc['heaps3']
    heaps4=calc['heaps4']
    Heaps=calc['Heaps']
    Heaps2=calc['Heaps2']
    Heaps3=calc['Heaps3']
    Heaps4=calc['Heaps4']
    Ids=calc['Ids']
    Ids2=calc['Ids2']
    Ids3=calc['Ids3']
    Ids4=calc['Ids4']
    ids=calc['ids']
    ids2=calc['ids2']
    ids3=calc['ids3']
    ids4=calc['ids4']
    Paths4=calc['Paths4']
    Paths3=calc['Paths3']
    Paths2=calc['Paths2']
    Paths=calc['Paths']
    PersonalBorders=calc['PersonalBorders']
    PersonalBorders2=calc['PersonalBorders2']
    PersonalBorders3=calc['PersonalBorders3']
    PersonalBorders4=calc['PersonalBorders4']
    inf=1000000000
    if heaps[start]==heaps[finish]:
        return Paths[heaps[start]][ids[heaps[start]][start]][ids[heaps[start]][finish]]
    res1={}
    for b in PersonalBorders[heaps[start]]:
        res1[b]=Paths[heaps[start]][ids[heaps[start]][start]][ids[heaps[start]][b]]
    if heaps2[heaps[start]]==heaps2[heaps[finish]]:
        res2={}
        for b in PersonalBorders[heaps[finish]]:
            res2[b]=(inf,[])
        for b1 in res1:
            for b2 in PersonalBorders[heaps[finish]]:
                newDist=res1[b1][0]+Paths2[heaps2[heaps[start]]][ids2[heaps2[heaps[start]]][b1]][ids2[heaps2[heaps[start]]][b2]][0]
                if newDist<res2[b2][0]:
                    newPath=list(res1[b1][1])
                    newPath.pop()
                    newPath.extend(Paths2[heaps2[heaps[start]]][ids2[heaps2[heaps[start]]][b1]][ids2[heaps2[heaps[start]]][b2]][1])
                    res2[b2]=(newDist,newPath)
        res3=(inf,[])
        for b2 in res2:
            newDist=res2[b2][0]+Paths[heaps[finish]][ids[heaps[finish]][b2]][ids[heaps[finish]][finish]][0]
            if newDist<res3[0]:
                newPath=list(res2[b2][1])
                newPath.pop()
                newPath.extend(Paths[heaps[finish]][ids[heaps[finish]][b2]][ids[heaps[finish]][finish]][1])
                res3=(newDist,newPath)
        return res3
    res2={}
    for b in PersonalBorders2[heaps2[heaps[start]]]:
        res2[b]=(inf,[])
    for b1 in res1:
        for b2 in PersonalBorders2[heaps2[heaps[start]]]:
            newDist=res1[b1][0]+Paths2[heaps2[heaps[start]]][ids2[heaps2[heaps[start]]][b1]][ids2[heaps2[heaps[start]]][b2]][0]
            if newDist<res2[b2][0]:
                newPath=list(res1[b1][1])
                newPath.pop()
                newPath.extend(Paths2[heaps2[heaps[start]]][ids2[heaps2[heaps[start]]][b1]][ids2[heaps2[heaps[start]]][b2]][1])
                res2[b2]=(newDist,newPath)
    if heaps3[heaps2[heaps[start]]]==heaps3[heaps2[heaps[finish]]]:
        res3={}
        for b in PersonalBorders2[heaps2[heaps[finish]]]:
            res3[b]=(inf,[])
        for b2 in res2:
            for b3 in PersonalBorders2[heaps2[heaps[finish]]]:
                newDist=res2[b2][0]+Paths3[heaps3[heaps2[heaps[start]]]][ids3[heaps3[heaps2[heaps[start]]]][b2]][ids3[heaps3[heaps2[heaps[start]]]][b3]][0]
                if newDist<res3[b3][0]:
                    newPath=list(res2[b2][1])
                    newPath.pop()
                    newPath.extend(Paths3[heaps3[heaps2[heaps[start]]]][ids3[heaps3[heaps2[heaps[start]]]][b2]][ids3[heaps3[heaps2[heaps[start]]]][b3]][1])
                    res3[b3]=(newDist,newPath)
        res4={}
        for b in PersonalBorders[heaps[finish]]:
            res4[b]=(inf,[])
        for b3 in res3:
            for b4 in PersonalBorders[heaps[finish]]:
                newDist=res3[b3][0]+Paths2[heaps2[heaps[finish]]][ids2[heaps[finish]][b3]][ids2[heaps[finish]][b4]][0]
                if newDist<res4[b4][0]:
                    newPath=list(res3[b3][1])
                    newPath.pop()
                    newPath.extend(Paths2[heaps2[heaps[finish]]][ids2[heaps[finish]][b3]][ids2[heaps[finish]][b4]][1])
                    res4[b4]=(newDist,newPath)
        res5=(inf,[])
        for b4 in res4:
            newDist=res4[b4][0]+Paths[heaps[finish]][ids[heaps[finish]][b4]][ids[heaps[finish]][finish]][0]
            if newDist<res5[0]:
                newPath=list(res4[b4][1])
                newPath.pop()
                newPath.extend(Paths[heaps[finish]][ids[heaps[finish]][b4]][ids[heaps[finish]][finish]][1])
                res5=(newDist,newPath)
        return res5
    res3={}
    for b in PersonalBorders3[heaps3[heaps2[heaps[start]]]]:
        res3[b]=(inf,[])
    for b2 in res2:
        for b3 in PersonalBorders3[heaps3[heaps2[heaps[start]]]]:
            newDist=res2[b2][0]+Paths3[heaps3[heaps2[heaps[start]]]][ids3[heaps3[heaps2[heaps[start]]]][b2]][ids3[heaps3[heaps2[heaps[start]]]][b3]][0]
            if newDist<res3[b3][0]:
                newPath=list(res2[b2][1])
                newPath.pop()
                newPath.extend(Paths3[heaps3[heaps2[heaps[start]]]][ids3[heaps3[heaps2[heaps[start]]]][b2]][ids3[heaps3[heaps2[heaps[start]]]][b3]][1])
                res3[b3]=(newDist,newPath)
    if heaps4[heaps3[heaps2[heaps[start]]]]==heaps4[heaps3[heaps2[heaps[finish]]]]:
        res4={}
        for b in PersonalBorders3[heaps3[heaps2[heaps[finish]]]]:
            res4[b]=(inf,[])
        for b3 in res3:
            for b4 in PersonalBorders3[heaps3[heaps2[heaps[finish]]]]:
                newDist=res3[b3][0]+Paths4[heaps4[heaps3[heaps2[heaps[start]]]]][ids4[heaps4[heaps3[heaps2[heaps[start]]]]][b3]][ids4[heaps4[heaps3[heaps2[heaps[start]]]]][b4]][0]
                if newDist<res4[b4][0]:
                    newPath=list(res3[b3][1])
                    newPath.pop()
                    newPath.extend(Paths4[heaps4[heaps3[heaps2[heaps[start]]]]][ids4[heaps4[heaps3[heaps2[heaps[start]]]]][b3]][ids4[heaps4[heaps3[heaps2[heaps[start]]]]][b4]][1])
                    res4[b4]=(newDist,newPath)
        res5={}
        for b in PersonalBorders2[heaps2[heaps[finish]]]:
            res5[b]=(inf,[])
        for b4 in res4:
            for b5 in PersonalBorders2[heaps2[heaps[finish]]]:
                newDist=res4[b4][0]+Paths3[heaps3[heaps2[heaps[finish]]]][ids3[heaps3[heaps2[heaps[finish]]]][b4]][ids3[heaps3[heaps2[heaps[finish]]]][b5]][0]
                if newDist<res5[b5][0]:
                    newPath=list(res4[b4][1])
                    newPath.pop()
                    newPath.extend(Paths3[heaps3[heaps2[heaps[finish]]]][ids3[heaps3[heaps2[heaps[finish]]]][b4]][ids3[heaps3[heaps2[heaps[finish]]]][b5]][1])
                    res5[b5]=(newDist,newPath)
        res6={}
        for b in PersonalBorders[heaps[finish]]:
            res6[b]=(inf,[])
        for b5 in res5:
            for b6 in PersonalBorders[heaps[finish]]:
                newDist=res5[b5][0]+Paths2[heaps2[heaps[finish]]][ids2[heaps2[heaps[finish]]][b5]][ids2[heaps2[heaps[finish]]][b6]][0]
                if newDist<res6[b6][0]:
                    newPath=list(res5[b5][1])
                    newPath.pop()
                    newPath.extend(Paths2[heaps2[heaps[finish]]][ids2[heaps2[heaps[finish]]][b5]][ids2[heaps2[heaps[finish]]][b6]][1])
                    res6[b6]=(newDist,newPath)
        res7=(inf,[])
        for b6 in res6:
            newDist=res6[b6][0]+Paths[heaps[finish]][ids[heaps[finish]][b6]][ids[heaps[finish]][finish]][0]
            if newDist<res7[0]:
                newPath=list(res6[b6][1])
                newPath.pop()
                newPath.extend(Paths[heaps[finish]][ids[heaps[finish]][b6]][ids[heaps[finish]][finish]][1])
                res7=(newDist,newPath)
        return res7
############################################################


# In[16]:

#some initial work with map
def run():
    # (G,map)=getGraph(14,61.5784,55.0847,61.7015,55.14836,0.000025)
    (G,map)=getGraph(10,37.3535,55.5636,37.8548,55.9184,0.0025)
    # output = open('moscowg.txt','wb')
    # cPickle.dump(calc, output)
    # output.close()
    # inputF = open('map.txt','rb')
    # (G,map)=cPickle.load(inputF)
    # inputF.close()

    plotGraph(map,G)

    # print len(G.nodes())
    # listt=[[37,20],[200,464],[557,400],[42,708],[427,4],[17,80],[3,90]]
    # coolList=[]
    # for i in range(len(listt)):
    #     coolList.append(([G.nodes()[listt[i][0]],G.nodes()[listt[i][1]]],'r',4))
    # plotGraph(map,G,coolList)
    # trips=[[37,427,20,4],[3,200,90,464],[557,400],[17,80]]
    # newCoolList=[]
    # for t in range(len(trips)):
    #     now=[]
    #     for t2 in range(len(trips[t])):
    #         now.append(trips[t][t2])
    #     path=[]
    #     for n in range(len(now)-1):
    #         result=nx.shortest_path(G,G.nodes()[now[n]],G.nodes()[now[n+1]])
    #         path.extend(result)
    #     if t%2==0:
    #         c='r'
    #     else:
    #         c='c'
    #     if t/2%2==0:
    #         w=8
    #     else:
    #         w=4
    #     newCoolList.append((path,c,w))
    # plotGraph(map,G,newCoolList)


def comparePathFindings():#you should know map and G
    calc=preCalculation(G)
    # output = open('calc.txt','wb')
    # cPickle.dump(calc, output)
    # output.close()
    # inputF = open('calc.txt','rb')
    # calc=cPickle.load(inputF)
    # inputF.close()



    # shortestPath(G.nodes()[0],G.nodes()[20])
    # print shortestPath(calc,G.nodes()[15],G.nodes()[20])[0]
    # print nx.shortest_path_length(G,G.nodes()[15],G.nodes()[20],'weight')
    l=shortestPath(calc,G.nodes()[15],G.nodes()[20])[1]
    # print l
    plotGraph(map,G,[(shortestPath(calc,G.nodes()[15],G.nodes()[20])[1],'r',4)])
    plotGraph(map,G,[(nx.shortest_path(G,G.nodes()[15],G.nodes()[20],'weight'),'r',4)])
    # print heaps[G.nodes()[17]],heaps[G.nodes()[20]]
    # print PersonalBorders[1]
    # print G.nodes()[17]

    # print nx.shortest_path(G,G.nodes()[9],G.nodes()[18],'weight')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



