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
start = time.time()
tree_n = ET.parse('osm.net.xml')
root_n = tree_n.getroot()
G = nx.MultiDiGraph()
pos = {}
for element in root_n:
    if(element.tag=='edge'):
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
end = time.time()
print(end-start)
nx.draw(G,pos)
plt.show()

