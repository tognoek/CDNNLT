import requests

payload = { 'api_key': 'cff06aa58e1849751df1c465d6bc14b7', 'url': 'https://www.vietnambooking.com/wp-content/uploads/data_json/tours/hotdestination.json' }
r = requests.get('https://api.scraperapi.com/', params=payload)
print(r.text)