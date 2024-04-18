from django import forms
from .models import Comment, News, File


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'photo']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']


FileFormSet = forms.inlineformset_factory(News, File, form=FileForm, extra=1, can_delete=True)
