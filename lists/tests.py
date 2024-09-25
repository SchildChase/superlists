from django.test import TestCase

class HomePageTest(TestCase):

    def test_use_home_template(self):
        responses = self.client.get("/")
        self.assertTemplateUsed(responses, 'home.html')

    def test_can_save_a_POST_request(self):
        responses = self.client.post('/', data={'item_text':'A new list item'})
        self.assertIn('A new list item', responses.content.decode())
        self.assertTemplateUsed(responses, 'home.html')
