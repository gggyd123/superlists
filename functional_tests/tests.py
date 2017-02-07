import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
	
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://'+arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser=webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		#王庆听说有个很好用的在线代办应用
		#看了一下这个应用的首页
		self.browser.get(self.server_url)
		#他注意到网页的标题和头部都有"To-Do"这个词
		self.assertIn('To-Do',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)
			
		#应用邀请他输入一个代办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		#他在文本框中输入的"购买孔雀羽毛"
		inputbox.send_keys('Buy peacoke feathers')
		
		#他按回车键页面更新了
		#代办事项的表格中显示了"1：购买孔雀羽毛"
		inputbox.send_keys(Keys.ENTER)
		import time
		time.sleep(3)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url,'/lists/.+')
		self.check_for_row_in_list_table('1:Buy peacoke feathers')		
			
		#页面中又显示了一个文本框，可以输入其他代办事项
		#他输入了使用孔雀羽毛做鱼漂
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacoke feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		
		import time
		time.sleep(3)
		#页面再次更新，他的清单中显示了两个代办事项
		self.check_for_row_in_list_table('1:Buy peacoke feathers')		
		self.check_for_row_in_list_table('2:Use peacoke feathers to make a fly')
		
		#现在有个叫天天的新用户访问网站
		
		#我们使用一个新的浏览器会话
		#确保王庆的信息不会从cookie中泄露出来
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		#天天访问首页
		#页面中看不到王庆的清单
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacoke feathers',page_text)
		self.assertNotIn('make a fly',page_text)

		#天天输入一个新的代办事项，新建一个清单
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		import time
		time.sleep(3)
		#天天获得了一个唯一的URL
		tt_list_url = self.browser.current_url
		self.assertRegex(tt_list_url,'/lists/.+')
		self.assertNotEqual(tt_list_url,edith_list_url)

		#这个页面还是没有王庆的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacoke feathers',page_text)
		self.assertIn('Buy milk',page_text)

		#很满意，睡觉去了
		
		#self.fail('Finish the test!')

	def test_layout_and_styling(self):
		#访问首页
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)

		#输入框居中显示
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=5)

		#新建一个清单，输入框仍完美的居中显示
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		import time
		time.sleep(3)
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=5)

