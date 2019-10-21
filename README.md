# Extend SUMO function

## [Setup SUMO 1.1](https://github.com/XiyuZhai97/SUMO_extend/tree/master/HelloSUMO)
  [Ref](https://sumo.dlr.de/docs/Installing/Linux_Build.html)

## [Get Altitude](https://github.com/XiyuZhai97/SUMO_extend/tree/master/GetAltitude)

## [Get OSM data](https://github.com/XiyuZhai97/SUMO_extend/tree/master/GetOSM)

## Arc Generator:
To make roundabout's shape better
Given center point, start and end point coordinates, generate 90 points on the arc.

## Osm Commandline Download Wizard
	python osmTwizardZ.py -c beijing -n True
	# equal to 
	netconvert -t '/home/xiyu/Documents/sumo/data/typemap/osmNetconvert.typ.xml' --geometry.remove --roundabouts.guess --ramps.guess -v --junctions.join --tls.guess-signals --tls.discard-simple --tls.join --output.original-names --junctions.corner-detail 5 --output.street-names --tls.default-type actuated --osm.elevation --osm-files osm_bbox.osm.xml -o osm.net.xml

## Use sumo-web3d to visualize sumocfg

	sumo-web3d -c ~/Documents/janux/janux/topology/xiyuzhai/emeryville2019-10-19-19-39-33/osm.sumocfg 
