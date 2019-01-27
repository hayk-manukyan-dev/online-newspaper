from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django.core.validators import EmailValidator

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from configuration.transfers import readJson

models_config = readJson('configuration/json/models.json')

class UserManager(BaseUserManager):
    use_in_migrations = True

    def email_not_exist(self, email):
        try:
            User.objects.get(email = email)
            return False
        except:
            return True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if self.email_not_exist(email):
            return self._create_user(email, password, **extra_fields)
        raise ValueError('Email is not available')

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def find_email(self, email):
        try:
            user = User.objects.get(email = email)
            return user
        except:
            return False

    def valid_email(self, email):
        if self.find_email(email):
            return False
#        from blacklist.models import BlackListManager
#        if BlackListManager().email_exist_in_blacklist(email) != True:
            email_validator = str#EmailValidator()
        try:
            email_validator(email)
            return True
        except:
            return False

    def save_email(self, user, email):
        if self.valid_email(email):
            user.email = email
            user.email_confirmed = False
            user.save()
            return {'success' : True, 'obj' : user}
        return {'success' : False, 'message' : 'email_validation_failure'}

    def save_first_name(self, user, first_name):
        if len(first_name) >= 2 and len(first_name) <= 25:
            try:
                user.first_name = first_name
                user.save()
                return {'success' : True}
            except:
                Warning('<(UserManager > save_first_name) first_name is not saved')
        return {'success' : False, 'message' : 'length_error'}

    def save_last_name(self, user, last_name):
        if len(last_name) >= 2 and len(last_name) <= 25:
            try:
                user.last_name = last_name
                user.save()
                return {'success' : True}
            except:
                Warning('(UserManager > save_first_name) first_name is not saved')
        return {'success' : False, 'message' : 'length_error'}

    def remove_image(self, user):
        user.avatar.delete(save=False)
        user.avatar.delete()
        user.avatar = User._meta.get_field('avatar').get_default()
        user.save()
        return user

    def save_image(self, user, image):
        if user.avatar == User._meta.get_field('avatar').get_default():
            user.avatar = image
        else:
            self.remove_image(user)
            user.avatar = image
        user.save()
        return user



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default = models_config["User"]["email_confirmed"]["default"])
    avatar = models.ImageField(upload_to = 'avatars', default = 'images/avatars/static/avatar.jpg')
    avatar_thumbnail = ImageSpecField(source = 'avatar',
                                      processors = [ResizeToFill(models_config["User"]["avatar_thumbnail"]["processors"]["ResizeToFill"][0], models_config["User"]["avatar_thumbnail"]["processors"]["ResizeToFill"][1])],
                                      format = models_config["User"]["avatar_thumbnail"]["format"],
                                      options = models_config["User"]["avatar_thumbnail"]["options"])


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'avatar':
                field.upload_to = 'images/avatars/' + str(self.email)
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):#not work in admin
        self.avatar.delete(save = False)
        self.avatar.delete()
        super(UserManager, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.email)
