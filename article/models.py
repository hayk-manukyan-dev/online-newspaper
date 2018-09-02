from django.db import models
from online_newspaper.settings import languages_dict

from initialarticle.models import InitialArticle

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from datetime import datetime

class ArticleManager(models.Manager):

    def language_exist(self, keywords, language):
        articles = Article.objects.filter(initial__keywords = keywords, language = language)
        if articles:
            return True
        return False

    def create_article(self, initial, language, title, description, text, main_image):
        if self.language_exist(initial.keywords, language) == False:
            article = Article(initial = initial, language = language, title = title, description = description, text = text, main_image = main_image)
            article.save()
            return article
        return ValueError("article.models ArticleManager create_article >> Chosed language exist")

    def delete_main_image(self, article_pk):
        article = Article.objects.get(pk = article_pk)
        article.main_image.delete(save = False)
        article.main_image.delete()


    def edit_article(self, article_object, language, title, description, text, main_image):
        if language != article_object.language and self.language_exist(article_object.initial.keywords, language) != False:
            return ValueError('article.models ArticleManager edit_article >> Chosed language exist')
        article_object.language = language
        article_object.title = title
        article_object.description = description
        article_object.text = text
        self.delete_main_image(article_object.pk)
        article_object.main_image = main_image
        article_object.save()
        return article_object


    def get_article(self, keywords, **kwargs):
        return Article.objects.get(initial__keywords = keywords, **kwargs)


    def article_owner_is_requester(self, request, article):
        if article.initial.by == request.user:
            return True
        return False


class Article(models.Model):
    initial = models.ForeignKey(InitialArticle, on_delete=models.CASCADE)
    language = models.CharField(max_length = 3, null = True, blank = True)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    text = models.CharField(max_length = 1000)
    main_image = models.ImageField(upload_to='article', default='article.jpg')
    date_time = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'main_image':
                field.upload_to = 'article/' + str(datetime.now().date()) + '/' + str(self.initial.keywords)
        if self.language in languages_dict:
            return super(Article, self).save(*args, **kwargs)
        raise ValueError('articel.models Article save >> unregisterd language')


    objects = ArticleManager()


    def __str__(self):
        return self.title
