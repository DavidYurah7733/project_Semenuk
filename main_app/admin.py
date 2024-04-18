from django.contrib import admin

from main_app.models import News, Comment, File

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(File)
