import re, validators
from processing.base.message_manager import MessageManager

class TypedValidation(MessageManager):
    def post(self):
        try:
            message = super(TypedValidation, self).post()
            return message
        except:
            return self.message

    def passwordValid(self, password, simple = True, password_min_length = 6):
        if re.split(' ', password) != '':
            if simple != True:
                if re.match("^[a-zA-Z0-9_]*$", password) is None:
                    self.message = 'password_characters_not_valid'
                    return self.post()
            if len(password) < password_min_length:
                self.message = 'password_not_much_length'
                return self.post()
            self.message = 'True'
            return self.post()
        self.message = 'password_required'
        return self.post()

    def emailValid(self, email, simple = True):
        if re.split(' ', email)[0]  != '':
            if simple != True:
                if validators.email(email):
                    self.message = "True"
                    return self.post()
                self.message = 'email_not_valid'
            return self.post()
        self.message = "True"
        return self.post()

    def stringValid(self, string, min_length = 2):
        if re.split(' ', string) != '':
            if len(string) >= min_length:
                self.message = "True"
                return self.post()
            self.message = 'str_min_length_error'
            return self.post()
        self.message = 'str_required'
        return self.post()
