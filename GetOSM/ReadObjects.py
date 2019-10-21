import pickle
import os
import itertools
import networkx as nx
import shutil
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print ("---  new folder...  ---")
    else:
        print ("--- Remove all .pkl in it---")

def read_from_pickle(fname):
    try:
        while True:
            yield pickle.load(inputHandler)
    except EOFError:
        pass
def countnode(info):
    return info['pos_matrix'].shape[1]
def countedge(info):
    adjm = info['adj_matrix']
    # print(adjm.shape)
    mpoint = np.max(np.sum(adjm, axis = 0)[0])
    print(mpoint)
    return mpoint

def recover(info):
    G = nx.MultiDiGraph()
    combine_pos = {}
    posm = info['pos_matrix']
    adjm = info['adj_matrix']
    nodes_n = posm.shape[1]
    # print(nodes_n)
    node_names = {}
    
    for i in range(nodes_n):
        node_name = 'X:'+str(posm[0][i])+'Y:'+str(posm[1][i])
        combine_pos[node_name]=(posm[0][i],posm[1][i])
        node_names[i]=node_name
        G.add_node(node_name)
    for i in range(adjm.shape[0]):
        for j in range(adjm.shape[1]):
            if adjm[i,j]==1:
                G.add_edge(node_names[i],node_names[j])

    nx.draw(G,combine_pos)
    plt.show()
parser = ArgumentParser(
    description="Read and show pkl files of nodes")
parser.add_argument("--citydir","-f", default='emeryville2019-10-19-19-39-33',dest="citydir", help="Directory folder of the city.")

if __name__== "__main__":
    args = parser.parse_args()
    citydir = args.citydir
    # citydir = 'emeryville2019-10-19-19-39-33'
    sourcedir = citydir + '/pklfile'
    targetdir = citydir + '/mostpkl'
    mkdir(targetdir)
    # dictcountnod = {}
    dictcountedg = {}
    for filename in os.listdir(sourcedir):
        print(filename)
        if filename.endswith(".pkl"):
            inputHandler = open(sourcedir+'/'+filename, "rb")
            for item in read_from_pickle(inputHandler):
                # dictcountnod[str(filename)] = countnode(item)
                dictcountedg[str(filename)] = countedge(item)# * countnode(item)
            inputHandler.close()
    # dictsorted = sorted(dictcountnod.items(), key = lambda item:item[1], reverse = True)
    dictsorted = sorted(dictcountedg.items(), key = lambda item:item[1], reverse = True)
    print(dictsorted)
    for filename in dictsorted[0:10]:
        if filename[0] == "abstract_G.pkl":
            continue
        print(filename)
        inputHandler = open(sourcedir+'/'+filename[0], "rb")
        for item in read_from_pickle(inputHandler):
            recover(item)
        inputHandler.close()
        srcFile = os.path.join(sourcedir,filename[0])
        targetFile = os.path.join(targetdir,filename[0])
        shutil.copyfile(srcFile,targetFile)
