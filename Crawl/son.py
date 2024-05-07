import requests

url = "https://www.vietnambooking.com/wp-admin/admin-ajax.php"

payload = {
    "action": "api_flight_ajax_system_search_flight",
    "info_search[adult]": "1",
    "info_search[child]": "0",
    "info_search[infant]": "0",
    "info_search[device]": "desktop",
    "info_search[itinerary]": "Oneway",
    "info_search[departure]": "SGN",
    "info_search[destination]": "HAN",
    "info_search[departuredate]": "15052024",
    "info_search[returndate]": ""
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    data = response.json()
    depart_html_data_flight = data.get("data_flight_html", {}).get("depart_html_data_flight")
    if depart_html_data_flight:
        print("Dữ liệu depart_html_data_flight:")
        print(depart_html_data_flight)
    else:
        print("Không tìm thấy depart_html_data_flight trong phản hồi.")
else:
    print("Lỗi khi gửi yêu cầu:", response.status_code)
