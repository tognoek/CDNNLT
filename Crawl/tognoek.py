# pip install requests
import requests
from bs4 import BeautifulSoup
import json
url = 'https://www.vietnambooking.com/wp-content/uploads/data_json/tours/hotdestination.json'
apikey = 'f089459c644a010d87fbc5c9452db869e2fb250d'
params = {
    'url': url,
    'apikey': apikey,
	'original_status': 'true',
	'js_render': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
pre_tag_content = soup.find('pre').string.strip()

# Chuyển đổi nội dung của thẻ <pre> thành đối tượng Python (trong trường hợp này là danh sách các từ điển)
data = json.loads(pre_tag_content)
print(data)