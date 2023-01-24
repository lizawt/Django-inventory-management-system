from django.shortcuts import render, redirect
from django.contrib import messages
from stockmgmt.models import Stock
from stockmgmt.forms import StockCreateForm, StockSearchForm, StockUpdateForm


def home(request):
    title = 'Welcome: This is the Home Page'
    text = 'wow'#check out how it works in the template
    context = {
        "title": title,
        "text": text
        }
    return render(request, "home.html",context)
def list_item(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
        item_name__icontains=form['item_name'].value())

        context = {
	    "form": form,
	    "header": header,
	    "queryset": queryset,
    }
    return render(request, "list_items.html", context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_item.html", context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset) #changed
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('/list_items')

    context = {
        'form':form
    }
    return render(request, 'add_item.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted succesfully!')
        return redirect('/list_items')
    return render(request, 'delete_items.html')