# tintin
tintin++ scripts

Map converter for Mudlet to tintin++ format using NyyMap for TorilMUD:

Put files in the same directory to keep it simple:
1) Export Nyyr's Mudlet map from within Mudlet using: ‘lua saveJsonMap’ from the Mudlet command line.
2) There is a list of Toril areas in the .py file - update this as new areas are added.
3) From the shell run:
python3 mudlet_json_to_tintin.py exportedmudletmapname.json > new_map.tin
4) From within tintin++:

#read new_map.tin

#map write final_map.map

thats it!
