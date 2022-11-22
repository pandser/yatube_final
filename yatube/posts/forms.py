from django import forms

from .models import Post, Comment
from .constants import MIN_LENGTH_POST


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < MIN_LENGTH_POST:
            raise forms.ValidationError('Давайте напишем пост подлиннее :(')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < MIN_LENGTH_POST:
            raise forms.ValidationError(
                'Давайте напишем коментарий подлиннее :('
            )
        return data
