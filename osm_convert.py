import requests
import json
import sumolib
netconvert = sumolib.checkBinary('netconvert', bindir)
netconvertOpts = [netconvert]
netconvertOpts += ['--osm-files'] + ['berlin.osm.xml']
netconvertOpts += ['-o'] + ['berlin.net.xml']
print(netconvertOpts)