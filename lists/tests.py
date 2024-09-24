from django.test import TestCase

class HomePageTest(TestCase):

    def test_use_home_template(self):
        responses = self.client.get("/")
        self.assertTemplateUsed(responses, 'home.html')