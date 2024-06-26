import requests
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi import FastAPI # type: ignore
import time
from datetime import datetime
import threading
import configparser
import json
from bs4 import BeautifulSoup # type: ignore

# Khởi tạo một đối tượng ConfigParser
config = configparser.ConfigParser()
# Đọc các giá trị từ file .conf
config.read(".conf")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể chỉ định danh sách các origin cụ thể
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Có thể chỉ định các phương thức cụ thể
    allow_headers=["*"],  # Có thể chỉ định danh sách các header cụ thể
)

tognoek = False

url_real = "http://db_api:8000"
# Url real
url_hot_destination = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/hotdestination.json"
url_list_tour = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/list_tour.json"
url_list_tour_all = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/list_tour_all.json"

# key
apikey = "f089459c644a010d87fbc5c9452db869e2fb250d"

# api fake
url_hot_destination_fake = "http://api_fake:8020/hot_destination"
url_list_tour_fake = "http://api_fake:8020/list_tour"
url_list_tour_all_fake = "http://api_fake:8020/list_tour_all"


# Lấy thời gian cào dữ liệu
const_hour = config.getint("setup_crawl", "const_hour")
const_minute = config.getint("setup_crawl", "const_minute")
const_second = config.getint("setup_crawl", "const_second")

@app.get("/crawl_now")
async def crawl_now():
    crawl_all()
    return "Đã cào mới dữ liệu"

def call_api_hot_destination(data):
    url = url_real + "/insert_data_hot_destination"
    if data == None:
        print("No data")
        return
    for item in data:
        data_payload = {
        "id_post": item["id_post"],
        "tour_type_category": item["tour_type_category"],
        "image": item["image"],
        "name": item["name"],
        "url": item["url"],
        "type": item["type"],
        "count": item["count"]
        }
        # Gửi yêu cầu POST đến API
        response = requests.post(url, json=data_payload)
        if response.status_code == 200:
            print("Gửi yêu cầu thành công")
        else:
            print("Lỗi: ", response.text)
def call_api_list_tour(data):
    url = url_real + "/insert_data_list_tour"
    if data == None:
        print("No data")
        return
    for item in data:
        data_payload = {
            "id_post": item["id_post"],
            "name": item["name"],
            "image": item["image"],
            "url": item["url"],
            "type": item["type"],
            "count": item["count"]
        }
        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=data_payload)
            response.raise_for_status()  
            # In ra thông báo nếu thành công
            print("Gửi yêu cầu thành công")
        except requests.HTTPError as e:
            print("Lỗi: ", e)

def call_api_list_tour_all(data):
    url = url_real + "/insert_data_list_tour_all"
    if data == None:
        print("No data")
        return
    for item in data:
        price = "2904"
        if item["price"] != "":
            price = item["price"]
        data_payload = {
            "id_post": item["id_post"],
            "name": item["name"],
            "url": item["url"],
            "category": item["category"],
            "price": price,
            "image": item["image"],
            "type": item["type"],
            "location": item["location"],
            "code": item["code"]
        }

        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=data_payload)
            response.raise_for_status()  
            
            # In ra thông báo nếu thành công
            print("Gửi yêu cầu thành công")
        except requests.HTTPError as e:
            print("Lỗi: ", e)


def crawl(url):
    response = requests.get(url)
    if response.status_code == 200: # Kiểm tra kết quả trả 200 - OK
        json_data = response.json()
        print("Sử dụng: " + url)
        return json_data
    else:
        return None
def crawl_by_zenrows(url):
    params = {
        "url": url,
        "apikey": apikey,
    }
    if tognoek:
        response = requests.get("https://api.zenrows.com/v1/", params=params)
        if response.status_code == 2030:
            print("Sử dụng Zenrows")
            return response.json()
        else:
            return None
    else:
        return None

def crawl_by_zenrows_vip(url):
    params = {
        "url": url,
        "apikey": apikey,
        "original_status": "true",
        "js_render": "true",
    }
    if tognoek:
        response = requests.get("https://api.zenrows.com/v1/", params=params)
        if response.status_code == 2030:
            soup = BeautifulSoup(response.text, "html.parser")
            pre_tag_content = soup.find("pre").string.strip()
            # Chuyển đổi nội dung của thẻ <pre> thành đối tượng Python (trong trường hợp này là danh sách các từ điển)
            data = json.loads(pre_tag_content)
            print("Sử dụng Zenrows Vip")
            return data
        else:
            return None
    else:
        return None

def crawl_all():
    # Gọi tới API insert của từng bảng với dữ liệu được cào theo đường link
    data_json = crawl(url_hot_destination)
    if (data_json != None):
        call_api_hot_destination(data_json)
    else:
        data_json = crawl_by_zenrows(url_hot_destination)
        if (data_json != None):
            call_api_hot_destination(data_json)
        else:
            data_json = crawl_by_zenrows_vip(url_hot_destination)
            if (data_json != None):
                call_api_hot_destination(data_json)
            else:
                data_json = crawl(url_hot_destination_fake)
            call_api_hot_destination(data_json)

    data_json = crawl(url_list_tour)
    if (data_json != None):
        call_api_list_tour(data_json)
    else:
        data_json = crawl_by_zenrows(url_list_tour)
        if (data_json != None):
            call_api_list_tour(data_json)
        else:
            data_json = crawl_by_zenrows_vip(url_list_tour)
            if (data_json != None):
                call_api_list_tour(data_json)
            else:
                data_json = crawl(url_list_tour_fake)
            call_api_list_tour(data_json)
    
    data_json = crawl(url_list_tour_all)
    if (data_json != None):
        call_api_list_tour_all(data_json)
    else:
        data_json = crawl_by_zenrows(url_list_tour_all)
        if (data_json != None):
            call_api_list_tour_all(data_json)
        else:
            data_json = crawl_by_zenrows_vip(url_list_tour_all)
            if (data_json != None):
                call_api_list_tour_all(data_json)
            else:
                data_json = crawl(url_list_tour_all_fake)
            call_api_list_tour_all(data_json)

    # call_api_hot_destination(crawl(url_hot_destination))
    # call_api_list_tour(crawl(url_list_tour))
    # call_api_list_tour_all(crawl(url_list_tour_all))
    print("Đã thực thi xong cào toàn bộ dữ liệu")
def setup_crawl():
    run = True
    is_crawl = False
    while (run):
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        # print(hour, minute, second)
        # print(const_hour, const_minute, const_second)
        if hour != const_hour:
            is_crawl = False
        if (hour == const_hour and minute == const_minute and not is_crawl):
            is_crawl = True
            crawl_all()
            print("Đã cào mới dữ liệu theo thời gian cài đặt")
        time.sleep(1)

#  Cào dữ liệu ngày khi chương trình (container -- docker) khỏi chạy
crawl_all()

# Tạo một tiến trình mới để chạy vòng lặp vô hạn
crawler_thread = threading.Thread(target=setup_crawl)
crawler_thread.daemon = True  # Đánh dấu tiến trình là daemon để nó tự động dừng khi chương trình chính dừng
crawler_thread.start()  # Bắt đầu chạy tiến trình

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)