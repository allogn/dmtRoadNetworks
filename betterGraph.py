
# coding: utf-8

# In[42]:

import cPickle, gzip, math, random
import numpy as np
from numba import autojit
import networkx as nx
import xml.sax
import copy
import matplotlib.pyplot as plt
import smopy
get_ipython().magic(u'matplotlib inline')

        
"""
Read graphs in Open Street Maps osm format
Based on osm.py from brianw's osmgeocode
http://github.com/brianw/osmgeocode, which is based on osm.py from
comes from Graphserver:
http://github.com/bmander/graphserver/tree/master and is copyright (c)
2007, Brandon Martin-Anderson under the BSD License
"""

import xml.sax
import copy
import networkx

def download_osm(left,bottom,right,top,highway_cat):
    """
    Downloads OSM street (only highway-tagged) Data using a BBOX, 
    plus a specification of highway tag values to use

    Parameters
    ----------
    left,bottom,right,top : BBOX of left,bottom,right,top coordinates in WGS84
    highway_cat : highway tag values to use, separated by pipes (|), for instance 'motorway|trunk|primary'

    Returns
    ----------
    stream object with osm xml data

    """

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
    """Read graph in OSM format from file specified by name or by stream object.

    Parameters
    ----------
    filename_or_stream : filename or stream object

    Returns
    -------
    G : Graph

    Examples
    --------
    >>> G=nx.read_osm(nx.download_osm(-122.33,47.60,-122.31,47.61))
    >>> plot([G.node[n]['data'].lat for n in G], [G.node[n]['data'].lon for n in G], ',')

    """
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
def getGraph(x1,y1,x2,y2,delta=0.005):
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
    delta=0.000005
    cut=0
    edges=G.edges()
    print len(edges),'edges'
    print len(G.node),'nodes'
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
    lists=[]
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
    for n in Edges:
        if groups[n]!=cool:
            Edges[n]=[]
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
                if weights[e]+count<delta*5:
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
    nG=nx.DiGraph()
    for n in newNodes:
        nG.add_node(n,lon=G.node[n]['lon'],lat=G.node[n]['lat'])
    for n in Edges:
        for e in Edges[n]:
            nG.add_edge(e[0],e[1],weight=weights[e])
    return nG


def plotGraph(x1,y1,x2,y2,nG):
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
    map = smopy.Map(p[1],p[0],p[3],p[2],z=15,margin=.1)
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
    
    
    
# G=getGraph(37.4721,55.6451,37.6230,55.7092,0.005)
# plotGraph(37.4721,55.6451,37.6230,55.7092,G)


#37.4721,55.6451,37.6230,55.7092#troparevo
#37.3182,55.7003,37.3305,55.7078,highway_cat))#trekgorka
# 61.5784,55.0847,61.7015,55.14836,highway_cat))#kopeisk
#61.2124,55.0272,61.6093,55.2783,highway_cat))#chelyabinsk
#7.3535,55.5636,37.8548,55.9184moscow


# In[43]:




# In[ ]:

#37.3182,55.7003,37.3305,55.7078,highway_cat))#trekgorka
# 61.5784,55.0847,61.7015,55.14836,highway_cat))#kopeisk
#61.2124,55.0272,61.6093,55.2783,highway_cat))#chelyabinsk
#7.3535,55.5636,37.8548,55.9184moscow
# @autojit
# def abss():
#     for i in range(3000):
#         print i

