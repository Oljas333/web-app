from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def about(request):
    print(request.GET)
    if request.method == "post":
        print(request.POST)
        # return render(request, 'main/about.html', )

    return render(request, 'main/about.html')
