from django.core.signals import request_started
from django.shortcuts import render, redirect
from lists.models import Item,List

from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list':list_})
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}/')
def add_item(request,list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/',{'list':list_})