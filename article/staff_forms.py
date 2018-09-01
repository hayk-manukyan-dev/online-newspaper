from django import forms
from django.utils.translation import gettext as _

from django_summernote.widgets import SummernoteWidget
from article.models import Article
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill



class ArticleCreateForm(forms.Form):
    title = forms.CharField(label = _('Title'), widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : _('Title')}))
    description = forms.CharField(label = _('Description'), widget = forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : _('Description')}))
    text = forms.CharField(label = _('Article'), widget = SummernoteWidget(attrs={'class' : 'form-control', 'placeholder' : _('Article')}))
    main_image = ProcessedImageField(spec_id='article:Article:main_image', processors=[ResizeToFill(1600, 1200)], format='JPEG', options={'quality': 99})

    def save_(self, initial_article, language):
        return Article.objects.create_article(initial = initial_article, language = language, title = self.cleaned_data['title'], description = self.cleaned_data['description'], text = self.cleaned_data['text'], main_image = self.cleaned_data['main_image'])



class ArticleEditForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : _('Title')}))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : _('Description')}))
    text = forms.CharField(label=_('article text'), widget=SummernoteWidget(attrs={'class' : 'form-control', 'placeholder' : _('Article')}))
    main_image = ProcessedImageField(spec_id='article:Article:main_image', processors=[ResizeToFill(1600, 1200)], format='JPEG', options={'quality': 99})

    class Meta:
        model = Article
        fields = ['title', 'description', 'text', 'main_image']

    def edit(self, article_object, commit = True):
        edit_responce = Article.objects.edit_article(article_object = article_object, language = article_object.language, title = self.cleaned_data['title'], description = self.cleaned_data['description'], text = self.cleaned_data['text'], main_image = self.cleaned_data['main_image'])
        return edit_responce