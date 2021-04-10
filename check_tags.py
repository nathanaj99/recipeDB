import json
from collections import Counter
import glob

source = "epicurious"

files = glob.glob("data/raw_jl/"+source+"*")

count = Counter()

for f in files:
    t = open(f,"r")
    for i in t.readlines():
        count += Counter(json.loads(i.strip())["tags"])

f = open("data/"+source+"_tag_counts.txt","w")
for i in count.most_common():
    f.write(i[0]+","+str(i[1])+"\n")
f.close()