import networkx as nx
import xml.etree.ElementTree as ET
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
def mkdir(path):
 
    folder = os.path.exists(path)
 
    if not folder:
        os.makedirs(path)
        print ("---  new folder...  ---")
    else:
        print ("---  There is this folder!  ---")
#抽象Node，此时每一个节点里面存着一个小的图
class AbsNode():
	def __init__(self, absnode, pos):
		#每个抽象Node的成员有小的图，type为nx的数据类型
		#以及对应这个小的图的各个节点的position
		self.absnode = absnode
		self.pos = pos

	def merge(self,glst):
		if type(glst)==list:
			for g in glst:
				nodes = list(g.absnode.nodes())
				edges = list(g.absnode.edges())
				for node in nodes:
					self.absnode.add_node(node)
					self.pos[node] = g.pos[node]
				for edge in edges:
					self.absnode.add_edge(edge)
		else:
			nodes = list(glst.absnode.nodes())
			edges = list(glst.absnode.edges())
			for node in nodes:
				self.absnode.add_node(node)
				self.pos[node] = glst.pos[node]
			for edge in edges:
				self.absnode.add_edge(edge)

#抽象的总图，总图里的每个节点的attribution里面的detail是之前的抽象Node.
class AbsGraph():
	def __init__(self,absgraph,pos):
		self.absgraph = absgraph
		self.pos = pos

	def merge(self, nlst):
		if type(nlst)!=list:
			print('Error: Input error')
		else:
			base = nlst[0]
			mean_x = self.pos[base][0]
			mean_y = self.pos[base][1]
			detail = self.absgraph[base]['details']
			for node in nlst[1:]:
				cur_detail = self.absgraph[node]['details']
				detail.merge(cur_detail)
				mean_x+=self.pos[node][0]
				mean_y+=self.pos[node][1]
				self.pos.pop(node)
				predecessors = list(self.absgraph.predecessors(node))
				successors = list(self.absgraph.successors(node))
				self.absgraph.remove_node(node)
				for pre in predecessors:
					self.absgraph.add_edge(pre, base)
				for suc in successors:
					self.absgraph.add_edge(base, suc)
			self.pos[base][0]=mean_x/len(nlst)
			self.pos[base][1]=mean_y/len(nlst)
			self.absgraph[base]['details']=detail




class sumo2nx():
	def __init__(self, net_path):
		self.father_path = os.path.abspath(os.path.dirname(net_path) + os.path.sep + ".")
		self.tree = ET.parse(net_path)
		self.root = self.tree.getroot()

	def cut(self):
		cur_id = None
		abstract_G = nx.MultiDiGraph()
		abstract_pos = {}
		mkdir(self.father_path+"/pklfile")
		for element in self.root:
			if (element.tag == 'edge'):
				if 'function' in element.attrib and element.attrib['function'] == 'internal':
					new_cur_id = element.attrib['id'].lstrip(':').split('_')[0]
					if new_cur_id == 'cluster':
						continue
				else:
					new_cur_id = element.attrib['id']
				if new_cur_id != cur_id:
					if cur_id!=None:
						info = {}
						nodes = list(G.nodes())
						nodes_dic = {}
						for i in range(len(nodes)):
							nodes_dic[nodes[i]] = i
						info['nodes'] = nodes_dic
						pos_matrix = np.zeros((2, len(pos)))
						for i in range(len(nodes)):
							pos_matrix[0, i] = pos[nodes[i]][0]
							pos_matrix[1, i] = pos[nodes[i]][1]
						info['pos_matrix'] = pos_matrix
						adj_matrix = nx.to_numpy_matrix(G)
						info['adj_matrix'] = adj_matrix
						sources = []
						targets = []
						for i in range(len(nodes)):
							if G.in_degree(nodes[i]) == 0:
								sources.append(i)
							if G.out_degree(nodes[i]) == 0:
								targets.append(i)
						info['sources'] = sources
						info['targets'] = targets
						f = open(self.father_path + '/pklfile/%s.pkl'%cur_id,'wb')
						pickle.dump(info, f)
						mean_x = 0.0
						mean_y = 0.0
						for item in pos:
							mean_x += pos[item][0]
							mean_y += pos[item][1]
						mean_x /= len(pos)
						mean_y /= len(pos)
						abstract_G.add_node(cur_id)
						abstract_pos[cur_id] = (mean_x, mean_y)
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
						node_name = 'X:' + str(pos_x) + '/Y:' + str(pos_y)
						pos[node_name] = (pos_x, pos_y)
						G.add_nodes_from([(node_name)])
						if last != None:
							G.add_edges_from([(last, node_name, attrib)])
						last = node_name

		else:
			abstract_G.add_node(cur_id)
			info = {}
			nodes = list(G.nodes())
			nodes_dic = {}
			for i in range(len(nodes)):
				nodes_dic[nodes[i]] = i
			info['nodes'] = nodes_dic
			pos_matrix = np.zeros((2, len(pos)))
			for i in range(len(nodes)):
				pos_matrix[0, i] = pos[nodes[i]][0]
				pos_matrix[1, i] = pos[nodes[i]][1]
			info['pos_matrix'] = pos_matrix
			adj_matrix = nx.to_numpy_matrix(G)
			info['adj_matrix'] = adj_matrix
			sources = []
			targets = []
			for i in range(len(nodes)):
				if G.in_degree(nodes[i]) == 0:
					sources.append(i)
				if G.out_degree(nodes[i]) == 0:
					targets.append(i)
			info['sources'] = sources
			info['targets'] = targets
			f = open(self.father_path + '/pklfile/%s.pkl'%cur_id,'wb')
			pickle.dump(info, f)
			mean_x = 0.0
			mean_y = 0.0
			for item in pos:
				mean_x += pos[item][0]
				mean_y += pos[item][1]
			mean_x /= len(pos)
			mean_y /= len(pos)
			abstract_pos[cur_id] = (mean_x, mean_y)

		for element in self.root:
			if (element.tag == 'edge'):
				if 'from' in element.attrib:
					from_ = element.attrib['from']
					if from_ in abstract_pos:
						to_ = element.attrib['id']
						abstract_G.add_edge(from_, to_)
				if 'to' in element.attrib:
					
					to_ = element.attrib['to']
					if to_ in abstract_pos:
						from_ = element.attrib['id']
						abstract_G.add_edge(from_, to_)

		info = {}
		nodes = list(abstract_G.nodes())
		#print(len(nodes),len(abstract_pos))
		nodes_dic = {}
		for i in range(len(nodes)):
			nodes_dic[nodes[i]] = i
		info['nodes'] = nodes_dic
		pos_matrix = np.zeros((2, len(abstract_pos)))
		for i in range(len(nodes)):
			try:
				pos_matrix[0, i] = abstract_pos[nodes[i]][0]
				pos_matrix[1, i] = abstract_pos[nodes[i]][1]
			except:
				print(nodes[i])
		info['pos_matrix'] = pos_matrix
		adj_matrix = nx.to_numpy_matrix(abstract_G)
		info['adj_matrix'] = adj_matrix
		sources = []
		targets = []
		for i in range(len(nodes)):
			if abstract_G.in_degree(nodes[i]) == 0:
				sources.append(i)
			if abstract_G.out_degree(nodes[i]) == 0:
				targets.append(i)
		info['sources'] = sources
		info['targets'] = targets
		#nx.draw(abstract_G,abstract_pos)
		#plt.show()
		f =  open(self.father_path + '/pklfile/abstract_G.pkl','wb')
		pickle.dump(info, f)
		
	def recover(self, to_recover):
		G = nx.MultiDiGraph()
		combine_pos = {}
		for item in to_recover:
			f = open(item + '.pkl', 'rb')
			info = pickle.load(f)
			posm = info['pos_matrix']
			adjm = info['adj_matrix']
			nodes_n = posm.shape[1]
			node_names = {}
			for i in range(nodes_n):
				node_name = 'X:' + str(posm[0][i]) + 'Y:' + str(posm[1][i])
				combine_pos[node_name] = (posm[0][i], posm[1][i])
				node_names[i] = node_name
				G.add_node(node_name)
			for i in range(adjm.shape[0]):
				for j in range(adjm.shape[1]):
					if adjm[i, j] == 1:
						G.add_edge(node_names[i], node_names[j])
		return G, combine_pos

	def build_graph(self, name):
		G = nx.MultiDiGraph()
		combine_pos = {}
		f = open(name + '.pkl', 'rb')
		info = pickle.load(f)
		posm = info['pos_matrix']
		adjm = info['adj_matrix']
		nodes_n = posm.shape[1]
		node_names = {}
		for i in range(nodes_n):
			node_name = 'X:' + str(posm[0][i]) + 'Y:' + str(posm[1][i])
			combine_pos[node_name] = (posm[0][i], posm[1][i])
			node_names[i] = node_name
			G.add_node(node_name)
		for i in range(adjm.shape[0]):
			for j in range(adjm.shape[1]):
				if adjm[i, j] == 1:
					G.add_edge(node_names[i], node_names[j])
		return G, combine_pos

	def whole(self):
		G = nx.MultiDiGraph()
		pos = {}
		for element in self.root:
			if (element.tag == 'edge'):
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
						node_name = 'X:' + str(pos_x) + '/Y:' + str(pos_y)
						pos[node_name] = (pos_x, pos_y)
						G.add_nodes_from([(node_name)])
						if last != None:
							G.add_edges_from([(last, node_name, attrib)])
						last = node_name
		adjm = nx.to_numpy_matrix(G)
		nodes = list(G.nodes())
		posm = np.zeros((2, len(nodes)))
		sources = []
		targets = []
		for i in range(len(nodes)):
			if G.in_degree(nodes[i]) == 0:
				sources.append(i)
			if G.out_degree(nodes[i]) == 0:
				targets.append(i)
			posm[0][i] = pos[nodes[i]][0]
			posm[1][i] = pos[nodes[i]][1]
		info = {}
		info['adj_matrix'] = adjm
		info['pos_matrix'] = posm
		info['sources'] = sources
		info['targets'] = targets
		f = open('net.pkl', 'wb')
		pickle.dump(info, f)
		return G, pos

	def visualize(self, G, pos=None):
		if pos != None:
			nx.draw(G, pos)
		else:
			nx.draw(G)
		plt.show()



if __name__ =='__main__':
	sn = sumo2nx('Roundabout4.net.xml')
	sn.cut()