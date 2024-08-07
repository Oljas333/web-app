from django.db import models

class Category(models.Model):
    name = models.CharField('Новая категория', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
class ArtiLes(models.Model):
    title = models.CharField('Название', max_length=50, default='Badmonkey#1')
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    article = models.ForeignKey(ArtiLes, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=100)
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author} на {self.article.title}'

    class Meta:
        ordering = ['created_at']



