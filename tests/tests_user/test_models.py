from django.test import TestCase

from user.models import User
from django.contrib.auth import get_user_model


class UserModelsTest(TestCase):
    
    @classmethod
    def setUpTestData(self):
        get_user_model().objects.create_user('hm@hm.hm', '12345678', first_name = 'Hman')


    def changeFirstName(self):
        user = get_user_model().objects.get(email = 'hm@hm.hm')
        valid_name = get_user_model().objects.save_first_name(user, 'Hman1')
        invalid_name1 = get_user_model().objects.save_first_name(user, 'h')#1 character
        invalid_name2 = get_user_model().objects.save_first_name(user, 'qwertyuiopasdfghjklzxcvbnm')#26 characters
        self.assertEqual(valid_name.first_name, 'Hman1')
        self.assertFalse(invalid_name1.first_name == 'h')
        self.assertFalse(invalid_name2.first_name == 'qwertyuiopasdfghjklzxcvbnm')


    def changeLastName(self):
        user = get_user_model().objects.get(email = 'hm@hm.hm')
        valid_last_name = get_user_model().objects.save_last_name(user, 'Hman1')
        invalid_last_name1 = get_user_model().objects.save_last_name(user, 'h')#1 character
        invalid_last_name2 = get_user_model().objects.save_last_name(user, 'qwertyuiopasdfghjklzxcvbnm')#26 characters
        self.assertEqual(valid_last_name.last_name, 'Hman1')
        self.assertFalse(invalid_last_name1.last_name == 'h')
        self.assertFalse(invalid_last_name2.last_name == 'qwertyuiopasdfghjklzxcvbnm')

    def getFullName(self):
        user = get_user_model().objects.get(email = 'hm@hm.hm')
        self.assertEqual(user.full_name(), 'Hman1 Hman1')


    def emailRepeatRegistration(self):
        user1 = get_user_model().objects.create_user('hm@hm.hm', '12345678', first_name = 'Hman')
        user2 = get_user_model().objects.create_user('hm@hm.hm', '12345678', first_name = 'Hman')
        self.assertFalse(user1 == user2)

    def changeEmail(self):
        user = get_user_model().objects.get(email = 'hm@hm.hm')
        saved = get_user_model().objects.save_email(user, 'hm1@hm.hm')
        if saved['success'] == True:
            self.assertEqual(saved['obj'].email, 'hm1@hm.hm')
        return saved

    def deleteModel(self):
        user = get_user_model().objects.get(email = 'hm@hm.hm')
        user.objects.delete()
