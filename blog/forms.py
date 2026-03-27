from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    publish = forms.BooleanField(
        required=False,
        label='Publicar articulo',
        help_text='Marcar para publicar inmediatamente (requiere permiso)'
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'publish']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }
