from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import MyModel

# Create your views here.

def show_all_models(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            name = 'No name'
        description = request.POST.get('description')
        if not description:
            description = 'No description'
        MyModel.objects.create(name=name, description=description)
        return redirect('my_app:models')
    all_models = MyModel.objects.all()
    context = {'models': all_models, 'title': 'My Models'}
    return render(request, 'my_app/models.html', context)


def index(request: HttpRequest) -> HttpResponse:
    context = {'title': 'My App', 'list': ['a', 'b', 'c'], 'dict': {'a': 1,
                                                                    'b': 2}}
    return render(request, 'my_app/index.html', context)

def home(request: HttpRequest) -> HttpResponse:
    return redirect('my_app:index')

def show_one_model(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'GET':
        model = MyModel.objects.get(id=id)
        context = {'model': model, 'title': model.name}
        return render(request,'my_app/one_model.html', context)
    elif request.method == 'POST':
        model = MyModel.objects.get(id=id)
        model.name = request.POST.get('name')
        model.description = request.POST.get('description')
        model.save()
        return redirect('my_app:one_model', id)
    else:
        return HttpResponse(f'Method {request.method} not allowed')


def delete_model(request: HttpRequest, id: int) -> HttpResponse:
    model = MyModel.objects.get(id=id)
    model.delete()
    return redirect('my_app:models')