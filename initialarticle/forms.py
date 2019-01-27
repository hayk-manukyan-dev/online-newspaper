from django import forms
from django.utils.translation import gettext as _

from initialarticle.models import InitialArticle
from articlecategory.models import ArticleCategoryManager



class InitialArticleCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(InitialArticleCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(ArticleCategoryManager().get_article_categories(request), widget =forms.Select(attrs = {'class' : 'form-control'}))

    keywords = forms.CharField(label= _('Keywords'), max_length = 105, widget = forms.TextInput(attrs = {'class' : 'form-control'}))

    def save(self, user):
        return InitialArticle.objects.create_initial_article(by = user, category = self.cleaned_data['category'], keywords = self.cleaned_data['keywords'])


class InitialArticleEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(InitialArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(ArticleCategoryManager().get_article_categories(request), widget=forms.Select(attrs = {'class' : 'form-control'}))
        self.fields['keywords'] = forms.CharField(label= _('Keywords'), max_length = 105, widget = forms.TextInput(attrs = {'class' : 'form-control'}))


    class Meta:
        model = InitialArticle
        fields = ['category', 'keywords']

    def save_(self, user, article_keywords_object, commit = True):
        return InitialArticle.objects.edit_initial_article(article_keywords_object = article_keywords_object, by = user, category = self.cleaned_data['category'], keywords = self.cleaned_data['keywords'])
