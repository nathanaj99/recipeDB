import json
import csv

input_file = 'nyt'

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

# check_size()


def convert_json():
    nyt = json.loads(open('data/nyt_parser/' + input_file + '_results.json', 'r').read())
    raw = open('data/' + input_file + '_raw.txt', 'r').readlines()
    new_dict = {}
    for i in range(len(raw)):
        new_dict[raw[i].strip()] = nyt[i]

    w = open('data/nyt_parser/' + input_file + '_results3.json', 'w')
    json.dump(new_dict, w, ensure_ascii=False, indent=4)

    w.close()

    # nrm = json.loads(open('data/nrm/' + input_file + '_results.json', 'r').read())

# convert_json()


def get_unique_ingredients():
    nyt = json.loads(open('data/nyt_parser/nyt_results2.json', 'r').read())
    nyt_set = set([nyt[i]['name'] for i in nyt if 'name' in nyt[i]])
    print(len(nyt_set))
    # print(nyt2_list)

    nyt_dinner = json.loads(open('data/nyt_parser/nyt_dinner_results2.json', 'r').read())
    nyt_dinner_set = set([nyt_dinner[i]['name'] for i in nyt_dinner if 'name' in nyt_dinner[i]])
    print(len(nyt_dinner_set))

    epicurious = json.loads(open('data/nyt_parser/epicurious_results2.json', 'r').read())
    epicurious_set = set([epicurious[i]['name'] for i in epicurious if 'name' in epicurious[i]])
    print(len(epicurious_set))

    total_set = nyt_set | nyt_dinner_set | epicurious_set
    print(len(total_set))

    named_ingredients = open('data/ingredients/named_ingredients1.txt', 'w')
    named_ingredients2 = open('data/ingredients/named_ingredients2.txt', 'w')
    counter = 0
    for i in total_set:
        if counter < 10000:
            named_ingredients.write(i + '\n')
        else:
            named_ingredients2.write(i + '\n')
        counter += 1

    named_ingredients2.close()
    named_ingredients.close()


    # nyt = json.loads(open('data/nyt_parser/nyt_results.json', 'r').read())
    # print(len(nyt))
    # nyt_list = set([i['input'] for i in nyt])
    # print(len(nyt_list))
    #
    # print(nyt2_list - nyt_list)


# get_unique_ingredients()

def no_name():
    nyt = json.loads(open('data/nyt_parser/nyt_results2.json', 'r').read())
    nyt_set_noname = set([i for i in nyt if 'name' not in nyt[i]])
    # print(nyt_set_noname)
    print(len(nyt_set_noname))

    nyt = json.loads(open('data/nyt_parser/nyt_dinner_results2.json', 'r').read())
    nyt_set_noname2 = set([i for i in nyt if 'name' not in nyt[i]])
    # print(nyt_set_noname)
    print(len(nyt_set_noname))

    nyt = json.loads(open('data/nyt_parser/epicurious_results2.json', 'r').read())
    nyt_set_noname3 = set([i for i in nyt if 'name' not in nyt[i]])
    # print(nyt_set_noname)
    print(len(nyt_set_noname))

    all_set = nyt_set_noname | nyt_set_noname2 | nyt_set_noname3
    print(len(all_set))

    unnamed_ingredients = open('data/ingredients/unnamed_ingredients.txt', 'w')
    for i in all_set:
        unnamed_ingredients.write(i + '\n')

    unnamed_ingredients.close()

# no_name()

def split_json(input):
    d = json.loads(open('data/ingredients/' + input + '_nutrition.json', 'r').read())
    w1 = open('data/ingredients/' + input + '_1_nutrition.json', 'w')
    w2 = open('data/ingredients/' + input + '_2_nutrition.json', 'w')
    print(len(d))
    d1 = dict(list(d.items())[len(d) // 2:])
    print(len(d1))
    d2 = dict(list(d.items())[:len(d) // 2])
    print(len(d2))

    json.dump(d1, w1, ensure_ascii=False, indent=4)
    json.dump(d2, w2, ensure_ascii=False, indent=4)
    w1.close()
    w2.close()

split_json('named_ingredients2')