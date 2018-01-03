#coding=UTF-8

from transitions.extensions import GraphMachine
import requests
from bs4 import BeautifulSoup
from langconv import*
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import os
import zipfile
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

firebase = None
class TocMachine(GraphMachine):
	global firebase
	def __init__(self, **machine_configs):
		self.machine = GraphMachine(
		model = self,
		**machine_configs
		)
		cred = credentials.Certificate('storytogether-be978-firebase-adminsdk-44g5v-1ea7f4860a.json')
		firebase_admin.initialize_app(cred,{
			'databaseURL':'https://storytogether-be978.firebaseio.com'})

	def is_going_to_home(self, update, bot):
		text = update.message.text
		boolean = (text.find('home') >= 0)
		return boolean
	
	def is_going_to_novel(self, update, bot):
		text = update.message.text
		boolean = (text.find('novel') >= 0)
		return boolean
	
	def is_going_to_write(self, update, bot):
		text = update.message.text
		boolean = (text.find('write') >= 0)
		return boolean
	
	def is_going_to_web(self, update, bot):
		text = update.message.text
		boolean = (text.find('web') >= 0)
		return boolean
	
	def is_back_to_home_novel(self, update, bot):
		if self.state != 'novel':
			return False

		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean
	
	def is_back_to_home_web(self, update, bot):
		if self.state != 'web':
			return False

		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean
	
	def is_back_to_novel(self, update, bot):
		if self.state != 'biqukan':
			return False

		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean
		
		if text.find('http://www.biqukan.com/') >= 0:
			update.message.reply_text("給偶一點時間~~><")
			chat_id = update.message.chat_id
			bot.send_document(chat_id,document = open('loading.gif','rb'))
			
			request = requests.get(update.message.text)
			request.encoding = 'gbk'
			soup = BeautifulSoup(request.text,'html.parser')
			novel_name = soup.find( property = 'og:title')
			novel_name = novel_name.get('content')
			chapter = soup.find_all('div',class_='listmain')
			chapter_soup = BeautifulSoup(str(chapter),'html.parser')
			
			directory = '/home/dianarolien/TOC-Project-2017/novel/'+novel_name
			isExist = os.path.exists(directory)
			if isExist == False:
				os.mkdir(directory)

			if os.path.exists(directory+'.zip') == True:
				bot.send_document(chat_id,document = open(directory+'.zip','rb'))
				return boolean

			download_flag = False
			for child in chapter_soup.dl.children:
				if child != '\n':
					if child.string.find(u'正文卷') >= 0:
						download_flag = True
				
					if download_flag == True and child.a != None:
						download_url = 'http://www.biqukan.com' + child.a.get('href')
						download_req = requests.get(download_url)
						download_req.encoding = 'gbk'
						download_soup = BeautifulSoup(download_req.text,'html.parser')
						download_content = download_soup.find_all(id = 'content', class_= 'showtxt')
						content = BeautifulSoup(str(download_content),'html.parser')
						content = content.div.text.replace('        ',"\n")
						download_name = child.string
						
						path = directory+'/'+ download_name+'.txt'
						isExist = os.path.exists(path)
						if isExist == False:
							f = open(path,'w',encoding = 'utf-8')
							f.write(download_name+'\n\n')
							f.write(content)
							f.close()
			
			zp = zipfile.ZipFile( directory +'.zip','w',zipfile.ZIP_DEFLATED)
			for dirname,subdirs,files in os.walk(directory):
				for filename in files:
					absname = os.path.abspath(os.path.join(dirname,filename))
					zp.write(absname,filename)
			zp.close()
			bot.send_document(chat_id,document = open(directory+'.zip','rb'))
			return True

		else:
			update.message.reply_text(u"網址錯了喔！！")

		return boolean
		
	def is_back_to_novel2(self, update, bot):
		
		if self.state != 'quanben':
			return False
		
		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean
		
		driver = webdriver.Chrome('/home/dianarolien/Downloads/chromedriver')
		driver.get('http://big5.quanben5.com/')
		#search_input = WebDriverWait(driver,3).until(EC.presence_of_element_located(By.name,'keywords'))#.find_element_by_name('keywords')
		#search_input.send_keys('pig')

	def is_back_to_home_write(self,update,bot):
		if self.state != 'write':
			return False

	def is_back_to_write_writing(self, update, bot):
		if self.state != 'writing':
			return False
		
		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean

		ref = db.reference('story')
		ref.set(ref.get()+'\n'+text)
		
	def is_back_to_write_reading(self, update, bot):
		if self.state != 'reading':
			return False
		
		text = update.message.text
		boolean =  (text.find('back') >= 0)
		if boolean == True:
			return boolean
		
		update.message.reply_text(u"使用 /back 回到上一層\n/home 回到主選單")

	def is_going_to_biqukan(self, update ,bot):
		text = update.message.text
		boolean =  (text.find('biqukan') >= 0)
		return boolean
		
	def is_going_to_quanben(self, update, bot):
		text = update.message.text
		boolean =  (text.find('quanben') >= 0)
		return boolean
	
	def is_going_to_writing(self, update, bot):
		text = update.message.text
		boolean =  (text.find('writing') >= 0)
		return boolean
	
	def is_going_to_reading(self, update, bot):
		text = update.message.text
		boolean =  (text.find('reading') >= 0)
		return boolean
	
	def on_exit_home(self, update, bot):
		print('Leaving home')

	def on_enter_novel(self, update, bot):
		update.message.reply_text(u"Piggy 提供網站下載你想看的小說～\n/biqukan (筆趣看)\n")

	def on_exit_novel(self, update, bot):
		print('Leaving novel')
	
	def on_enter_write(self, update, bot):
		print ('Enter write')
		update.message.reply_text(u"Piggy 提供和其他使用者一起共筆一本小說的服務～\n/writing 開始共筆 \n/reading 讀取此小說")

	def on_exit_write(self, update, bot):
		print('Leave write')
	
	def on_enter_writing(self, update, bot):
		print ('Enter writing')
		update.message.reply_text(u"開始編輯小說：從現在開始,除了 /back 跟 /home ,你打的每一個字都會變成小說的內容,請小心使用～三思而後行～")

	def on_exit_writing(self, update, bot):
		print ('Leaving writing')
	
	def on_enter_reading(self, update, bot):
		print ('Enter reading')
		ref = db.reference('story')
		update.message.reply_text(ref.get())

	def on_exit_reading(self, update, bot):
		print ('Leaving reading')

	def on_enter_web(self, update, bot):
		print ('Enter web')
		update.message.reply_text(u"嗨,推薦一些好用的相關網站：\n\n小說網：\n晉江文學城：http://www.jjwxc.net/\n全本小說網：http://big5.quanben5.com/\n筆趣看：http://www.biqukan.com/\n宙斯小說網：http://tw.zhsxs.com/gengxin/info_1.html\n輕之國度：https://www.lightnovel.cn/forum.php\n\n購書網：\n誠品網路書店：http://www.eslite.com/\n博客來：http://www.books.com.tw/\n金石堂：https://www.kingstone.com.tw/\nAmazon:https://www.amazon.co.jp/gp/top-sellers/books/ref=crw_ratp_ts_books\nTAAZE:http://www.taaze.tw/index.html\n城邦讀書花園：http://www.cite.com.tw/\n若水堂：http://www.waterlike.com.tw/")

	def on_exit_web(self, update, bot):
		print('Leave web')

	def on_enter_biqukan(self, update, bot):
		print ('Enter biqukan')
		update.message.reply_text(u"嗨,歡迎使用筆趣看:http://www.biqukan.com\n輸入一個你中意的小說的網址(ex:http://www.biqukan.com/17_17065/)\nPiggy 會幫你打包txt檔送給你～")

	def on_exit_biqukan(self, update, bot):
		print('Leaving biqukan')
			
	def on_enter_quanben(self, update, bot):
		update.message.reply_text("嗨,歡迎使用全本小說網:http://big5.quanben5.com/")
	

	def on_exit_quanben(self, update, bot):
		print('Leaving quanben')
