from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to='news_photos', blank=True, null=True)
    SCIENCES = (
        ('Фізика', 'Фізика'),
        ('Хімія', 'Хімія'),
        ('Математика', 'Математика'),
    )
    category = models.CharField(max_length=20, choices=SCIENCES, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class File(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='news_file')

    def __str__(self):
        return f'{self.news.title} - {self.file.name}'


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коментарій від {self.author} на новину {self.news.title}'

    def is_author(self):
        return self.author == 2
