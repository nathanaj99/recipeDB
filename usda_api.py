import requests
import json

keyword = 'Cheddar Cheese'
keyword = keyword.replace(' ', '%20')
url = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=pCgUQRaVoVmMiPgkTNQgAlPplPQOQp1snwnM7Ahh&query=' + keyword
resp = requests.get(url)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))


print(resp.json())