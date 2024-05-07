from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import mysql.connector # type: ignore
from MyClass import HotDestination, ListTour, ListTourAll

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể chỉ định danh sách các origin cụ thể
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Có thể chỉ định các phương thức cụ thể
    allow_headers=["*"],  # Có thể chỉ định danh sách các header cụ thể
)

# Kết nối đến cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="db",
    user="root",
    password="psw123",
    database="vietnambooking")
cursor = conn.cursor()

# API để chèn dữ liệu vào bảng hot_destination
@app.post("/insert_data_hot_destination")
async def insert_data(tour: HotDestination):
    try:
        # Thực hiện truy vấn INSERT INTO ... ON DUPLICATE KEY UPDATE
        mysql = ("INSERT INTO hot_destination (id_post, tour_type_category, image, name, url, type, count) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE "
                 "tour_type_category = VALUES(tour_type_category), "
                 "image = VALUES(image), "
                 "name = VALUES(name), "
                 "url = VALUES(url), "
                 "type = VALUES(type), "
                 "count = VALUES(count)")
        cursor.execute(mysql, (tour.id_post, tour.tour_type_category, tour.image, tour.name, tour.url, tour.type, tour.count))

        # Lưu các thay đổi
        conn.commit()
        
        print("Dữ liệu đã được chèn vào bảng hot_destination hoặc đã được cập nhật nếu đã tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# API để chèn dữ liệu vào bảng list_tour
@app.post("/insert_data_list_tour")
async def insert_data_list_tour(tour: ListTour):
    try:
        # Thực hiện truy vấn INSERT INTO ... ON DUPLICATE KEY UPDATE
        mysql = ("INSERT INTO list_tour (id_post, name, image, url, type, count) "
                 "VALUES (%s, %s, %s, %s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE "
                 "name = VALUES(name), "
                 "image = VALUES(image), "
                 "url = VALUES(url), "
                 "type = VALUES(type), "
                 "count = VALUES(count)")
        cursor.execute(mysql, (tour.id_post, tour.name, tour.image, tour.url, tour.type, tour.count))

        # Lưu các thay đổi
        conn.commit()
        
        print("Dữ liệu đã được chèn vào bảng list_tour hoặc đã được cập nhật nếu đã tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API để chèn dữ liệu vào bảng list_tour_all
@app.post("/insert_data_list_tour_all")
async def insert_data_list_tour_all(tour: ListTourAll):
    try:
        # Thực hiện truy vấn INSERT INTO ... ON DUPLICATE KEY UPDATE
        mysql = ("INSERT INTO list_tour_all (id_post, name, url, category, price, image, type, location, code) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE "
                 "name = VALUES(name), "
                 "url = VALUES(url), "
                 "category = VALUES(category), "
                 "price = VALUES(price), "
                 "image = VALUES(image), "
                 "type = VALUES(type), "
                 "location = VALUES(location), "
                 "code = VALUES(code)")
        cursor.execute(mysql, (tour.id_post, tour.name, tour.url, tour.category, tour.price, tour.image, tour.type, tour.location, tour.code))

        # Lưu các thay đổi
        conn.commit()
        
        print("Dữ liệu đã được chèn vào bảng list_tour_all hoặc đã được cập nhật nếu đã tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API để lấy tất cả dữ liệu từ bảng hot_destination
@app.get("/get_all_data_hot_destination")
async def get_all_data():
    try:
        # Thực hiện truy vấn SELECT để lấy tất cả dữ liệu từ cơ sở dữ liệu
        cursor.execute("SELECT * FROM hot_destination")

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# API để lấy tất cả dữ liệu từ bảng list_tour
@app.get("/get_all_data_list_tour")
async def get_all_data_list_tour():
    try:
        # Thực hiện truy vấn SELECT để lấy tất cả dữ liệu từ cơ sở dữ liệu
        cursor.execute("SELECT * FROM list_tour")

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API để lấy tất cả dữ liệu từ bảng list_tour_all
@app.get("/get_all_data_list_tour_all")
async def get_all_data_list_tour_all():
    try:
        # Thực hiện truy vấn SELECT để lấy tất cả dữ liệu từ cơ sở dữ liệu
        cursor.execute("SELECT * FROM list_tour_all")

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# API để tìm kiếm tour trong bảng hot_destination
@app.get("/search_tours_hot_destination/")
async def search_tours(search_input: str):
    try:
        # Thực hiện truy vấn SELECT với điều kiện LIKE để tìm các dòng chứa từ trong cột name
        sql = "SELECT * FROM hot_destination WHERE name LIKE %s"
        cursor.execute(sql, ("%" + search_input + "%",))

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# API để tìm kiếm tour trong bảng list_tour
@app.get("/search_tours_list_tour/")
async def search_tours_list_tour(search_input: str):
    try:
        # Thực hiện truy vấn SELECT với điều kiện LIKE để tìm các dòng chứa từ trong cột name
        sql = "SELECT * FROM list_tour WHERE name LIKE %s"
        cursor.execute(sql, ("%" + search_input + "%",))

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API để tìm kiếm tour trong bảng list_tour_all
@app.get("/search_tours_list_tour_all/")
async def search_tours_list_tour_all(search_input: str):
    try:
        # Thực hiện truy vấn SELECT với điều kiện LIKE để tìm các dòng chứa từ trong cột name
        sql = "SELECT * FROM list_tour_all WHERE name LIKE %s"
        cursor.execute(sql, ("%" + search_input + "%",))

        # Lấy tất cả các dòng dữ liệu từ kết quả của truy vấn
        data = cursor.fetchall()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)