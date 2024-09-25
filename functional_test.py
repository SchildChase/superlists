from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # eva 听说有个在线办事应用
        # 他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

        #他注意到这个网站的标题和头部包含“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)#标题
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn('To-Do',header_text)

        #应用邀请他输入一个代办事项
        input_box = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #他在一个文本框中输入了“Buy peacock feathers" (购买孔雀羽毛)
        #eva的爱好是使用假蝇做饵钓鱼
        input_box.send_keys('Buy peacock')

        #他按回车键后，页面更新了
        #代办事项表格中显示了“1.Buy peacock feathers”
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1:Buy peacock')


        #页面中又显示了一个文本框，可以输入其他待办事项
        #他输入了“Use peacock feathers to make a fly”(使用孔雀羽毛做一个假蝇)
        #eva 做事很有调理
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys('Use peacock feathers')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        #页面再次更新，他的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1:Buy peacock')
        self.check_for_row_in_list_table('2:Use peacock feathers')

        #eva想知道这个网站是否会记住他的清单
        #他看到网站为他生成了一个唯一的URL
        #而且页面中有些文字解说这个功能
        self.fail('Finish the test!')
        #他访问这个URL，发现他的待办事项列表还在

        #他很满意，去睡觉了

if __name__ =='__main__':
    unittest.main(warnings='ignore')
