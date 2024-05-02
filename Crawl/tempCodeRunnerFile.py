config = configparser.ConfigParser()

# Đọc các giá trị từ file config.conf
config.read(".conf")

const_hour = config.getint("setup_crawl", "const_hour")
const_minute = config.getint("setup_crawl", "const_minute")
const_second = config.getint("setup_crawl", "const_second")
