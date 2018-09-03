from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from django.conf.urls.static import static
from online_newspaper.settings import MEDIA_URL, MEDIA_ROOT

from translate.views import changeLanguage

from user.views import SignUp, LogIn, LogOut, EditUser, editEmail, editFirstName, editLastName, UserAvatarRemove, UserAvatarEdit, editAvatar
from user.manage_users_views import GetUsers, AddUserInGroup, RemoveUserFromGroup
from blacklist.views import EmailIsInBlackList
from articlecategory.views import CreateArticleCategory, EditArticleCategory, removeArticleCategory, GetArticleCategories, getArticleCategories
from group.views import addUserToGroup, removeUserFromGroup

from initialarticle.views import CreateInitialArticle, EditInitialArticle, RequesterInitialarticles, removeInitialArticle
from article.staff_views import  CreateArticle, EditArticle, removeArticle
from article.views import GetArticleByKeywords, GetArticlesByCategory, GetMixedArticles

from processing.views.main_view import EnteryLanguageDetect



urlpatterns = [
    path('online-newspaper/admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('translate/<str:language>', changeLanguage),

    path(r'summernote/', include('django_summernote.urls')),

    path('', EnteryLanguageDetect.as_view()),

    path('user/signup', SignUp.as_view()),
    path('user/login', LogIn.as_view()),
    path('user/logout', LogOut.as_view()),
    path('user/edit', EditUser.as_view()),
    path('user/avataredit', UserAvatarEdit.as_view()),
    path('user/avatarremove', UserAvatarRemove.as_view()),

    path('admin/getusers', GetUsers.as_view()),
    path('admin/add/useringroup/<int:user_pk>/<str:group>', AddUserInGroup.as_view()),
    path('admin/remove/userfromgroup/<int:user_pk>/<str:group>', RemoveUserFromGroup.as_view()),

    path('group/adduser/<str:user_pk>/<str:group_pk>/', addUserToGroup),
    path('group/removeuser/<str:user_pk>/<str:group_pk>/', removeUserFromGroup),

    path('blacklist/emailisinblacklist', EmailIsInBlackList.as_view()),

    path('articlecategory/create', CreateArticleCategory.as_view(), name = 'articlecategory_create'),
    path('articlecategory/edit/<article_category_pk>', EditArticleCategory.as_view()),
    path('articlecategory/remove/<str:article_category_pk>', removeArticleCategory),
    path('articlecategory/getall', GetArticleCategories.as_view()),

    path('initialarticle/create', CreateInitialArticle.as_view()),
    path('initialarticle/edit/<str:keywords>', EditInitialArticle.as_view()),
    path('initialarticle/remove/<str:keywords>', removeInitialArticle),
    path('initialarticle/userarticles', RequesterInitialarticles.as_view()),

    path('article/stuff/create/<str:language>/<str:keywords>', CreateArticle.as_view(), name = 'article_create'),
    path('article/stuff/edit/<str:language>/<str:keywords>', EditArticle.as_view()),
    path('article/stuff/remove/<str:language>/<str:keywords>', removeArticle),
    path('article/get/<str:language>/<str:keywords>', GetArticleByKeywords.as_view(), name = 'article_get'),

    path('article/category/<str:language>/<int:category_pk>/<int:page>', GetArticlesByCategory.as_view()),
    path('<str:language>', GetMixedArticles.as_view()),

    path('static/documentation', TemplateView.as_view(template_name = 'documentation.html')),
    path('static/source_code', TemplateView.as_view(template_name = 'source_code.html')),
]


#json
urlpatterns += [
    path('json/articlecategory/getall', getArticleCategories),
]

#ajax
urlpatterns += [
    path('ajax/user/editemail', editEmail),
    path('ajax/user/editfirstname', editFirstName),
    path('ajax/user/editlastname', editLastName),
    path('ajax/user/editavatar', editAvatar),

]


urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)
