from http.client import responses

from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_use_home_template(self):
        responses = self.client.get("/")
        self.assertTemplateUsed(responses, 'home.html')

    def test_can_save_a_POST_request(self):
        responses = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        # self.assertIn('A new list item', responses.content.decode())
        # self.assertTemplateUsed(responses, 'home.html')

    def test_redirects_after_POST(self):
        responses = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(responses.status_code, 302)
        self.assertEqual(responses['location'], '/lists/the_only_list_in_world/')

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)




class ItemModelTest(TestCase):

    def test_saving_an_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.text, 'item the second')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        responses = self.client.get('/lists/the_only_list_in_world/')
        self.assertTemplateUsed(responses,'list.html')

    def test_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        responses = self.client.get('/lists/the_only_list_in_world/')

        self.assertContains(responses, 'itemey 1')
        self.assertContains(responses, 'itemey 2')


