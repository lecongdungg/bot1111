import urllib.request
import json
import datetime
import random
import string
import time
import os
import sys

# Cấu hình
REFERRER = "d7a5f2bf-33ed-4c33-912c-9e4ea45f32da"
API_URL_TEMPLATE = 'https://api.cloudflareclient.com/v0a{}/reg'
USER_AGENT = 'okhttp/3.12.1'
HEADERS = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'api.cloudflareclient.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': USER_AGENT
}

# Cài đặt giao diện console
def setup_console():
    os.system("title -PLUS-CLOUDFLARE By CÔNG DỤNG")
    os.system('cls' if os.name == 'nt' else 'clear')

def print_info():
    print("[+] THÔNG TIN SCRIPT:")
    print("[-] Với script này, bạn có thể nhận được không giới hạn GB trên Warp+.")
    print("[-] Phiên bản: 1.0.0")
    print("--------")
    print("[+] SCRIPT ĐƯỢC CODE BỞI CÔNG DỤNG") 
    print("--------")

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def random_digit_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

def create_request_data():
    return {
        "key": f"{random_string(43)}=",
        "install_id": random_string(22),
        "fcm_token": f"{random_string(22)}:APA91b{random_string(134)}",
        "referrer": REFERRER,
        "warp_enabled": False,
        "tos": datetime.datetime.now().isoformat()[:-3] + "+02:00",
        "type": "Android",
        "locale": "es_ES"
    }

def send_request(url, data):
    try:
        request = urllib.request.Request(url, json.dumps(data).encode('utf8'), HEADERS)
        response = urllib.request.urlopen(request)
        return response.getcode()
    except Exception as e:
        print(f"Lỗi khi gửi yêu cầu: {e}")
        return None

def display_progress(success_count, failure_count):
    progress = [
        "[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", 
        "[■■■■□□□□□□] 40%", "[■■■■■□□□□□] 50%", "[■■■■■■□□□□] 60%", 
        "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%", "[■■■■■■■■■□] 90%", 
        "[■■■■■■■■■■] 100%"
    ]
    for step in progress:
        time.sleep(0.5)
        sys.stdout.write("\r[+] Chuẩn bị... " + step)
        sys.stdout.flush()
    print(f"\n[-] ĐANG HOẠT ĐỘNG TRÊN ID: {REFERRER}")    
    print(f"[:)] {success_count} GB đã được thêm thành công vào tài khoản của bạn.")
    print(f"[#] Tổng: {success_count} Tốt {failure_count} Xấu")
    print("[*] Sau 18 giây, yêu cầu mới sẽ được gửi.")
    time.sleep(18)

def main():
    setup_console()
    print_info()
    
    success_count = 0
    failure_count = 0

    while True:
        url = API_URL_TEMPLATE.format(random_digit_string(3))
        data = create_request_data()
        status_code = send_request(url, data)

        if status_code == 200:
            success_count += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            display_progress(success_count, failure_count)
        else:
            failure_count += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print_info()
            print("[:(] Lỗi khi kết nối tới máy chủ.")
            print(f"[#] Tổng: {success_count} Tốt {failure_count} Xấu")

if __name__ == "__main__":
    main()
