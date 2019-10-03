import os
import osmnx as ox
import subprocess
import overpass
osmapi = overpass.API()#endpoint="https://overpass.myserver/interpreter")

print("OutputDir=",end='')
OutputDir = input()
try:
	os.mkdir(os.path.abspath(OutputDir))
except:
	print("Exists")
print("city: ", end='')
city = input()

osmFile = OutputDir + '/graph.osm'
osmFile = os.path.abspath(osmFile)
xmlfile = OutputDir + "/graph.net.xml"
xmlfile =  os.path.abspath(xmlfile)

# print("Downloading map stat...")
# G = ox.graph_from_place(city, network_type='drive')
# print("Saving map stat...")
# ox.save_graph_osm(G, folder = OutputDir, filename='graph.osm')

print("Downloading map stat...")
response = osmapi.get('node["name"="Salt Lake City"]', responseformat="xml")
print(response)
newosmFile=open(osmFile,'w')
newosmFile.write(response)
# doc.writexml(osmFile,addindent=' '*4, newl='\n', encoding='utf-8')

# overpass_url = "http://overpass-api.de/api/interpreter"
# overpass_query = """
# area["ISO3166-1"="DE"][admin_level=2];
# (node["amenity"=%s](area);
#  way["amenity"=%s](area);
#  rel["amenity"=%s](area);
# );
# out center;
# """, city, city, city
# response = requests.get(overpass_url, 
#                         params={'data': overpass_query})
# print(response)

print("Saving map stat...")
# tree = ET.parse(response.text)
# root = tree.getroot()
# with open(osmFile, 'w') as f:
#     f.write(response.text)

# Convert

cmd = "netconvert --osm-files " + osmFile + ' -o ' + xmlfile
# netconvert --osm-files berlin.osm.xml -o berlin.net.xml
returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix


# city = input()
# overpass_url = "http://overpass-api.de/api/interpreter"
# overpass_query = """
#  <query type="relation">
#  <has-kv k="boundary" v="administrative"/>
#  <has-kv k="name" v="Berlin"/>
#  </query>
#  <print mode="body"/>
# """
# response = requests.post(overpass_url, 
#                         params={'data': overpass_query})
# data = response.json()
# os.Save("dataosm.osm",data)