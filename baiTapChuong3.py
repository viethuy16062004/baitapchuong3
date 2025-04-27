import os
import shutil
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path='D:/TuDongHoa/BaiTapChuong3/baiTapChuong3.env')

MAIL_SENDER = os.getenv('MAIL_SENDER')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_RECEIVER = os.getenv('MAIL_RECEIVER')
SOURCE_FOLDER = './databases'  
BACKUP_FOLDER = './backup'

def gui_email(chu_de, noi_dung):
    try:
        message = MIMEMultipart()
        message['From'] = MAIL_SENDER
        message['To'] = MAIL_RECEIVER
        message['Subject'] = chu_de
        message.attach(MIMEText(noi_dung, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MAIL_SENDER, MAIL_PASSWORD)
            server.send_message(message)

        print('Đã gửi email thông báo.')
    except Exception as e:
        print(f'Lỗi khi gửi email: {e}')

def sao_luu_csdldata():
    try:
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)
        backup_success = False
        for filename in os.listdir(SOURCE_FOLDER):
            if filename.endswith(('.sql', '.sqlite3')): 
                src_path = os.path.join(SOURCE_FOLDER, filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dst_filename = f"{os.path.splitext(filename)[0]}_backup_{timestamp}{os.path.splitext(filename)[1]}"
                dst_path = os.path.join(BACKUP_FOLDER, dst_filename)
                shutil.copy2(src_path, dst_path)
                backup_success = True
        if backup_success:
            gui_email('Backup thành công', f'Backup database thành công vào lúc {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        else:
            gui_email('Backup thất bại', 'Không tìm thấy file để sao lưu.')

    except Exception as e:
        gui_email('Backup thất bại', f'Lỗi trong quá trình backup: {e}')

schedule.every().day.at("15:42").do(sao_luu_csdldata)

print("Đang chạy lịch backup database hàng ngày")
while True:
    schedule.run_pending()
    time.sleep(1)
