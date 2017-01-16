from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser=webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#王庆听说有个很好用的在线代办应用
		#看了一下这个应用的首页
		self.browser.get('http://localhost:8000')
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
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1:Buy peacoke feathers' for row in rows),
			"New to-do item did not appear in table"
		)
		
		#页面中又显示了一个文本框，可以输入其他代办事项
		#他输入了使用孔雀羽毛做鱼漂
		
		#页面再次更新，他的清单中显示了两个代办事项
		
		#王庆想知道网站是否会记住这个代办清单
		
		#他看到网站为他生成了一个唯一的URL
		#而且有一些文字解说这个功能
		
		#他访问这个URL发现这个他的代办还在
		
		#很满意，睡觉去了
		
		self.fail('Finish the test!')

if __name__=='__main__':
	unittest.main()
