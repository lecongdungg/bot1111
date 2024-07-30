import telebot
import subprocess
import time
import logging

API_TOKEN = '6752131474:AAHx2UIGONwXULSVo9mW_L2pQr9Ve-FZijk'
bot = telebot.TeleBot(API_TOKEN)

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = (
        "Chào mừng bạn đến với bot tặng GB WARP!\n"
        "Sử dụng bot như sau:\n\n"
        "Gửi lệnh:\n /id <user_id>,<time_in_seconds> để tặng 1 GB WARP cho ID cụ thể trong khoảng thời gian nhất định.\n\n"
        "Ví dụ:\n /id 6752131474:AAHx2UIGONwXULSVo9mW_L2pQr9Ve-FZijk,1000\n"
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['id'])
def handle_id(message):
    try:
        logging.info("Nhận được tin nhắn: %s", message.text)
        
        # Lấy ID và thời gian chạy từ tin nhắn
        parts = message.text.split()[1].split(',')
        user_id = parts[0]
        total_run_time = int(parts[1])
        interval = 20
        logging.info("Lấy được ID người dùng: %s và thời gian chạy: %d giây", user_id, total_run_time)

        # Phản hồi ngay lập tức rằng bot đã nhận được ID và thời gian chạy
        acknowledgement_message = f"Đã nhận được ID: {user_id} với thời gian chạy là: {total_run_time} giây."
        bot.reply_to(message, acknowledgement_message)

        # Thay thế ID trong file script
        with open("warp.py", "r") as file:
            data = file.readlines()

        for i, line in enumerate(data):
            if line.strip().startswith('referrer ='):
                data[i] = f'referrer = "{user_id}"\n'
                logging.info("Đã thay thế ID referrer ở dòng %d", i)

        with open("warp.py", "w") as file:
            file.writelines(data)
        logging.info("Đã cập nhật warp.py với ID referrer mới")

        # Chạy file script trong khoảng thời gian quy định và phản hồi sau mỗi 20 giây
        num_intervals = total_run_time // interval
        for _ in range(num_intervals):
            process = subprocess.Popen(['python', 'warp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("Đã bắt đầu chạy script warp.py")

            time.sleep(interval)
            process.terminate()
            logging.info("Đã dừng script warp.py sau %d giây", interval)

            stdout, stderr = process.communicate()
            if stdout:
                logging.info("Kết quả đầu ra của script: %s", stdout.decode())
            if stderr:
                logging.error("Kết quả lỗi của script: %s", stderr.decode())

            response_message = f"LÊ CÔNG DỤNG ĐÃ TẶNG 1 GB WARP THÀNH CÔNG CHO ID: {user_id}."
            logging.info("Gửi phản hồi tới người dùng: %s", response_message)
            bot.reply_to(message, response_message)
        
        # Phản hồi sau khi hoàn thành tất cả các khoảng thời gian
        final_message = (
            f"Hoàn thành việc tặng GB WARP cho ID: {user_id} trong {total_run_time} giây.\n\n"
            "Lưu ý sau khi hết thời gian, có thể xin thêm một lần nữa, nếu làm liên tục sẽ gặp lỗi"
        )
        logging.info("Gửi phản hồi cuối cùng tới người dùng: %s", final_message)
        bot.reply_to(message, final_message)
    except Exception as e:
        logging.error("Đã xảy ra lỗi: %s", str(e))
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

logging.info("Bot đang chạy...")
bot.polling()
