from django.test import  LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # eva 听说有个在线办事应用
        # 他去看了这个应用的首页
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1:Buy peacock')


        #页面中又显示了一个文本框，可以输入其他待办事项
        #他输入了“Use peacock feathers to make a fly”(使用孔雀羽毛做一个假蝇)
        #eva 做事很有调理
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys('Use peacock feathers')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        #页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1:Buy peacock')
        self.wait_for_row_in_list_table('2:Use peacock feathers')

        #eva想知道这个网站是否会记住他的清单
        #他看到网站为他生成了一个唯一的URL
        #而且页面中有些文字解说这个功能
        self.fail('Finish the test!')
        #他访问这个URL，发现他的待办事项列表还在

        #他很满意，去睡觉了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #eva新建了一个待办事项
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy peacock')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock')
        #他注意到清单有个唯一URL
        eva_list_url = self.browser.current_url
        self.assertRegex(eva_list_url,'/lists/.+')

        # 现在一名叫作弗朗西斯的新用户访问了网站
        ## 我们使用一个新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser=webdriver.Firefox()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy peacock',page_text)
        self.assertNotIn('Use peacock feathers',page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单
        # 他不像伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')

        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(eva_list_url,francis_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_tex = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy peacock',page_tex)
        self.assertIn('Buy milk',page_tex)

        #满意满意