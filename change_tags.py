import csv
import json
import re
from collections import defaultdict
import textdistance

e_tags = open("data/epicurious_tag_counts.txt","r")
n_tags = open("data/nyt_tag_counts.txt","r")

e_tag = list()
for i in e_tags.readlines():
    e_tag.append(" ".join(i.strip().split(",")[:-1]))

n_tag = list()
for i in n_tags.readlines():
    n_tag.append(" ".join(i.strip().split(",")[:-1]))

e_tags.close()
n_tags.close()

change = defaultdict(str)
max_sim = defaultdict(float)
for n in n_tag:
    for e in e_tag:
        temp = re.sub("[\\/-]"," ",e)
        if "Free" in temp and "Free" not in n:
            continue
        if "Free" in n and "Free" not in temp:
            continue
        if "Low" in temp and "Low" not in n:
            continue
        if "Low" in n and "Low" not in temp:
            continue
        if "No" in temp and "No" not in n:
            continue
        if "No" in n and "No" not in temp:
            continue
        if "Conscious" in temp and "Conscious" not in n:
            continue
        if "Conscious" in n and "Conscious" not in temp:
            continue
        sim = textdistance.levenshtein.normalized_similarity(n, temp)
        # sim = textdistance.needleman_wunsch.normalized_similarity(n, temp)
        if n == e or n in temp or sim > 0.8:
            if max_sim[e] < sim:
                change[e] = n
                max_sim[e] = sim

f = open("data/change_tags_lev.txt","w",encoding="utf-8")
f.write(json.dumps(change, indent=2, sort_keys=True))
f.close()