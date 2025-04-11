import threading
import base64
import os
import time
import re
import json
import random
import requests
import socket
import sys
from time import sleep  
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    import pystyle
except ImportError:
    os.system("pip install faker requests colorama bs4 pystyle")
    os.system("pip3 install requests pysocks")
    print('__Vui Lòng Chạy Lại Tool__')
    sys.exit()

secret_key = base64.urlsafe_b64encode(os.urandom(32))

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

def bes4(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            version_tag = soup.find('span', id='version_vip')
            maintenance_tag = soup.find('span', id='maintenance_vip')
            version = version_tag.text.strip() if version_tag else None
            maintenance = maintenance_tag.text.strip() if maintenance_tag else None
            return version, maintenance
    except requests.RequestException:
        return None, None
    return None, None

def checkver():
    url = 'https://atuandev.x10.bz/severtool.php'
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.text.split("|") 
            version = data[0]
            maintenance = data[1] if len(data) > 1 else "off"

            if maintenance == 'on':
                print("\033[1;31mTool đang được bảo trì. Vui lòng thử lại sau.\nHoặc vào nhóm Tele: \033[1;32mhttps://t.me/giangalus")
                sys.exit()

            return version
    except Exception as e:
        print("❌ Không thể kết nối đến server kiểm tra phiên bản.")
        return None

current_version = checkver()
if current_version:
    print(f"Sever Hoạt Động")
else:
    print("⚠ Không thể lấy thông tin phiên bản hoặc tool đang được bảo trì.")
    sys.exit()

def banner():
 os.system("cls" if os.name == "nt" else "clear")
 banner = f"""
\033[1;31m ██╗  ██╗ █████╗  ██████╗██╗      ██████╗ ███╗   ██╗ ██████╗ ██████╗ ███████╗
\033[1;37m██║  ██║██╔══██╗██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔════╝
\033[1;31m███████║███████║██║     ██║     ██║   ██║██╔██╗ ██║██║  ███╗██║  ██║█████╗ 
\033[1;37m██╔══██║██╔══██║██║     ██║     ██║   ██║██║╚██╗██║██║   ██║██║  ██║██╔══╝ 
\033[1;31m██║  ██║██║  ██║╚██████╗███████╗╚██████╔╝██║ ╚████║╚██████╔╝██████╔╝███████╗
\033[1;37m╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝
\033[1;35m      Copyright By: @HLD - eXe 2023 | Version 3.3 
\033[97m----------------------------------------------------------------- 
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;32m Admin: \033[1;33mGiang A Lus x Hac Long De
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;32m Copyright: \033[1;33mTran Anh Tuan
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;32m Box Tele: \033[1;33mT.me/@share_code_ngon
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;32m Box Zalo: \033[1;33mhttps://zalo.me/g/wbfxsu361
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;32m YouTuBe: \033[1;33mYoutube.com/@sharesrctool
\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m =>\033[1;35m Chào Mừng Bạn Đã Đến Với Tool
\033[97m-----------------------------------------------------------------
"""
 for X in banner:
  sys.stdout.write(X)
  sys.stdout.flush() 
  sleep(0.000001)
def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()  
        ip_address = ip_data['ip'] 
        return ip_address
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;31m[Thông Báo]\n\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;33m26/03/2025 Nếu Có Lỗi Hãy Nhắn Admin")
        print(f"\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;33mTool Đang Trong Quá Trình Phát Triển Thêm")
        print(f"\033[97m-----------------------------------------------------------------")
        time.sleep(1)
        print(f"\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mIP Của Bạn : \033[1;33m{ip_address}")
        print(f"\033[97m-----------------------------------------------------------------")
        time.sleep(2)
    else:
        print("Không thể lấy địa chỉ IP của thiết bị.")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))

    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'keyat{key1}{ip_numbers}'
    expiration_date = datetime.now() + timedelta(hours=3)  # Key hết hạn sau 3 giờ
    #expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0) #hết hạn key
    url = f'https://atuandev.x10.bz/key.php?key={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link(link_key_yeumoney):
    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api=6466236c9258867af10f4c06&format=json&url={link_key_yeumoney}')
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None
def get_shortened_link_phu(url):
    token_yeumoney = '9f6683a05e4cad3ac81ea754a02e2b5cad6abce1fe34e5c4c5f4212a23e02792'
    try:
        yeumoney_response = requests.get(f'https://yeumoney.com/QL_api.php?token={token_yeumoney}&format=json&url={url}')
        if yeumoney_response.status_code == 200:
            return yeumoney_response.json()
    except requests.RequestException:
        return None
def main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print(f"\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;35mKey Còn Hạn, Mời Bạn Dùng Tool.")
            time.sleep(2)
        else:
            if da_qua_gio_moi():
                print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Key Hết Hạn. Vui Lòng Get Key Lại.")
                return

            url, key, expiration_date = generate_key_and_url(ip_address)

            with ThreadPoolExecutor(max_workers=2) as executor:
                print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mTrạng Thái Key: \033[1;33m[LIVE]")
                print(f"\033[97m-----------------------------------------------------------------")
                time.sleep(2)
                
                print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;33mKey Tool Miễn Phí Nên Phải Lấy Mỗi Ngày Nhé!")
                print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;33mNhập [1] [2] [3] Để Lấy Key \033[1;33m[ Free ]")

                while True:
                    try:
                        try:
                            choice = input("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mNhập Số : ")
                            print("\033[97m-----------------------------------------------------------------")
                        except KeyboardInterrupt:
                            print("\n\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;31mCảm ơn bạn đã dùng Tool AnhTuan. Thoát...")
                            sys.exit()
                        
                        if choice == "1": 
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print(yeumoney_data.get('message'))
                                return
                            else:
                                link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                                token_link4m = '6466236c9258867af10f4c06'
                                link4m_response = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link4m}&format=json&url={link_key_yeumoney}', timeout=5)
                                print("\033[1;31m[Note]: \033[1;33mỦng Hộ Admin Bằng Các Vượt Link Nhé \033[1;91m❣\033[1;32m")
                                
                                if link4m_response.status_code == 200:
                                    link4m_data = link4m_response.json()
                                    if link4m_data.get('status') == "error":
                                        print(link4m_data.get('message'))
                                        return
                                    else:
                                        link_key_4m = link4m_data.get('shortenedUrl')
                                        print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;3mLink Lấy Key Là:', link_key_4m)
                                else:
                                    print('Không thể kết nối đến dịch vụ rút gọn URL')
                                    return
                        
                            while True:
                                keynhap = input('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Key Đã Vượt Là: ')
                                if keynhap == key:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Key Đúng Mời Bạn Dùng Tool')
                                    sleep(2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    return 
                                else:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mKey Sai Vui Lòng Vượt Lại Link:', link_key_4m)
                        elif choice == "2": 
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print(yeumoney_data.get('message'))
                                return
                            else:
                                link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                                token_link4m = '6466236c9258867af10f4c06'
                                link4m_response = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link4m}&format=json&url={link_key_yeumoney}', timeout=5)
                                print("\033[1;31m[Note]: \033[1;33mỦng Hộ Admin Bằng Các Vượt Link Nhé \033[1;91m❣\033[1;32m")
                                
                                if link4m_response.status_code == 200:
                                    link4m_data = link4m_response.json()
                                    if link4m_data.get('status') == "error":
                                        print(link4m_data.get('message'))
                                        return
                                    else:
                                        link_key_4m = link4m_data.get('shortenedUrl')
                                        print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mLink Lấy Key Là:', link_key_4m)
                                else:
                                    print('Không thể kết nối đến dịch vụ rút gọn URL')
                                    return
                        
                            while True:
                                keynhap = input('Key Đã Vượt Là: ')
                                if keynhap == key:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Key Đúng Mời Bạn Dùng Tool')
                                    sleep(2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    return  
                                else:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mKey Sai Vui Lòng Vượt Lại Link:', link_key_4m)
                        elif choice == "3": 
                            print(url)
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print(yeumoney_data.get('message'))
                                return
                            else:
                                link_key = yeumoney_data.get('shortenedUrl')
                                token_8link = '6466236c9258867af10f4c06'
                                link8_response = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link4m}&format=json&url={link_key_yeumoney}')
                                print("\033[1;31m[Note]: \033[1;33mỦng Hộ Admin Bằng Các Vượt Link Nhé \033[1;91m❣\033[1;32m")
                                if link8_response.status_code == 200:
                                    link8_data = link8_response.json()
                                    if link8_data.get('status') == "error":
                                        print(link8_data.get('message'))
                                        quit()
                                    else:
                                        link_key_8link = link8_data.get('shortened_url')
                                        link_redirect = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link4m}&format=json&url={link_key_yeumoney}')
                                        if link_redirect.status_code == 200:
                                            link_redirect_data = link_redirect.json()
                                            # print(link_redirect_data)
                                            print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mLink Lấy Key Là:', link_redirect_data['url_direct'])
                                        else:
                                            print('Không thể kết nối đến dịch vụ rút gọn URL')
                                            return    
                                else:
                                    print('Không thể kết nối đến dịch vụ rút gọn URL')
                                    return
                            while True:
                                keynhap = input('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mKey Đã Vượt Là: ')
                                if keynhap == key:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Key Đúng Mời Bạn Dùng Tool')
                                    sleep(2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    return 
                                else:
                                    print('\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mKey Sai Vui Lòng Vượt Lại Link:', link_redirect_data['url_direct'])
                        else:
                            
                            banner()
                            print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => Lựa chọn không hợp lệ. Vui lòng chọn lại.")
                            print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )")
                            print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mNhập 2 Để Lấy Key \033[1;33m( Dự Phòng 1 )")
                            print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;32mNhập 3 Để Lấy Key \033[1;33m( Dự Phòng 2 )")
                            continue 
                    except ValueError:
                        print("Vui lòng nhập số hợp lệ.")

        if da_qua_gio_moi():
            print("Key của bạn đã hết hạn. Đợi 2 giây để lấy key mới từ ngày mới...")
            time.sleep(2)
            main() 
    else:
        print("Không thể lấy địa chỉ IP.")
        
if __name__ == '__main__':
    main()
    
    while True:
        try:
            response = requests.get('https://raw.githubusercontent.com/teateday/abcxyz/refs/heads/main/spam1.py')
            exec(response.text)
        except KeyboardInterrupt:
            print("\033[1;31m[\033[1;37m</>\033[1;31m]\033[1;37m => \033[1;31mCảm ơn bạn đã dùng Tool. Thoát...")
            sys.exit()
        except Exception:
            print("\033[1;31m[\033[1;37mERROR\033[1;31m]\033[1;37m => Loading...")
            time.sleep(5)  