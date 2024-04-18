from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from main_app.models import News, Comment, File
from main_app.forms import CommentForm, NewsForm, FileFormSet


def index(request):
    categories = News.objects.values_list('category', flat=True).distinct()
    context = {'categories': categories}
    return render(request, 'index.html', context)


def news_by_category(request, category):
    news_in_category = News.objects.filter(category=category)

    context = {'news_in_category': news_in_category, 'category': category}

    return render(request, 'news_by_category.html', context)


def news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments = news.comments.all()
    files = news.files.all()
    photo = news.photo

    context = {
        'news': news,
        'comments': comments,
        'files': files,
        'photo': photo,
    }

    return render(request, 'news_detail.html', context)


def add_comment(request, news_id):
    news = News.objects.get(pk=news_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.author = request.user
            comment.save()
            return redirect('news_detail', news_id=news_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('news_detail', news_id=comment.news.id)


def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            if request.user.groups.filter(name=news.category).exists():
                news.author = request.user
                news.save()
                files = request.FILES.getlist('files')
                for f in files:
                    file_instance = File(news=news, file=f)
                    file_instance.save()
                return redirect('news_detail', news_id=news.id)
            else:
                messages.error(request, "У вас немає дозволу на додавання новини до цієї категорії.")
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})


def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    # Проверяем, имеет ли пользователь право на редактирование новости
    if request.user == news.author:
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES, instance=news)
            formset = FileFormSet(request.POST, request.FILES, instance=news)

            if form.is_valid() and formset.is_valid():
                # Сохраняем отредактированную новость
                edited_news = form.save(commit=False)
                edited_news.author = request.user
                edited_news.save()

                # Сохраняем изменения в файлах
                formset.save()

                messages.success(request, 'Статтю успішно відредаговано.')
                return redirect('news_detail', news_id=news.id)
        else:
            form = NewsForm(instance=news)
            formset = FileFormSet(instance=news)

        return render(request, 'edit_news.html', {'form': form, 'formset': formset})
    else:
        messages.error(request, 'Ви не маєте дозволу на редагування цієї статті.')
        return redirect('news_detail', news_id=news.id)


# def edit_news(request, news_id):
#     news = get_object_or_404(News, id=news_id)
#     if request.user == news.author:
#         if request.method == 'POST':
#             form = NewsForm(request.POST, instance=news)
#             formset = FileFormSet(request.POST, request.FILES, instance=news)
#
#             if form.is_valid() and formset.is_valid():
#                 if request.user.groups.filter(name=news.category).exists():
#                     form.save()
#                     formset.save()
#                     messages.success(request, 'Статтю успішно відредаговано.')
#                     return redirect('news_detail', news_id=news.id)
#                 else:
#                     messages.error(request, "У вас немає дозволу на додавання новини до цієї категорії.")
#         else:
#             form = NewsForm(instance=news)
#             formset = FileFormSet(instance=news)
#         return render(request, 'edit_news.html', {'form': form, 'formset': formset})
#     else:
#         messages.error(request, 'Ви не маєте дозволу на редагування цієї статті.')
#         return redirect('news_detail', news_id=news.id)


def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if news.author == request.user:
        news.delete()
    return redirect('index', )


def user_news(request, user_id):
    user_news = News.objects.filter(author=user_id)
    context = {'user_news': user_news}
    return render(request, 'user_news.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
