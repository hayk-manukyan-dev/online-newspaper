from django import forms
from django.utils.translation import gettext as _

from articlecategory.models import ArticleCategory, ArticleCategoryManager


class ArticleCategoryModelForm(forms.ModelForm):
    name = forms.CharField(label = _('Name'), widget = forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : _('Name')}))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs = {'class' : 'form-control', 'rows' : '3', 'placeholder' : _('Description')}))


    class Meta:
        model = ArticleCategory
        fields = ['name', 'description']
