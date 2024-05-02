import configparser

# Khởi tạo một đối tượng ConfigParser
config = configparser.ConfigParser()

# Đọc các giá trị từ file config.conf
config.read(".conf")

# Lấy các giá trị từ phần 'setup_crawl'
const_hour = config.getint("setup_crawl", "const_hour")
const_minute = config.getint("setup_crawl", "const_minute")
const_second = config.getint("setup_crawl", "const_second")

# In các giá trị để kiểm tra
print("const_hour:", const_hour)
print("const_minute:", const_minute)
print("const_second:", const_second)
