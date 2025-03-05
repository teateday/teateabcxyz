import os, json, sys, requests 
from sys import platform
from time import sleep
from datetime import datetime
from random import randint
from pystyle import Colors, Colorate
import uuid, re
from bs4 import BeautifulSoup

def banner():
 os.system("cls" if os.name == "nt" else "clear")
 banner = f"""

"""
 for X in banner:
  sys.stdout.write(X)
  sys.stdout.flush() 
  sleep(0.00125)

class Facebook_Api(object):
    def __init__(self, cookie):
        self.cookie = cookie

        # Kiểm tra nếu 'c_user=' không có trong cookie
        if 'c_user=' not in cookie:
            raise ValueError("Lỗi: Cookie không hợp lệ hoặc đã hết hạn!")

        try:
            self.user_id = cookie.split('c_user=')[1].split(';')[0]
            
        except IndexError:
            raise ValueError("Lỗi: Cookie")

        self.headers = {
            'authority': 'mbasic.facebook.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'origin': 'https://mbasic.facebook.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, như Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://mbasic.facebook.com/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookie
        }

    def get_thongtin(self):
        try:
            response = requests.get('https://mbasic.facebook.com/profile.php', headers=self.headers)
            
            # Kiểm tra nếu response không thành công
            if response.status_code != 200:
                print("Lỗi: Không thể lấy thông tin tài khoản!")
                return None, None

            home = response.text
            
            # Kiểm tra xem fb_dtsg và jazoest có tồn tại trong response không
            if '<input type="hidden" name="fb_dtsg" value="' not in home or '<input type="hidden" name="jazoest" value="' not in home:
                print("Lỗi: Cookie không hợp lệ hoặc đã hết hạn!")
                return None, None

            self.fb_dtsg = home.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
            self.jazoest = home.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
            ten = home.split('<title>')[1].split('</title>')[0].strip()

            
            return ten, self.user_id
        except Exception as e:
            print(f" Lỗi: {str(e)}")
            return None, None

# Hàm thực hiện request đến Facebook API
def follow(cookie, id):
    try:
        head = {
            "host": "mbasic.facebook.com",
            "content-length": "0",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; Lenovo TB-X505X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": cookie
        }
        link = f"https://mbasic.facebook.com/{id}"
        data = requests.get(link, headers=head).text
        try:
            act = re.search(r'name="fb_dtsg" value="(.*?)"', data).group(1)
            jazoest = re.search(r'name="jazoest" value="(\d+)"', data).group(1)
            follow_link = re.search(f'href="(/a/subscribe.php.*?)"', data).group(1)
            url = f"https://mbasic.facebook.com{follow_link.replace('&amp;', '&')}"
            param = {
                "fb_dtsg": act,
                "jazoest": jazoest
            }
            response = requests.post(url, headers=head, data=param).text
            if "Hapus" in response or "Remove" in response:
                print(f"[SUCCESS] Followed {id}")
            else:
                print(f"[FAILED] Could not follow {id}")
        except AttributeError:
            print("[ERROR] Failed to extract required parameters.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

def page(cookie, id):
    try:
        head = {
            "host": "mbasic.facebook.com",
            "content-length": "0",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; Lenovo TB-X505X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": cookie
        }
        link = f"https://mbasic.facebook.com/{id}"
        data = requests.get(link, headers=head).text
        try:
            act = re.search(r'name="fb_dtsg" value="(.*?)"', data).group(1)
            jazoest = re.search(r'name="jazoest" value="(\d+)"', data).group(1)
            like_link = re.search(f'href="(/a/profile.php.*?)"', data).group(1)
            url = f"https://mbasic.facebook.com{like_link.replace('&amp;', '&')}"
            param = {
                "fb_dtsg": act,
                "jazoest": jazoest
            }
            response = requests.post(url, headers=head, data=param).text
            if "Unlike" in response or "Unlike" in response:
                print(f"[SUCCESS] Liked page {id}")
            else:
                print(f"[FAILED] Could not like page {id}")
        except AttributeError:
            print("[ERROR] Failed to extract required parameters.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

def group(cookie, id):
    try:
        head = {
            "host": "mbasic.facebook.com",
            "content-length": "0",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; Lenovo TB-X505X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": cookie
        }
        link = f"https://mbasic.facebook.com/groups/{id}"
        data = requests.get(link, headers=head).text
        try:
            act = re.search(r'name="fb_dtsg" value="(.*?)"', data).group(1)
            jazoest = re.search(r'name="jazoest" value="(\d+)"', data).group(1)
            join_link = re.search(f'href="(/a/group/join/.*?)"', data).group(1)
            url = f"https://mbasic.facebook.com{join_link.replace('&amp;', '&')}"
            param = {
                "fb_dtsg": act,
                "jazoest": jazoest
            }
            response = requests.post(url, headers=head, data=param).text
            if "Joined" in response or "Leave Group" in response:
                print(f"[SUCCESS] Joined group {id}")
            else:
                print(f"[FAILED] Could not join group {id}")
        except AttributeError:
            print("[ERROR] Failed to extract required parameters.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
class TraoDoiSub_Api (object):
	def __init__ (self, token):
		self.token = token
	
	def main(self):
		try:
			main = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+self.token).json()
			try:
				return main['data']
			except:
				False
		except:
			return False 
	
	def run(self, id):
		try:
			run = requests.get(f'https://traodoisub.com/api/?fields=run&id={id}&access_token={self.token}').json()
			try:
				run['data']['id']
				return True
			except:
				return False
		except:
			return False
	#follow, like, likegiare, likesieure, reaction, comment, share, reactcmt, group, page
	def get_job(self, type):
		try:
			get = requests.get(f'https://traodoisub.com/api/?fields={type}&access_token={self.token}',headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
			return get
		except:
			return False 
		
	def nhan_xu(self, type, id): 
		try:
			nhan = requests.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}',headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}).json()
			try:
				xu = nhan['data']['xu']
				msg = nhan['data']['msg']
				return msg, xu
			except:
				return nhan
		except:
			return False
		
def bongoc(so):
	a= "\033[1;31m────"*so
	print(a)
def hoanthanh(dem, id, type, msg, xu):
	uid = id.split('_')[1] if '_' in id else id
	time=datetime.now().strftime("%H:%M:%S")
	print(f'\033[1;31m[\033[1;33m{dem}\033[1;31m] \033[1;31m| \033[1;36m{time} \033[1;31m| \033[1;36m{type} \033[1;31m| \033[1;33m{uid} \033[1;31m| \033[1;32m{msg} \033[1;31m| \033[1;33m{xu} \033[1;31m|')

def error(id, type):
	time=datetime.now().strftime("%H:%M:%S")
	uid = id.split('_')[1] if '_' in id else id
	print(f'\033[1;31m Đang Lỗi Gì Đó Mong Thông Cảm Nhé', end = '\r'); sleep(2); print('                                                   ', end = '\r')

def Nhap_Cookie():
	list_cookie = []
	i = 0
	while True:
		i += 1
		cookie = input(f'\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1;32mNhập Cookie Facebook Thứ: \033[1;33m{i}: ')
		if cookie == '' and i > 1:
			break
		fb = Facebook_Api(cookie)
		name = fb.get_thongtin()
		if name != 0:
			ten = name[0]
			print('\033[1;31m────────────────────────────────────────────────────────────')
			print(f'\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1;32mTên Facebook: {ten}')
			list_cookie.append(cookie)
			print('\033[1;31m────────────────────────────────────────────────────────────')
		else:
			print('Cookie Facebook Die ! Nhập Lại !!!')
			print('\033[1;31m────────────────────────────────────────────────────────────')
			i-=1
	return list_cookie
def chongblock(delaybl):
	for i in range(delaybl, -1, -1):
		print(f' Hoạt động chống block đang được kích hoạt chờ {i} giây  ',end = '\r');sleep(1); print('                                                        ', end = '\r')
def nghingoi(delaymin, delaymax):
	delay = randint(delaymin, delaymax)
	for i in range(delay, -1, -1):
		sleep(1)

def main():
	ntool = 0
	dem = 0
	banner()
	while True:
		if os.path.exists('configtds.txt'):
			with open('configtds.txt', 'r') as f:
				token = f.read()
			tds = TraoDoiSub_Api(token)
			data = tds.main()
			try:
				print('\033[1;31m[\033[1;37mTAT07\033[1;31m] \033[1;37m=> \033[1;32mNhập [\033[1;33m1\033[1;32m] Giữ Lại Tài Khoản '+ data['user'] )
				print('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập [\033[1;33m2\033[1;32m] Nhập Access_Token TDS Mới')
				chon = input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập \033[1;37m===>:\033[1;33m ')
				if chon == '2':
					os.remove('configtds.txt')
				elif chon == '1':
					pass
				else:
					print('chỉ chọn 1 hoặc 2!!!');bongoc(14)
					continue 
			except:
				os.remove('configtds.txt')
		if not os.path.exists('configtds.txt'):
			token = input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập Access_Token TDS:\033[1;33m ')
			with open('configtds.txt', 'w') as f:
				f.write(token)
		with open('configtds.txt', 'r') as f:
			token = f.read()
		tds = TraoDoiSub_Api(token)
		data = tds.main()
		try:
			xu = data['xu']
			xudie = data['xudie']
			user = data['user']
			break
		except:
			print('Access Token Không Hợp Lệ! vô web lấy Lại ')
			os.remove('configtds.txt')
			continue 
	print('\033[1;31m────────────────────────────────────────────────────────────')
	
	while True:
		if os.path.exists('Cookie_FB.txt'):
			print('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập [\033[1;33m1\033[1;32m] Sử Dụng Cookie Facebook Đã Lưu ')
			print('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập [\033[1;33m2\033[1;32m] Nhập Cookie Facebook Mới')
			chon = input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mVui Lòng Nhập:\033[1;33m ')
			if chon == '1':
				print('\033[1;32mĐang Lấy Dữ Liệu Đã Lưu');sleep(1)
				with open('Cookie_FB.txt', 'r') as f:
					list_cookie = json.loads(f.read())
					break
			elif chon == '2':
				os.remove('Cookie_FB.txt'); bongoc(14)
			else:
				print('chỉ chọn 1 hoặc 2!!!.'); bongoc(14); continue
		if not os.path.exists('Cookie_FB.txt'):
			list_cookie = Nhap_Cookie()
			with open('Cookie_FB.txt', 'w') as f:
				json.dump(list_cookie, f)
			break
	banner()
	print(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mTên Tài Khoản: {user} ')
	print(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mXu Hiện Tại: {xu}')
	print(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mXu Bị Phạt: {xudie} ')
	print(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSố Cookie: {len(list_cookie)} ')
	print('\033[1;31m────────────────────────────────────────────────────────────')
	print('\033[1;32m[1 : LIKE — 2 : COMMENT — 3 : SHARE — 4 : REACTION]')
	print('\033[1;32m[5 : FOLLOW — 6 : PAGE — 7 : REACTCMT —  8 : GROUP]')
	print('\033[1;31m────────────────────────────────────────────────────────────')
	print('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mCó Thể Chọn Nhiều Nhiệm Vụ (Ví Dụ 123...)')
	nhiemvu = input ('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập Số Để Chạy Nhiệm Vụ: ')
	delaymin = int(input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập Delay Min: '))
	delaymax = int(input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mNhập Delay Max: '))
	print('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSau ____ Nhiệm Vụ Thì Kích Hoạt Chống Block.',end='\r')
	nvblock = int(input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSau '))
	print(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSau {nvblock} Nhiệm Vụ Nghỉ Ngơi ____ Giây       ',end='\r')
	delaybl = int(input(f'\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSau {nvblock} Nhiệm Vụ Nghỉ Ngơi '))
	doinick = int(input('\033[1;31m[\033[1;37mNDK\033[1;31m] \033[1;37m=> \033[1;32mSau Bao Nhiêu Nhiệm Vụ Thì Đổi Nick: '))
	print('\033[1;31m────────────────────────────────────────────────────────────')
	while True:
		if len(list_cookie) == 0:
			print('Đã Xoá Tất Cả Cookie, Nhập Lại  ')
			list_cookie = Nhap_Cookie()
			with open('Cookie_FB.txt', 'w') as f:
				json.dump(list_cookie, f)
		for cookie in list_cookie:
			loilike, loicmt, loishare, loicx, loifollow, loipage, loicxcmt, loigroup = 0, 0, 0, 0, 0, 0, 0, 0
			fb = Facebook_Api(cookie)
			name = fb.get_thongtin()
			if name != 0:
				ten = name[0]
				id = name[1]
			else:
				id = cookie.split('c_user=')[1].split(';')[0]
				print(f'Cookie Tài Khoản {id} Die', end='\r');sleep(3); print('                                     ', end = '\r' )
				list_cookie.remove(cookie)
				continue
			cau_hinh = tds.run(id)
			if cau_hinh == True:
				print(f'\033[1;33mĐang Cấu Hình ID FB: {id} \033[1;37m| \033[1;32mTên FB: {ten}')
				print('\033[1;31m────────────────────────────────────────────────────────────')
			else:
				print(f'Cấu Hình Thất Bại ID FB: {id} | Tên FB: {ten} ', end = '\r')
				continue
			ntool = 0
			while True:
			
				nvlike = 1 if '1' in nhiemvu else 0
				nvlike2 = 1 if '1' in nhiemvu else 0
				nvlike3 = 1 if '1' in nhiemvu else 0
				nvcmt = 1 if '2' in nhiemvu else 0
				nvshare = 1 if '3' in nhiemvu else 0
				nvcx = 1 if '4' in nhiemvu else 0
				nvfollow = 1 if '5' in nhiemvu else 0
				nvpage = 1 if '6' in nhiemvu else 0
				nvcxcmt = 1 if '7' in nhiemvu else 0
				nvgroup = 1 if '8' in nhiemvu else 0
			######
				
				if nvlike == 1:
					listlike = tds.get_job('like')
					if listlike == False:
						print('Không Get Được Nhiệm Vụ Like              ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvlike = 0
					elif 'error' in listlike.text:
						if listlike.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listlike.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Like, COUNTDOWN: {str(round(coun, 3))}              ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listlike.json()['error'] , end ='\r')
						nvlike = 0
					else:
						listlike = listlike.json()
						if len(listlike) == 0:
							print('Hết Nhiệm Vụ Like                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvlike = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listlike)} Nhiệm Vụ Like                       ', end = '\r')
							for x in listlike:
								id = x['id']
								like = fb.like(id, 'LIKE')
								if like == False:
									error(id, 'LIKE')
									loilike += 1
								else:
									nhan=tds.nhan_xu('LIKE', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'LIKE', msg, xu)
										loilike = 0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'LIKE')
										loilike += 1
								
								if loilike >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Like !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
			
				if ntool == 1:
					break
			
				if nvlike2 == 1:
					listlike2 = tds.get_job('likegiare')
					if listlike2 == False:
						print('Không Get Được Nhiệm Vụ Like 2                        ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvlike2 = 0
					elif 'error' in listlike2.text:
						if listlike2.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listlike2.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Like 2, COUNTDOWN: {str(round(coun, 3))}                 ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listlike2.json()['error'] , end ='\r')
						nvlike2 = 0
					else:
						listlike2 = listlike2.json()
						if len(listlike2) == 0:
							print('Hết Nhiệm Vụ Like 2                                  ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvlike2 = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listlike2)} Nhiệm Vụ Like 2                  ', end = '\r')
							for x in listlike2:
								id = x['id']
								like = fb.like(id, 'LIKE')
								if like == False:
									error(id, 'LIKE 2')
									loilike+=1
								else:
									nhan=tds.nhan_xu('LIKEGIARE', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'LIKE 2', msg, xu)
										loilike=0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'LIKE 2')
										loilike+=1
								

								if loilike >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Like !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
				if ntool == 1:
					break
			
				if nvlike3 == 1:
					listlike3 = tds.get_job('likesieure')
					if listlike3 == False:
						print('Không Get Được Nhiệm Vụ Like 3                        ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvlike3 = 0
					elif 'error' in listlike3.text:
						if listlike3.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listlike3.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Like 3, COUNTDOWN: {str(round(coun, 3))}                 ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listlike3.json()['error'] , end ='\r')
						nvlike3 = 0
					else:
						listlike3 = listlike3.json()
						if len(listlike3) == 0:
							print('Hết Nhiệm Vụ Like 3                                  ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvlike3 = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listlike3)} Nhiệm Vụ Like 2                  ', end = '\r')
							for x in listlike3:
								id = x['id']
								like = fb.like(id, 'LIKE')
								if like == False:
									error(id, 'LIKE 3')
									loilike+=1
								else:
									nhan=tds.nhan_xu('LIKESIEURE', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'LIKE 3', msg, xu)
										loilike=0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'LIKE 3')
										loilike+=1
								

								if loilike >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Like !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
				if ntool == 1:
					break
				if nvcmt == 1:
					listcmt = tds.get_job('comment')
					if listcmt == False:
						print('Không Get Được Nhiệm Vụ Comment                     ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvcmt = 0
					elif 'error' in listcmt.text:
						if listcmt.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listcmt.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Comment, COUNTDOWN: {str(round(coun, 3))}               ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listcmt.json()['error'] , end ='\r')
						nvcmt = 0
					else:
						listcmt = listcmt.json()
						if len(listcmt) == 0:
							print('Hết Nhiệm Vụ Comment                                 ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvcmt = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listcmt)} Nhiệm Vụ Comment                           ', end = '\r')
							for x in listcmt:
								id = x['id']
								msg = x['msg']
								cmt = fb.comment(id, msg)
								if cmt == False:
									error(id, 'COMMENT')
									loicmt+=1
								else:
									nhan=tds.nhan_xu('COMMENT', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'COMMENT', msg, xu)
										loicmt=0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'COMMENT')
										loicmt+=1
								
								if loicmt >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Comment !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break

				if ntool == 1:
					break
				if nvshare == 1:
					listshare = tds.get_job('share')
					if listshare == False:
						print('Không Get Được Nhiệm Vụ Share                       ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvshare = 0
					elif 'error' in listshare.text:
						if listshare.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listshare.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Share, COUNTDOWN: {str(round(coun, 3))}                ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listshare.json()['error'] , end ='\r')
						nvshare = 0
					else:
						listshare = listshare.json()
						if len(listshare) == 0:
							print('Hết Nhiệm Vụ Share ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvshare = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listshare)} Nhiệm Vụ Share                           ', end = '\r')
							for x in listshare:
								id = x['id']
								share = fb.share(id)
								if share == False:
									error(id, 'SHARE')
									loishare+=1
								else:
									nhan=tds.nhan_xu('SHARE', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'SHARE', msg, xu)
										loishare = 0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'SHARE')
										loishare+=1
								
								if loishare >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Share !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break


				if ntool == 1:
					break
				if nvcx == 1:
					listcx = tds.get_job('reaction')
					if listcx == False:
						print('Không Get Được Nhiệm Vụ Cảm Xúc                             ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvcx = 0
					elif 'error' in listcx.text:
						if listcx.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listcx.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Cảm Xúc, COUNTDOWN: {str(round(coun, 3))}                 ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listcx.json()['error'] , end ='\r')
						nvcx = 0
					else:
						listcx = listcx.json()
						if len(listcx) == 0:
							print('Hết Nhiệm Vụ Cảm Xúc                                 ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvcx = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listcx)} Nhiệm Vụ Cảm Xúc                           ', end = '\r')
							for x in listcx:
								id = x['id']
								type = x['type']
								reac = fb.like(id, type)
								if reac == False:
									error(id, type)
									loilike += 1
								else:
									nhan=tds.nhan_xu(type, id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, type, msg, xu)
										loilike = 0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, type)
										loilike += 1
								
								
								if loilike >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Cảm Xúc !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break

				if ntool == 1:
					break
				if nvfollow == 1:
					listfollow = tds.get_job('follow')
					if listfollow == False:
						print('Không Get Được Nhiệm Vụ Follow                      ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvfollow = 0
						listfollow = []
					elif 'error' in listfollow.text:
						if listfollow.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listfollow.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Follow, COUNTDOWN: {str(round(coun, 3))}                     ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listfollow.json()['error'] , end ='\r')
							sleep(2)
						nvfollow = 0
						listfollow = []
					else:
						listfollow = listfollow.json()
						if len(listfollow) == 0:
							print('Hết Nhiệm Vụ Follow                                    ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvfollow = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listfollow)} Nhiệm Vụ Follow           ', end = '\r')
							for x in listfollow:
								id = x['id']
								follow = fb.follow(id)
								if follow == False:
									error(id, 'FOLLOW')
									loifollow += 1
								else:
									nhan=tds.nhan_xu('FOLLOW', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'FOLLOW', msg, xu)
										loifollow=0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'FOLLOW')
										loifollow += 1
								
								if loifollow >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Follow !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break

				if ntool == 1:
					break
				if nvpage == 1:
					listpage = tds.get_job('page')
					if listpage == False:
						print('Không Get Được Nhiệm Vụ Like Page                 ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvpage = 0
						listpage = []
					elif 'error' in listpage.text:
						if listpage.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listpage.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Page, COUNTDOWN: {str(round(coun, 3))}                         ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listpage.json()['error'] , end ='\r')
						nvpage = 0
						listpage = []
					else:
						listpage = listpage.json()
						if len(listpage) == 0:
							print('Hết Nhiệm Vụ Like Page                                 ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							nvpage = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listpage)} Nhiệm Vụ Like Page           ', end = '\r')
							for x in listpage:
								id = x['id']
								page = fb.page(id)
								if page == False:
									error(id, 'PAGE')
									loipage+=1
								else:
									nhan=tds.nhan_xu('PAGE', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'PAGE', msg, xu)
										loipage = 0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'PAGE')
										loipage+=1
								
								
								if loipage >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Like Page !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
				if ntool == 1:
					break
				if nvcxcmt == 1:
					listcxcmt = tds.get_job('reactcmt')
					if listcxcmt == False:
						print('Không Get Được Nhiệm Vụ Cảm Xúc Comment ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvcxcmt = 0
						listcxcmt = []
					elif 'error' in listcxcmt.text:
						if listcxcmt.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listcxcmt.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Cảm Xúc Comment, COUNTDOWN: {str(round(coun, 3))}                   ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listcxcmt.json()['error'] , end ='\r')
						nvcxcmt = 0
						listcxcmt = []
					else:
						listcxcmt = listcxcmt.json()
						if len(listcxcmt) == 0:
							print('Hết Nhiệm Vụ Cảm Xúc Comment                       ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							listcxcmt = 0
						else:
							print(f'\033[1;32mTìm Thấy {len(listcxcmt)} Nhiệm Vụ Cảm Xúc Comment               ', end = '\r')
							for x in listcxcmt:
								id = x['id']
								type = x['type']
								cxcmt = fb.like(id, type)
								if cxcmt == False:
									error(id, type+'CMT')
									loicxcmt+=1
								else:
									nhan=tds.nhan_xu(type+'CMT', id)
									try:
							#if True:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, type+'CMT', msg, xu)
										loicxcmt=0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, type+'CMT')
										loicxcmt+=1
								
								if loicxcmt >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Cảm Xúc CMT !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
				if ntool == 1:
					break
				if nvgroup == 1:
					listgroup = tds.get_job('group')
					if listgroup == False:
						print('Không Get Được Nhiệm Vụ Group                               ', end = '\r');sleep(2); print('                                                        ', end = '\r')
						nvgroup = 0
						listgroup = []
					elif 'error' in listgroup.text:
						if listgroup.json()['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
							coun = listgroup.json()['countdown']
							print(f'Đang Get Nhiệm Vụ Group, COUNTDOWN: {str(round(coun, 3))}               ', end = '\r'); sleep(2); print('                                                       ', end = '\r')
						else:
							print(listlike.json()['error'] , end ='\r')
						nvgroup = 0
						listgroup = []
					else:
						listgroup = listgroup.json()
						if len(listgroup) == 0:
							print('Hết Nhiệm Vụ Group                                 ', end = '\r');sleep(2); print('                                                        ', end = '\r')
							listgroup = 0
						else:
							print(f'\033[1;32mThấy {len(listgroup)} Nhiệm Vụ Group           ', end = '\r')
						
							for x in listgroup:
								id = x['id']
								gr = fb.group(id)
								if gr == False:
									error(id, 'GROUP')
									loigroup += 1
								else:
									nhan=tds.nhan_xu('GROUP', id)
									try:
										xu = nhan[1]
										msg = nhan[0] 
										dem+=1
										hoanthanh(dem, id, 'GROUP', msg, xu)
										loigroup = 0
										if dem % doinick == 0:
											bongoc(14); print(f'Số Xu Hiện Tại: {xu} | Số Tài Khoản Facebook {len(list_cookie)}'); bongoc(14); ntool = 1; break
										if dem % nvblock == 0:
											chongblock(delaybl)
										else:
											nghingoi(delaymin, delaymax)
									except:
										error(id, 'GROUP')
										loigroup += 1
								
								if loigroup >= 5:
									name = fb.get_thongtin()
									if name == 0:
										print(f'  Cookie Tài Khoản {ten} Đã Bị Out !!!                ')
									else:
										print(f' Tài Khoản {ten} Đã Bị Block Join Group !!!					')
									list_cookie.remove(cookie)
									ntool = 1
									break
				if ntool == 1:
					break
				if nvcx + nvgroup + nvcxcmt + nvpage + nvfollow + nvshare + nvcmt + nvlike == 0:
					for i in range(10, 0, -1):
						print(f' Tất Cả Các Nhiệm Vụ Đã Hết, Chờ chút xíu  ha💟{i} Giây ', end = '\r');sleep(1); print('                                                        ', end = '\r')
	
if __name__ == '__main__':
	main()



	
