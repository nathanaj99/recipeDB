import json
import csv

input_file = 'nyt_dinner'
jl = open(input_file + '.jl', "r").read()
data = [json.loads(str(item)) for item in jl.strip().split('\n')]

w = open(input_file + '.txt', 'w')

for i in data:
    ingredients = i['ingredients']
    for j in ingredients:
        w.write(j + '\n')

w.close()