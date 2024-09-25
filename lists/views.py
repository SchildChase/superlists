from django.shortcuts import render
from lists.models import Item

from django.http import HttpResponse

# Create your views here.
def home_page(request):
    item = Item()
    item.text = request.POST.get('item_text','')
    item.save()
    
    #if request.method == 'POST':
        #return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html',{
        'new_item_text':request.POST.get('item_text',''),
    })
    #HttpResponse('<html><title>To-Do lists</title></html>')