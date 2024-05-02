import requests
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi import FastAPI # type: ignore
import time
from datetime import datetime
import threading
import configparser

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể chỉ định danh sách các origin cụ thể
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Có thể chỉ định các phương thức cụ thể
    allow_headers=["*"],  # Có thể chỉ định danh sách các header cụ thể
)

url_real = "http://db_api:8000"
url_hot_destination = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/hotdestination.json"
url_list_tour = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/list_tour.json"
url_list_tour_all = "https://www.vietnambooking.com/wp-content/uploads/data_json/tours/list_tour_all.json"

# Khởi tạo một đối tượng ConfigParser
config = configparser.ConfigParser()

# Đọc các giá trị từ file .conf
config.read(".conf")

const_hour = config.getint("setup_crawl", "const_hour")
const_minute = config.getint("setup_crawl", "const_minute")
const_second = config.getint("setup_crawl", "const_second")

@app.get("/crawl_now")
async def crawl_now():
    crawl_all()
    return "Đã cào mới dữ liệu"

def call_api_hot_destination(data):
    url = url_real + "/insert_data_hot_destination"
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
            print("Data inserted successfully!")
        else:
            print("Failed to insert data:", response.text)
def call_api_list_tour(data):
    url = url_real + "/insert_data_list_tour"
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
            response.raise_for_status()  # Nếu có lỗi trong phản hồi, nó sẽ ném một ngoại lệ HTTPError
            
            # In ra thông báo nếu thành công
            print("Dữ liệu được chèn thành công!!")
        except requests.HTTPError as e:
            print("Lỗi trong khi chèn dữ liệu:", e)

def call_api_list_tour_all(data):
    url = url_real + "/insert_data_list_tour_all"
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
            response.raise_for_status()  # Nếu có lỗi trong phản hồi, nó sẽ ném một ngoại lệ HTTPError
            
            # In ra thông báo nếu thành công
            print("Dữ liệu được chèn thành công!")
        except requests.HTTPError as e:
            print("Lỗi trong khi chèn dữ liệu:", e)


def crawl(url):
    response = requests.get(url)
    if response.status_code == 200: # Kiểm tra kết quả trả 200 - OK
        json_data = response.json()
        return json_data
    else:
        return None

def crawl_all():
    # Gọi tới API insert của từng bảng với dữ liệu được cào theo đường link
    call_api_hot_destination(crawl(url_hot_destination))
    call_api_list_tour(crawl(url_list_tour))
    call_api_list_tour_all(crawl(url_list_tour_all))
    print("Đã thực thi xong cào toàn bộ dữ liệu")
def setup_crawl():
    run = True
    is_crawl = False
    while (run):
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        print(hour, minute, second)
        print(const_hour, const_minute, const_second)
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