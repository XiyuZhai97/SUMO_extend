# Setup SUMO 1.1 https://sumo.dlr.de/docs/Installing/Linux_Build.html

### Build
     sudo apt-get install cmake python g++ libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev swig
     git clone --branch v1_1_0 --recursive https://github.com/eclipse/sumo
     export SUMO_HOME="$PWD/sumo"
     mkdir sumo/build/cmake-build && cd sumo/build/cmake-build
     cmake ../..
     make -j$(nproc)
     
### Set Environment 
	sudo nano /etc/bash.bashrc 
    export SUMO_HOME="～～～～～/sumo"
	export PATH="$SUMO_HOME/bin:$PATH"
    source /etc/bash.bashrc
    
### Use sumo-gui to test

## Simple Crossing Road

### Make a example.nod.xml file
	<nodes> <!-- The opening tag -->

      <node id="0" x="0.0" y="0.0" type="traffic_light"/> <!-- def. of node "0" -->

      <node id="1" x="-500.0" y="0.0" type="priority"/> <!-- def. of node "1" -->
      <node id="2" x="+500.0" y="0.0" type="priority"/> <!-- def. of node "2" -->
      <node id="3" x="0.0" y="-500.0" type="priority"/> <!-- def. of node "3" -->
      <node id="4" x="0.0" y="+500.0" type="priority"/> <!-- def. of node "4" -->

      <node id="m1" x="-250.0" y="0.0" type="priority"/> <!-- def. of node "m1" -->
      <node id="m2" x="+250.0" y="0.0" type="priority"/> <!-- def. of node "m2" -->
      <node id="m3" x="0.0" y="-250.0" type="priority"/> <!-- def. of node "m3" -->
      <node id="m4" x="0.0" y="+250.0" type="priority"/> <!-- def. of node "m4" -->

  	</nodes> <!-- The closing tag -->
    
### Make a example.edg.xml file
    <edges>

      <edge id="1fi" from="1" to="m1" priority="2" numLanes="2" speed="11.11"/>
      <edge id="1si" from="m1" to="0" priority="3" numLanes="3" speed="13.89"/>
      <edge id="1o" from="0" to="1" priority="1" numLanes="1" speed="11.11"/>

      <edge id="2fi" from="2" to="m2" priority="2" numLanes="2" speed="11.11"/>
      <edge id="2si" from="m2" to="0" priority="3" numLanes="3" speed="13.89"/>
      <edge id="2o" from="0" to="2" priority="1" numLanes="1" speed="11.11"/>

      <edge id="3fi" from="3" to="m3" priority="2" numLanes="2" speed="11.11"/>
      <edge id="3si" from="m3" to="0" priority="3" numLanes="3" speed="13.89"/>
      <edge id="3o" from="0" to="3" priority="1" numLanes="1" speed="11.11"/>

      <edge id="4fi" from="4" to="m4" priority="2" numLanes="2" speed="11.11"/>
      <edge id="4si" from="m4" to="0" priority="3" numLanes="3" speed="13.89"/>
      <edge id="4o" from="0" to="4" priority="1" numLanes="1" speed="11.11"/>

    </edges>
    
### Use NETCONVERT to make .net.xml file from nod and edg
	netconvert --node-files=example.nod.xml --edge-files=example.edg.xml --output-file=hello.net.xml
Now you can see the crossing road in sumo-gui by open network: hello.net.xml

### Generate random vehicles https://sumo.dlr.de/docs/Tools/Trip.html
	$SUMO_HOME/tools/randomTrips.py -n hello.net.xml -e 50
  The option --seed <INT> can be used to get repeatable pseudo-randomness.
  Now we have trips.trips.xml file

### Make the simulation file example.sumocfg file
    <configuration>
        <input>
            <net-file value="hello.net.xml"/>
            <route-files value="trips.trips.xml"/>
        </input>
        <time>
            <begin value="0"/>
            <end value="10000"/>
        </time>
    </configuration>
  Now you can see the simulation in sumo-gui by open : example.sumocfg file