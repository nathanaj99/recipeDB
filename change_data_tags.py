import csv
import json
import re
from collections import defaultdict
import glob
import os

change = json.loads(open("data/change_tags_nw.txt","r").read())

files = glob.glob("data/raw_jl/epicurious*")
for f in files:
    f_name = os.path.basename(f)
    temp = open(f,"r")
    output = list()
    for i in temp.readlines():
        if i.strip()!="":
            l = json.loads(i.strip())
            if "tags" in l:
                t = [change[x] if x in change else x for x in l["tags"]]
                l["tags"] = t
            output.append(l)
    t = open("data/processed_jl/processed_"+f_name,"w",encoding="utf-8")
    for i in output:
        t.write(json.dumps(i)+"\n")
    t.close()
    temp.close()