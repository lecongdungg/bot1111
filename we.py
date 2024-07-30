import telebot
import subprocess
import time
import logging
import shutil
import os
import uuid
import threading

API_TOKEN = '6752131474:AAHx2UIGONwXULSVo9mW_L2pQr9Ve-FZijk'
bot = telebot.TeleBot(API_TOKEN)

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Từ điển để theo dõi trạng thái của các ID
running_ids = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = (
        "Chào mừng bạn đến với bot tặng GB WARP! của Lê Công Dụng \nMua code liên hệ @lecongdung102\n\n"
        "Sử dụng bot như sau:\n\n"
        "Cách lấy id như sau: \n"
        "1. Nhấn vào dấu 3 gạch trên góc phải màn hình\n"
        "2. Nhấn vào Advanced\n"
        "3. Nhấn vào Diagnostics \n"
        "4. Kéo xuống dưới copy hết đoạn mã ID \n"
        "Sau khi lấy ID vào BOT gửi lệnh :\n/id <user_id>,<time_in_seconds> để nhận 1 GB WARP cho ID cụ thể trong khoảng thời gian bạn đã cài đặt. (20s sẽ nhận được 1 GB, thời gian tối đa là 1000s)\n\n"
        "Ví dụ:\n /id 6752131474:AAHx2UIGONwXULSVo9mW_L2pQr9Ve-FZijk,1000\n"
    )
    bot.reply_to(message, welcome_message)

def handle_user_request(user_id, total_run_time, message):
    interval = 20
    logging.info("Lấy được ID người dùng: %s và thời gian chạy: %d giây", user_id, total_run_time)

    # Phản hồi ngay lập tức rằng bot đã nhận được ID và thời gian chạy
    acknowledgement_message = f"Đã nhận được ID:\n-  {user_id} \n - Thời gian chạy là: {total_run_time} giây."
    bot.reply_to(message, acknowledgement_message)

    # Tạo một bản sao tạm thời của warp.py cho người dùng này
    temp_script = f"warp_{uuid.uuid4()}.py"
    shutil.copyfile("warp.py", temp_script)

    # Thay thế ID trong file script tạm thời
    with open(temp_script, "r") as file:
        data = file.readlines()

    for i, line in enumerate(data):
        if line.strip().startswith('referrer ='):
            data[i] = f'referrer = "{user_id}"\n'
            logging.info("Đã thay thế ID referrer ở dòng %d trong file %s", i, temp_script)

    with open(temp_script, "w") as file:
        file.writelines(data)
    logging.info("Đã cập nhật %s với ID referrer mới", temp_script)

    # Chạy file script trong khoảng thời gian quy định và phản hồi sau mỗi 20 giây
    num_intervals = total_run_time // interval
    for _ in range(num_intervals):
        process = subprocess.Popen(['python', temp_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Đã bắt đầu chạy script %s", temp_script)

        time.sleep(interval)
        process.terminate()
        logging.info("Đã dừng script %s sau %d giây", temp_script, interval)

        stdout, stderr = process.communicate()
        if stdout:
            logging.info("Kết quả đầu ra của script %s: %s", temp_script, stdout.decode())
        if stderr:
            logging.error("Kết quả lỗi của script %s: %s", temp_script, stderr.decode())

        response_message = f"LÊ CÔNG DỤNG ĐÃ TẶNG 1 GB WARP THÀNH CÔNG CHO ID: {user_id}.\n\n- BOT nhận Warp đang được phát triển bởi @lecongdung102 mua code liên hệ @lecongdung102"
        logging.info("Gửi phản hồi tới người dùng: %s", response_message)
        bot.reply_to(message, response_message)

    # Phản hồi sau khi hoàn thành tất cả các khoảng thời gian
    final_message = (
        f"Lê Công Dụng tặng thành công 1 GB WARP cho ID: {user_id}.\n\n"
        "Lưu ý sau 20s sẽ nhận được 1 GB và cấm dùng nhiều lần liên tục sẽ gặp lỗi hãy đợi hết thời gian hãy xin tiếp\n\n- BOT nhận Warp đang được phát triển bởi @lecongdung102 mua code liên hệ @lecongdung102"
    )
    logging.info("Gửi phản hồi cuối cùng tới người dùng: %s", final_message)
    bot.reply_to(message, final_message)

    # Xóa file script tạm thời
    os.remove(temp_script)
    logging.info("Đã xóa file script tạm thời: %s", temp_script)

    # Xóa ID khỏi danh sách chạy
    del running_ids[user_id]

@bot.message_handler(commands=['id'])
def handle_id(message):
    try:
        logging.info("Nhận được tin nhắn: %s", message.text)
        
        # Lấy ID và thời gian chạy từ tin nhắn
        parts = message.text.split()[1].split(',')
        user_id = parts[0]
        total_run_time = int(parts[1])
        
        # Kiểm tra xem thời gian chạy có vượt quá giới hạn 1000 giây hay không
        if total_run_time > 1000:
            bot.reply_to(message, "Thời gian chạy không được vượt quá 1000 giây. Vui lòng thử lại với thời gian ngắn hơn.")
            return

        # Kiểm tra xem ID này có đang chạy hay không
        if user_id in running_ids:
            bot.reply_to(message, f"ID: {user_id} đang chạy. Vui lòng đợi cho đến khi hoàn thành trước khi yêu cầu tiếp.")
            return
        
        # Đánh dấu ID này là đang chạy
        running_ids[user_id] = True

        # Tạo một luồng mới để xử lý yêu cầu của người dùng
        user_thread = threading.Thread(target=handle_user_request, args=(user_id, total_run_time, message))
        user_thread.start()
        
    except Exception as e:
        logging.error("Đã xảy ra lỗi: %s", str(e))
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

logging.info("Bot đang chạy...")
bot.polling()
