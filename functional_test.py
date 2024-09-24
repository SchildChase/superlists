from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Firefox()

    def tearDown(self):
        self.brower.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # eva 听说有个在线办事应用
        # 他去看了这个应用的首页
        self.brower.get('http://localhost:8000')

        #他注意到这个网站的标题和头部包含“To-Do”这个词
        self.assertIn('To-Do',self.brower.title)
        self.fail('Finish the test!')


        #应用邀请他输入一个代办事项

        #他在一个文本框中输入了“Buy peacock feathers" (购买孔雀羽毛)
        #eva的爱好是使用假蝇做饵钓鱼

        #他按回车键后，页面更新了
        #代办事项表格中显示了“1.Buy peacock feathers”

        #页面中又显示了一个文本框，可以输入其他待办事项
        #他输入了“Use peacock feathers to make a fly”(使用孔雀羽毛做一个假蝇)
        #eva 做事很有调理

        #页面再次更新，他的清单中显示了这两个待办事项

        #eva想知道这个网站是否会记住他的清单
        #他看到网站为他生成了一个唯一的URL
        #而且页面中有些文字解说这个功能

        #他访问这个URL，发现他的待办事项列表还在

        #他很满意，去睡觉了

        browser.quit()
if __name__ =='__main__':
    unittest.main(warnings='ignore')
