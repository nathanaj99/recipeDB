import requests
import json
import re
import time

input = 'named_ingredients2'
api_key = 'pCgUQRaVoVmMiPgkTNQgAlPplPQOQp1snwnM7Ahh'

ingredients = open('data/ingredients/' + input + '.txt', 'r').readlines()

output = open('data/ingredients/' + input + '_nutrition.json', 'w')
nutrition_dic = {}

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

counter = 0
for i in ingredients:
    print(i)
    if counter % 3600 == 0:
        print(counter)
    keyword = " ".join(re.findall("[a-zA-Z0-9]+", i))
    keyword = keyword.replace(' ', '%20')
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={}&query={}'.format(api_key, keyword)
    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise APIError('GET /tasks/ {}'.format(resp.status_code))

    if len(resp.json()['foods']) > 0:
        # if the query gets some results
        nutrition_dic[i.strip()] = resp.json()['foods'][0]
    else:
        nutrition_dic[i.strip()] = {}

    time.sleep(2)
    counter += 1

json.dump(nutrition_dic, output, ensure_ascii=False, indent=4)


# i = '1 (5-pound) New York strip roast (also called beef strip loin or top loin), fat trimmed to 1/4", untied'
# keyword = " ".join(re.findall("[a-zA-Z0-9]+", i))
# print(keyword)
# keyword = keyword.replace(' ', '%20')
# api_key = 'pCgUQRaVoVmMiPgkTNQgAlPplPQOQp1snwnM7Ahh'
# url = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={}&query={}'.format(api_key, keyword)
# resp = requests.get(url)
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise APIError('GET /tasks/ {}'.format(resp.status_code))
#
# print(resp.json()['foods'][0])