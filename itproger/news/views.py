from django.shortcuts import render, redirect
from .models import ArtiLes, Comment, Category
from .forms import ArtiLesForm, CommentForm, CategoryForm
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework import generics
from .serializers import ArtiLesSerializer
from rest_framework import filters
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
import requests
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
    # fields = ['title', 'anons', 'full_text', 'date']
    form_class = ArtiLesForm


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form


class NewsDeleteView(SuccessMessageMixin, DeleteView):
    model = ArtiLes
    template_name = 'news/news-delete.html'
    success_url = reverse_lazy('news_home.html')
    success_message = "Статья успешно удалена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_title'] = self.object.title
        return context

# def create(request):
#     if request.method == 'POST':
#         article_form = ArtiLesForm(request.POST)
#         category_form = CategoryForm(request.POST)
#
#         if category_form.is_valid():
#             new_category = category_form.save()
#         else:
#             new_category = None
#
#         if article_form.is_valid():
#             article = article_form.save(commit=False)
#
#             category_id = article.category_id
#             if category_id:
#                 if not Category.objects.filter(id=category_id).exists():
#                     return HttpResponse("Категория не существует.")
#
#             if new_category:
#                 article.category = new_category
#
#             article.save()
#             return redirect('/news/')
#         else:
#             error = 'Форма статьи неверная'
#     else:
#         article_form = ArtiLesForm()
#         category_form = CategoryForm()
#
#     data = {
#         'article_form': article_form,
#         'category_form': category_form
#     }
#     return render(request, 'news/create.html', data)


def create(request):
    if request.method == 'POST':
        article_form = ArtiLesForm(request.POST)
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            new_category = category_form.save()
        else:
            new_category = None

        if article_form.is_valid():
            article = article_form.save(commit=False)
            category_id = article.category_id

            if category_id:
                if not Category.objects.filter(id=category_id).exists():
                    return HttpResponse("Категория не существует.")

            if new_category:
                article.category = new_category

            article.save()
            return redirect('/news/')
        else:
            error = 'Форма статьи неверная'
            data = {
                'article_form': article_form,
                'category_form': category_form,
                'error': error,
            }
            return render(request, 'news/create.html', data)
    else:
        article_form = ArtiLesForm()
        category_form = CategoryForm()

    data = {
        'article_form': article_form,
        'category_form': category_form,
    }
    return render(request, 'news/create.html', data)



def search(request):
    query = request.GET.get('q', '')
    if query:
        products = ArtiLes.objects.filter(
            Q(title__icontains=query) | Q(full_text__icontains=query)
        )
    else:
        products = []

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'news/search.html', context)


def add_comment(request, article_id):
    article = get_object_or_404(ArtiLes, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect(article.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'news/details_view.html', {'form': form, 'article': article})


# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('/news/')
#             if request.GET.get('_popup') == '1':
#                 return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window);</script>')
#             else:
#                 return redirect('category_list')
#     else:
#         form = CategoryForm()
#     data = {
#         'form': form,
#
#     }
#     return render(request, 'news/create.html', data)

def article_detail(request, id):
    article = get_object_or_404(ArtiLes, id=id)
    return render(request, 'news/article_detail.html', {'article': article})

def news_list(request):
    news = ArtiLes.objects.all()
    categories = Category.objects.all()
    return render(request, 'news/news_list.html', {'news': news, 'categories': categories})

def news_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    news = ArtiLes.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'news/news_list.html', {'categories': categories})

def edit(request, article_id):
    article = get_object_or_404(ArtiLes, id=article_id)

    if request.method == 'POST':
        article_form = ArtiLesForm(request.POST, instance=article)
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            new_category = category_form.save()
            article.category = new_category
        else:
            new_category = None

        if article_form.is_valid():
            article = article_form.save(commit=False)

            if not Category.objects.filter(id=article.category_id).exists():
                return HttpResponse("Категория не существует.")

            if new_category:
                article.category = new_category

            article.save()
            return redirect(article.get_absolute_url())
        else:
            error = 'Форма статьи неверная'
            data = {
                'article_form': article_form,
                'category_form': category_form,
                'error': error,
            }
            return render(request, 'news/edit.html', data)
    else:
        article_form = ArtiLesForm(instance=article)
        category_form = CategoryForm()

    data = {
        'article_form': article_form,
        'category_form': category_form,
        'article': article,
    }
    return render(request, 'news/edit.html', data)

import logging

logger = logging.getLogger(__name__)
def weather_and_currency_view(request):
    weather_api_key = 'e1b9079f105bdb7e3abaabfe82dcf8a8'
    weather_city = 'Almaty'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={weather_city}&appid={weather_api_key}&units=metric'

    try:
        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        weather_data = response_weather.json()
        logger.info(f"Weather API response: {weather_data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API error: {e}")
        weather_data = None

    currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        response_currency = requests.get(currency_url)
        response_currency.raise_for_status()
        currency_data = response_currency.json()
        logger.info(f"Currency API response: {currency_data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Currency API error: {e}")
        currency_data = None

    context = {
        'weather': weather_data,
        'currency': currency_data,
    }

    return render(request, 'news/weather-and-currency.html', context)