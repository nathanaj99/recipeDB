import recipeconverter
import json
import re
import time
from unicodedata import numeric
from fractions import Fraction


rc = recipeconverter.RecipeConverter()

input_file = 'nyt_dinner'

def convert_to_grams():
    """
    Loops through all ingredients from the nyt_parser file and tries to use recipeconverter to convert
    to grams. If doesn't work, do nothing. If it does work, then add to the dictionary
    :return:
    """
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def convert_number(s):
        # use dictionary to convert all unicode fractions into real fractions (manually)
        unicode_fractions_dic = {u'¼': ' 0.25', u'½': ' 0.5', u'¾': ' 0.75', u'⅛': ' 0.125', u'⅓': ' 0.33',
                                 u'⅔': ' 0.66', u'⅕': ' 0.2', u'⅙': ' 0.16666', u'⅜': ' 0.375', u'⅒': ' 0.1'} # add more here
        for frac, fl in unicode_fractions_dic.items():
            s = s.replace(frac, fl)

        test = re.findall(r'[A-Za-z]/\d', s)
        if len(test) > 0:
            nums = re.findall(r'(\d+[./]\d+|\d+)', s)
        else:
            nums = re.findall(r'(\d*[./]\d+|\d+)', s)
        print(nums)
        if len(nums) > 0:
            return float(sum(Fraction(j) for j in nums if len(j) > 0))
        else:
            return None

    # print(rc.convert_volume_to_mass('3 g / ¾ teaspoon fine sea salt'))
    # print(rc.convert_volume_to_mass('1 lb/455 g dried linguine'))

    data = json.loads(open('data/nyt_parser/' + input_file + '_results2.json', "r").read())
    print(len(data))

    counter = 0
    for i in data:

        converted = ''
        found = False
        ingredient = data[i]
        i = i.strip()#.replace('//', '/')
        # there is one bug in the epicurious dataset. replacing here
        # try to get grams through regex. if not found, then use the other way.
        # ---- CODE HERE ----
        """
        For NYT, only do "grams"
        For epicurious, do " g " or " g)" or " g/"
        """

        if 'nyt' in input_file:
            g_found = re.findall(r"([-+]?\d*\.\d+|\d+) grams", i)
        else:
            g_found = re.findall(r"([-+]?\d*\.\d+|\d+)(?: g | g\) | g/)", i)

        if len(g_found) > 0:
            # means they found the measurement in grams and we don't need to convert anymore
            data[i]['grams_qty'] = float(g_found[0])
            counter += 1
        else:
            found = False
            if is_number(i[0]):
                try:
                    converted = rc.convert_volume_to_mass(i)
                    if ' g ' in converted:
                        data[i]['grams_qty'] = float(converted.split(' g ')[0])
                        counter += 1
                        found = True
                except:
                    print("ERROR: " + i)

            if not found: # that means the parser couldn't convert to grams
                print("NOT FOUND: " + i)
                conversion_dic = {"cup": 236.59, "tbsp": 16.78, "tsp": 4.93, "quart": 948.35, "pint": 473.18}
                if 'unit' in data[i]:
                    if 'qty' in data[i]:
                        qty = convert_number(data[i]['qty'])
                    elif 'other' in data[i]:
                        qty = convert_number(data[i]['other'])
                    else:
                        qty = convert_number(data[i]['input'])

                    if qty is not None:
                        counter += 1
                        if 'cup' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['cup']
                        elif 'tablespoon' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['tbsp']
                        elif 'teaspoon' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['tsp']
                        elif 'quart' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['quart']
                        elif 'half-pint' in data[i]['unit'] or 'half pint' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['cup']
                        elif 'pint' in data[i]['unit']:
                            data[i]['grams_qty'] = qty * conversion_dic['pint']

    w = open('data/nyt_parser/' + input_file + '_results3.json', 'w')
    json.dump(data, w, ensure_ascii=False, indent=4)

# convert_to_grams()

def find_unique_units():
    data = json.loads(open('data/nyt_parser/' + input_file + '_results2.json', "r").read())
    unique = set([data[i]['qty'] for i in data if 'qty' in data[i] and '/' in data[i]['qty']])
    print(unique)

    print(rc.convert_volume_to_mass('1 lb/455 g dried linguine'))
    i = '1/4 0.25'
    print(float(sum(Fraction(s) for s in i.split())))

    def convert_number(s):
        # use dictionary to convert all unicode fractions into real fractions (manually)
        unicode_fractions_dic = {u'¼': ' 0.25', u'½': ' 0.5', u'¾': ' 0.75', u'⅛': ' 0.125', u'⅓': ' 0.33',
                                 u'⅔': ' 0.66', u'⅕': ' 0.2', u'⅙': ' 0.16666', u'⅜': ' 0.375',
                                 u'⅒': ' 0.1'}  # add more here
        for frac, fl in unicode_fractions_dic.items():
            s = s.replace(frac, fl)

        test = re.findall(r'[A-Za-z]/\d', s)
        if len(test) > 0:
            nums = re.findall(r'(\d+[./]\d+|\d+)', s)
        else:
            nums = re.findall(r'(\d*[./]\d+|\d+)', s)
        print(nums)
        if len(nums) > 0:
            return float(sum(Fraction(j) for j in nums if len(j) > 0))
        else:
            return None
    # print(convert_number('1 ½ cups walnuts or pecans'))
    # print(re.findall(r'(\d*[./]\d+|\d+)', '1 0.5 cups chopped celery'))

# find_unique_units()
# AFTER NUTRITIONAL CONTENT, also generate 1. health rating 2. glucose rating?

def calculate_recipe_nutrition():
    def convert_number(s):
        # use dictionary to convert all unicode fractions into real fractions (manually)
        unicode_fractions_dic = {u'¼': ' 0.25', u'½': ' 0.5', u'¾': ' 0.75', u'⅛': ' 0.125', u'⅓': ' 0.33',
                                 u'⅔': ' 0.66', u'⅕': ' 0.2', u'⅙': ' 0.16666', u'⅜': ' 0.375', u'⅒': ' 0.1'} # add more here
        for frac, fl in unicode_fractions_dic.items():
            s = s.replace(frac, fl)

        test = re.findall(r'[A-Za-z]/\d', s)
        if len(test) > 0:
            nums = re.findall(r'(\d+[./]\d+|\d+)', s)
        else:
            nums = re.findall(r'(\d*[./]\d+|\d+)', s)
        # print(nums)
        if len(nums) > 0:
            return float(sum(Fraction(j) for j in nums if len(j) > 0))
        else:
            return 0

    def normalize_health(s):
        if s < -77:
            return 0.0
        elif s >= 73:
            return 10.0
        else:
            if s >= -77 and s < -17:
                return round((int(s / 2) + 39) / 10.0, 1)
            elif s >= -17 and s < -7:
                return round((s + 48) / 10.0, 1)
            elif s >= -7 and s < 3:
                return round(((s + 7) * 2 + 41) / 10.0, 1)
            elif s >= 3 and s < 13:
                return round((s + 58) / 10.0, 1)
            elif s >= 13 and s < 73:
                return round((int(s / 2) + 64) / 10.0, 1)

    jl = open('data/raw_jl/' + input_file + '.jl', "r").read()
    nyt_results = json.loads(open('data/nyt_parser/' + input_file + '_results3.json', 'r').read())
    # w = open('data/health_results.txt', 'a+')
    w = open('data/processed_jl/' + input_file + '.jl', 'w')

    # FULL_NUTRITION IS NOT IN GIT. THE FILE IS TOO LARGE. BUT IT'S BASICALLY COMBINING ALL THE INGREDIENT NUTRITIONAL INFO
    dic = json.loads(open('data/ingredients/full_nutrition.json').read())
    # print(len(dic))

    data = [json.loads(str(item)) for item in jl.strip().split('\n')]
    nutrition_dic = {'calories': (1008, 2000), 'total fat': (1004, 78), 'carbs': (1005, 275), 'sugars': (2000, 50),
                     'protein': (1003, 50), 'sodium': (1093, 2300), 'fiber': (1079, 28), 'saturated fat': (1258, 20),
                     'trans fat': (1257, None), 'monounsaturated fat': (1292, None), 'polyunsaturated fat': (1293, None),
                     'cholesterol': (1253, 300),
                     'calcium': (1087, 1300), 'magnesium': (1090, 420), 'potassium': (1092, 4700), 'iron': (1089, 18),
                     'zinc': (1095, 11), 'phosphorus': (1091, 1250), 'vitamin a': (1106, 900), 'vitamin c': (1162, 90),
                     'thiamin b1': (1165, 1.2), 'riboflavin b2': (1166, 1.3), 'niacin b3': (1167, 20),
                     'vitabin b6': (1175, 1.7), 'folic acid': (1186, 400), 'vitamin b12': (1178, 2.4),
                     'vitamin d': (1114, 20), 'vitamin e': (1109, 15), 'vitamin k': (1185, 120)}

    for recipe in data:
        ingredients = recipe['ingredients']
        total_nutrition = {'calories': 0, 'total fat': 0, 'carbs': 0, 'sugars': 0, 'protein': 0, 'sodium': 0,
                           'fiber': 0, 'saturated fat': 0, 'trans fat': 0, 'monounsaturated fat': 0,
                           'polyunsaturated fat': 0, 'cholesterol': 0,
                           'calcium': 0, 'magnesium': 0, 'potassium': 0, 'iron': 0, 'zinc': 0, 'phosphorus': 0,
                           'vitamin a': 0, 'vitamin c': 0, 'thiamin b1': 0, 'riboflavin b2': 0, 'niacin b3': 0,
                           'vitabin b6': 0, 'folic acid': 0, 'vitamin b12': 0, 'vitamin d': 0, 'vitamin e': 0,
                           'vitamin k': 0}
        nutrition_dv = {'calories': 0, 'total fat': 0, 'carbs': 0, 'sugars': 0, 'protein': 0, 'sodium': 0,
                           'fiber': 0, 'saturated fat': 0, 'trans fat': None, 'monounsaturated fat': None,
                        'polyunsaturated fat': None, 'cholesterol': 0,
                           'calcium': 0, 'magnesium': 0, 'potassium': 0, 'iron': 0, 'zinc': 0, 'phosphorus': 0,
                           'vitamin a': 0, 'vitamin c': 0, 'thiamin b1': 0, 'riboflavin b2': 0, 'niacin b3': 0,
                           'vitabin b6': 0, 'folic acid': 0, 'vitamin b12': 0, 'vitamin d': 0, 'vitamin e': 0,
                           'vitamin k': 0, 'unsaturated fat': 0}
        for i in ingredients:
            print(i)
            i = i.split('\n')[0].strip()
            if len(i) > 0:
                ingredient_detail = nyt_results[i]
                # take the name, and find the nutritional information in the usda
                # print(ingredient_detail)
                if 'name' in ingredient_detail:
                    ingredient_nutrition = dic[ingredient_detail['name'].strip()]
                    mult = ''
                    if 'grams_qty' in ingredient_detail:
                        mult = ingredient_detail['grams_qty'] / float(100)
                    elif 'qty' in ingredient_detail:
                        mult = convert_number(ingredient_detail['qty']) / float(100)
                    else:
                        mult = 0

                    if 'foodNutrients' in ingredient_nutrition:
                        nutrition_info = ingredient_nutrition['foodNutrients']
                        for j in total_nutrition:
                            id = nutrition_dic[j][0]
                            for nutrient in nutrition_info:
                                if nutrient['nutrientId'] == id:
                                    total_nutrition[j] += mult * nutrient['value']

        for i in total_nutrition:
            if nutrition_dic[i][1] is not None:
                nutrition_dv[i] = (float(total_nutrition[i]) / float(nutrition_dic[i][1])) * 100
        nutrition_dv['unsaturated fat'] = (float(total_nutrition['monounsaturated fat']) + \
                                          float(total_nutrition['polyunsaturated fat'])) / float(33) * 100

        recipe['nutrition_total'] = total_nutrition
        recipe['nutrition_dv'] = nutrition_dv

        cals = nutrition_dv['calories']

        print(total_nutrition)
        print(nutrition_dv)



        if len(ingredients) > 0 and cals > 0:
            weights = [(1, 'unsaturated fat'), (1, 'fiber'), (1, 'protein'), (0.8, 'potassium'),
                                (0.5, 'magnesium'), (0.5, 'iron'), (-1, 'carbs'), (-1, 'saturated fat'),
                                (-1, 'sugars'), (-0.7, 'sodium'), (-1, 'cholesterol')]
            health = 0
            for i in weights:
                health += i[0] * float(nutrition_dv[i[1]]) / float(cals)

            recipe['health_score'] = normalize_health(health)
        else:
            # put health rating as NA when saving later
            recipe['health_score'] = None

        json.dump(recipe, w, ensure_ascii=False)
        w.write('\n')
    w.close()


calculate_recipe_nutrition()

def health_dist():
    r = open('data/health_results.txt', 'r').readlines()
    r = [float(i) for i in r]
    mu, std = norm.fit(r)

    # Plot the histogram.
    plt.hist(r, bins=25, density=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()

# health_dist()

def normalize_health(s):
    if s < -77:
        return 0.0
    elif s >= 73:
        return 10.0
    else:
        if s >= -77 and s < -17:
            return round((int(s/2) + 39)/10.0, 1)
        elif s >= -17 and s < -7:
            return round((s + 48)/10.0, 1)
        elif s >= -7 and s < 3:
            return round(((s + 7)*2 + 41)/10.0, 1)
        elif s >= 3 and s < 13:
            return round((s + 58)/10.0, 1)
        elif s >= 13 and s < 73:
            return round((int(s / 2) + 64) / 10.0, 1)



# for i in np.linspace(-78, 78, 300):
#     print(normalize_health(i))

