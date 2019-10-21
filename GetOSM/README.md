
# Osm Commandline Download Wizard
	python osmTwizardZ.py -c beijing -n True
	# equal to 
	
	netconvert -t '/home/xiyu/Documents/sumo/data/typemap/osmNetconvert.typ.xml' --geometry.remove --roundabouts.guess --ramps.guess -v --junctions.join --tls.guess-signals --tls.discard-simple --tls.join --output.original-names --junctions.corner-detail 5 --output.street-names --tls.default-type actuated --osm.elevation --osm-files osm_bbox.osm.xml -o osm.net.xml