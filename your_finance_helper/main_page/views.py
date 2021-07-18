from django.shortcuts import render


def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['some', '321', 'anybody'],
        'obj': {
            'car': 'BMW',
            'age': 18,
            'hobby': 'basketball'
        }
    }
    return render(request, 'main_page/index.html', data)


def about(request):
    return render(request, 'main_page/about.html')
