import xml.etree.ElementTree as ET
import requests
import pandas as pd
# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
# not support any more see in open-elevation
# need build own open elevation

def get_elevation(lat, long): 
    query = ('http://192.168.0.131:10000/api/v1/lookup'
             f'?locations={lat},{long}')
    r = requests.get(query).json()  # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation
def elevation(lat, lng):
    apikey = "USE YOUR OWN KEY !!!"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    try:
        results = json.loads(request.text).get('results')
        if 0 < len(results):
            elevation = results[0].get('elevation')
            #resolution = results[0].get('resolution') # for RESOLUTION
            # ELEVATION
            return elevation
        else:
            print('HTTP GET Request failed.')
    except ValueError as e:
        print('JSON decode failed: '+str(request) + str(e))
        xmlfile = "./emeryville2019-10-19-19-39-33/osm_ele.osm.xml"
import time
def get_latlon(element):
    lat = element.attrib['lat']
    lon = element.attrib['lon']
    return lat, lon
def add_Ele(xmlfile):
    start = time.time()
    tree_n = ET.parse(xmlfile)
    root_n = tree_n.getroot()
    i = 0
    for element in root_n:
        if(i%10000 == 0):
            end = time.time()
            print('Get ele for {0} nodes, time consuming:{1}'.format(i,end-start))
        if(element.tag=='node'):
            tag_ele = ET.Element("tag")
            tag_ele.set('k','ele')
            lat,lon = get_latlon(element)
            ele = get_elevation(lat, lon)
            tag_ele.set('v',str(ele))
            element.append(tag_ele)
            i += 1
    tree_n.write(xmlfile)
    end = time.time()
    print('Get ele for {0} nodes, time consuming:{1}'.format(i,end-start))
add_Ele(xmlfile)

#	netconvert -t '/home/xiyu/Documents/sumo/data/typemap/osmNetconvert.typ.xml' --geometry.remove --roundabouts.guess --ramps.guess -v --junctions.join --tls.guess-signals --tls.discard-simple --tls.join --output.original-names --junctions.corner-detail 5 --output.street-names --tls.default-type actuated --osm.elevation --osm-files osm_ele.osm.xml  -o osm.net.xml
#  	sumo-web3d -c ~/Documents/janux/janux/topology/xiyuzhai/emeryville2019-10-19-19-39-33/osm.sumocfg 
