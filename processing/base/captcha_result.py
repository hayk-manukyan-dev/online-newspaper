import urllib
import json
from online_newspaper.settings import GOOGLE_RECAPTCHA_SECRET_KEY

def captchaResult(recaptcha_response):
    recaptcha_response = recaptcha_response
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {'secret': GOOGLE_RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode())