import json
import csv
import textdistance

input_file = 'epicurious'

# file = json.loads(open('data/nyt_parser/epicurious_results.json', 'r').read())
# print(len(file))
# file = json.loads(open('data/nrm/epicurious_results.json', 'r').read())
# print(len(file))
#
# file = json.loads(open('data/nyt_parser/nyt_dinner_results.json', 'r').read())
# print(len(file))
# file = json.loads(open('data/nrm/nyt_dinner_results.json', 'r').read())
# print(len(file))
#
# file = json.loads(open('data/nyt_parser/nyt_results.json', 'r').read())
# print(len(file))
# file = json.loads(open('data/nrm/nyt_results.json', 'r').read())
# print(len(file))

#
#w = open('data/' + input_file + '_raw.txt', 'w')

# data = open('data/' + input_file + '.txt', 'r').readlines()
# w = open('data/nyt.txt', 'w')


# for j in data:
#     j = j.lower().replace(".", "")
#     for abbr, word in dic.items():
#         j = j.replace(abbr, word)
#     print(j)
#     w.write(j + '\n')

# for i in data:
#     ingredients = i['ingredients']
#     for j in ingredients:
#         # j = j.lower().replace(".", "")
#         # for abbr, word in dic.items():
#         #     j = j.replace(abbr, word)
#         # print(j)
#         w.write(j + '\n')
#
# w.close()

def raw_txt():
    jl = open('data/' + input_file + '.jl', "r").read()
    data = [json.loads(str(item)) for item in jl.strip().split('\n')]

    w = open('data/' + input_file + '_raw.txt', 'w')

    for i in data:
        ingredients = i['ingredients']
        for j in ingredients:
            j = j.strip()
            if len(j) > 0:
                w.write(j + '\n')


# raw_txt()

def raw_txt2():
    input_file = 'nyt_dinner'
    data = open('data/' + input_file + '_raw.txt', 'r').readlines()
    w = open('data/' + input_file + '_raw.txt', 'w')
    counter = 0
    for i in data:
        if (len(i.strip())) > 0:
            w.write(i)
            counter += 1

    print(counter)

# raw_txt2()

def preprocess_txt():
    dic = {"tbsp ": "tablespoon ", "tsp ": "teaspoon ", " gal ": " gallon ", "ml ": "milliliter ", " l ": " liter ",
           " lb ": " pound ", " lbs ": " pounds ", " oz ": " ounce ", " mg ": " milligram ", " g ": " gram ",
           "kg ": "kilogram "}

    data = open('data/' + input_file + '_raw.txt', 'r').readlines()
    print(len(data))
    w = open('data/' + input_file + '.txt', 'w')

    for i in data:
        if len(i.strip()) == 0:
            print(i)
        i = i.lower().replace('.', '')
        for abbr, word in dic.items():
            i = i.replace(abbr, word)
        w.write(i)

    w.close()

    data = open('data/' + input_file + '.txt', 'r').readlines()
    print(len(data))

# preprocess_txt()

def check_size():
    data_raw = open('data/' + input_file + '_raw.txt', 'r').readlines()
    data = open('data/' + input_file + '.txt', 'r').readlines()
    data_json = json.loads(open('data/nyt_parser/' + input_file + '_results.json', 'r').read())
    counter = 0
    json_list = [i['input'].strip() for i in data_json]
    # for i in range(len(data_raw)):
    #     raw_entry = data_raw[i].strip()
    #     json_entry = json_list[i].strip()
    #     if raw_entry != json_entry:
    #         # check jaro similarity
    #         if textdistance.jaro.similarity(raw_entry, json_entry) < 0.8:
    #             print(len(raw_entry))
    #             print(raw_entry + " | " + json_entry)
    #             break


    print(len(data))
    print(len(data_raw)) # 30551
    print(len(data_json)) # 30519

check_size()
# preprocessinf text files
# - make everything lowercase
# - combine the unicode fractions somehow
# - get rid of all punctuation .(),