from django.shortcuts import render


def index(request):
    data = {
        'title': 'Main page!!',
        'values': ['BaD', 'monkey', '379'],
        'obj':{
            'car': 'BMW',
            'age': 18,
            'hobby': 'Soccer'
        }
    }
    return render(request, 'main/index.html', data)


def about(request):
    print(request.GET)
    if request.method == "post":
        print(request.POST)

    return render(request, 'main/about.html')


def contacs(request):
    data = {
        'title': 'Контакты',
    }
    return render(request, 'main/contacs.html', data)