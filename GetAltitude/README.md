# [Get Altitude](https://github.com/XiyuZhai97/SUMO_extend/tree/master/GetAltitude)

## Keep lon and lat
OSM-data has always WGS84 geo coordinates which will be automatically UTM transformed by netconvert (since sumo 0.11.1). Thus you need explicit projection parameters only if you need a different projection. Refer to the NETCONVERT documentation for other conversion options.

 1. [Networks/Elevation](https://sumo.dlr.de/docs/Networks/Elevation.html) 
missing datas

    z-data is imported from tags with key="ele"  in OSM nodes
	
	--osm.elevation

 2. [Convert net to plain xml files](https://sumo.dlr.de/docs/Geo-Coordinates.html) 
regenerate wrong net

 3. [Use sumolib tools](https://www.eclipse.org/lists/sumo-user/msg01183.html)
 
       tricky to convert all nodes
 
       [coordinate_transformations](https://sumo.dlr.de/docs/Tools/Sumolib.html#coordinate_transformations)

4. [Netconvert projection](https://sumo.dlr.de/docs/NETCONVERT.html#projection)
--simple-projection
投影不正确导致变形
## Get Altitude via lon and lat

### Requests -- open-elevation not support api any more
	import requests
	import pandas as pd
	# script for returning elevation from lat, long, based on open elevation data
	# which in turn is based on SRTM
	def get_elevation(lat, long):
	    query = ('https://api.open-elevation.com/api/v1/lookup'
	             f'?locations={lat},{long}')
	    r = requests.get(query).json()  # json object, various ways you can extract value
	    # one approach is to use pandas json functionality:
	    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
	    return elevation

### Build own api on server
	follow https://github.com/Developer66/open-elevation

## Get Altitude via osm? -- not working well on ubuntu 18.04(I didnt try much)
We can keep altitude from osm files

When using option --osm.elevation, z-data is imported from tags with key="ele"  in OSM nodes. (Barely seen in osm)

Since this tag is not yet in wide use, tools exist to overlay OSM data with elevation data sources (http://wiki.openstreetmap.org/wiki/Srtm_to_Nodes). 

When using the osmosis-srtm pluging the option tagName=ele must be used since only the 'ele' tag is evaluated and the plugin would use the 'height' tag by default.

