# pip install requests
import requests

url = 'https://www.vietnambooking.com/wp-content/uploads/data_json/tours/hotdestination.json'
apikey = 'f089459c644a010d87fbc5c9452db869e2fb250d'
params = {
    'url': url,
    'apikey': apikey,
	'original_status': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.text)