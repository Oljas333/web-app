from .models import ArtiLes
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from .models import Comment, Category
from django import forms
class ArtiLesForm(ModelForm):
    class Meta:
        model = ArtiLes
        fields = ['title', 'anons', 'full_text', 'date']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс статьи'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации',
                'type': 'datetime-local'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст статьи'
            }),
            # "category": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Название категории'
            # }),

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }

class CategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(
    label='Категория',
    queryset=Category.objects.all(),
    empty_label="Выберите категорию",
    required=False,
    widget=forms.Select(attrs={
        'class': 'form-control',

        })
    )

    class Meta:
        model = Category
        fields = ['category', 'name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Новая категории'
            }),
        }
