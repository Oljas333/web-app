from django.shortcuts import render, redirect
from .models import ArtiLes
from  .forms import ArtiLesForm
from  django.views.generic import DetailView, UpdateView, DeleteView

def news_home(request):
    news = ArtiLes.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = ArtiLes
    template_name = 'news/details_view.html'
    context_object_name = 'article'

class NewsUpdateView(UpdateView):
    model =  ArtiLes
    template_name = 'news/create.html'
    #fields = ['title', 'anons', 'full_text', 'date']
    form_class = ArtiLesForm

class NewsDeleteView(DetailView):
    model =  ArtiLes
    sussess_url = '/news/'
    template_name = 'news/news-delete.html'


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArtiLesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
        else:
            error = 'Форма неверная'

    form = ArtiLesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)