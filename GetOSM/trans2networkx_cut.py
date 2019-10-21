import networkx as nx
'''from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse('example.edg.xml')
collection = DOMTree.documentElement
edges = collection.getElementsByTagName("edge")
for edge in edges:
    if edge.hasAttribute("id"):
        print(edge.attrib)'''
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import time
import numpy as np
import pickle
import os
def mkdir(path):
 
    folder = os.path.exists(path)
 
    if not folder:
        os.makedirs(path)
        print ("---  new folder...  ---")
    else:
        print ("---  There is this folder!  ---")

def convert(xmlfile):
    start = time.time()
    tree_n = ET.parse(xmlfile + "/osm.net.xml")
    print(xmlfile)
    print(xmlfile + "/osm.net.xml")

    root_n = tree_n.getroot()
    cur_id = None
    abstract_G = nx.MultiDiGraph()
    abstract_pos = {}
    mkdir(xmlfile+"/pklfile")
    for element in root_n:
        if(element.tag=='edge'):
            if 'function' in element.attrib and element.attrib['function']=='internal':   
                new_cur_id = element.attrib['id'].lstrip(':').split('_')[0]
            else:
                new_cur_id = element.attrib['id']
            if new_cur_id!=cur_id:
                if cur_id!=None and cur_id != 'cluster':
                    info = {}
                    #nx.draw(G,pos)
                    nodes = list(G.nodes())
                    nodes_dic = {}
                    for i in range(len(nodes)):
                        nodes_dic[nodes[i]] = i
                    info['nodes'] = nodes_dic
                    pos_matrix  = np.zeros((2,len(pos)))
                    for i in range(len(nodes)):
                        pos_matrix[0,i]=pos[nodes[i]][0]
                        pos_matrix[1,i]=pos[nodes[i]][1]
                    info['pos_matrix'] = pos_matrix
                    adj_matrix = nx.to_numpy_matrix(G)
                    info['adj_matrix'] = adj_matrix
                    sources = []
                    targets = []
                    for i in range(len(nodes)):
                        if G.in_degree(nodes[i])==0:
                            sources.append(i)
                        if G.out_degree(nodes[i])==0:
                            targets.append(i)
                    info['sources'] = sources
                    info['targets'] = targets

                    f = open(xmlfile + '/pklfile/%s.pkl'%cur_id,'wb')
                    pickle.dump(info,f)
                    mean_x = 0.0
                    mean_y = 0.0
                    for item in pos:
                        mean_x+=pos[item][0]
                        mean_y+=pos[item][1]
                    mean_x/=len(pos)
                    mean_y/=len(pos)
                    abstract_G.add_node(cur_id)
                    abstract_pos[cur_id]=(mean_x,mean_y)
                    #plt.show()
                cur_id = new_cur_id
                G = nx.MultiDiGraph()
                pos = {}
            else:
                pass
            for lane in element:
                try:
                    shape = lane.attrib['shape']
                    shape = shape.split(' ')
                    attrib = lane.attrib
                    attrib.pop('shape')
                except:
                    print(lane.attrib)
                last = None
                for i in range(len(shape)):
                    cur_pos = shape[i].split(',')
                    pos_x = float(cur_pos[0])
                    pos_y = float(cur_pos[1])
                    node_name = 'X:'+str(pos_x)+'/Y:'+str(pos_y)
                    pos[node_name] = (pos_x,pos_y)
                    G.add_nodes_from([(node_name)])
                    if last!=None:
                        G.add_edges_from([(last,node_name,attrib)])
                    last = node_name

    else:
        abstract_G.add_node(cur_id)
        info = {}
        #nx.draw(G,pos)
        nodes = list(G.nodes())
        nodes_dic = {}
        for i in range(len(nodes)):
            nodes_dic[nodes[i]] = i
        info['nodes'] = nodes_dic
        pos_matrix  = np.zeros((2,len(pos)))
        for i in range(len(nodes)):
            pos_matrix[0,i]=pos[nodes[i]][0]
            pos_matrix[1,i]=pos[nodes[i]][1]
        info['pos_matrix'] = pos_matrix
        adj_matrix = nx.to_numpy_matrix(G)
        info['adj_matrix'] = adj_matrix
        sources = []
        targets = []
        for i in range(len(nodes)):
            if G.in_degree(nodes[i])==0:
                sources.append(i)
            if G.out_degree(nodes[i])==0:
                targets.append(i)
        info['sources'] = sources
        info['targets'] = targets
        f = open(xmlfile + '/pklfile/%s.pkl'%cur_id,'wb')
        pickle.dump(info,f)
        mean_x = 0.0
        mean_y = 0.0
        for item in pos:
            mean_x+=pos[item][0]
            mean_y+=pos[item][1]
        mean_x/=len(pos)
        mean_y/=len(pos)
        abstract_pos[cur_id]=(mean_x,mean_y)
        print(abstract_pos)

    for element in root_n:
        if(element.tag=='edge'):
            if 'from' in element.attrib:
                from_ = element.attrib['from']
                to_ = element.attrib['id']
                abstract_G.add_edge(from_,to_)
            if 'to' in element.attrib:
                from_ = element.attrib['id']
                to_ = element.attrib['to']
                abstract_G.add_edge(from_,to_)
    end = time.time()
    print("Time consuming:", end-start)
    # print(abstract_G.nodes())
    # mat1 = nx.to_numpy_matrix(abstract_G,abstract_G.nodes())
    # mat2 = nx.to_numpy_matrix(abstract_G)
    # print(mat1,mat2)

    # nx.draw(abstract_G,abstract_pos)
    # plt.show()
