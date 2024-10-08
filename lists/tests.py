from http.client import responses

from django.test import TestCase
from lists.models import Item, List
from lists.views import new_list


class HomePageTest(TestCase):

    def test_use_home_template(self):
        responses = self.client.get("/")
        self.assertTemplateUsed(responses, 'home.html')


class ListAndItemModelTest(TestCase):
    def test_saving_an_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.text, 'item the second')
        self.assertEqual(second_saved_item.list,list_)



class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        responses = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(responses,'list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list =correct_list )
        Item.objects.create(text='itemey 2',list =correct_list )
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        responses = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(responses, 'itemey 1')
        self.assertContains(responses, 'itemey 2')
        self.assertNotContains(responses, 'other list item 1')
        self.assertNotContains(responses, 'other list item 2')
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        responses = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(responses.context['list'],correct_list)


class NewListTest(TestCase):
    #关于'/'的说明：在不修改数据库的“操作”后面加斜线
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        responses = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list= List.objects.first()
        self.assertRedirects(responses,f'/lists/{new_list.id}/')
        #self.assertEqual(responses.status_code, 302)
        #self.assertEqual(responses['location'], '/lists/the_only_list_in_world/')
class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_item(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'a item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        responses = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'a item for an existing list'}
        )
        self.assertRedirects(responses,f'/lists/{correct_list.id}/')

