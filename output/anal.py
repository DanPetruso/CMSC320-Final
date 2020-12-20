#!/bin/python3
import json
import os
import sys
import pdb
import subprocess
import json

directory = sys.argv[1]
out_dir  = sys.argv[2]
slippc_path = "./slippc/slippc"

print('recursing through = ' + directory)

replays = []

for dirpath, dirs, files in os.walk(directory):
    path = dirpath.split('/')
    print('|', (len(path))*'---', '[',os.path.basename(dirpath),']')
    for f in files:
        print('|', len(path)*'---', f)
        replays.append(dirpath + "/" + f)

print("Parsing " + str(len(replays)) + " replays")
analysis = []

for r in replays:
    fin = subprocess.Popen([slippc_path, "-i", r, "-a", r + ".json"]).wait()
    if fin == 0:
        analysis.append("./" + r + ".json")

print("Analyized " + str(len(analysis)) + " replays")
print("Sorting replays in: " + out_dir  + "/")

sort_dirs = {}

for a in analysis:
    print(a)
    try:
        with open(a) as f:
           match = json.load(f)
           p1 = match["players"][0]["char_name"]
           p2 = match["players"][1]["char_name"]
    
           #  Sort the names so the correspond to the propery dictionary key
           s = sorted((p1, p2))
           key = s[0] + "-" + s[1]
           print(key)
    
           if key not in sort_dirs:
                sort_dirs[key] =  []
           sort_dirs[key].append(a)
    except IOError as e:
        print("IO Error")

print("Writting sorted data")

for key in sort_dirs:
    count = 0
    for f in sort_dirs[key]:
        if not os.path.exists("./" + out_dir + "/" + key):
            os.makedirs("./" + out_dir + "/" + key)
        os.rename(f, "./" + out_dir + "/" + key  + "/" + key + "-" +  str(count) + ".json")
        count+=1

pdb.set_trace()
