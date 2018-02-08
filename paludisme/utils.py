import datetime
from django.http import JsonResponse
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import re
import requests
from django.conf import settings
import json

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number in the format: '+25799999999'. Up to 15 digits allowed."))


def validate_phone(phone=None):
    if not re.match(r'\+257', phone):
        phone = '+257' + phone
    expression = r'^(\+?(257)?)((61)|(62)|(68)|(69)|(71)|(72)|(75)|(76)|(79))([0-9]{6})$'
    if re.search(expression, phone):
        return phone
    else:
        return False


def validate_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%d%m%y')
    except ValueError:
        return JsonResponse({"error": "Date est incorecte. Le format est jjmmaa."}, safe=False)
    else:
        return date


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def split_message(request):
    # Let's put all the incoming data in the dictionary 'incoming_data'
    incoming_data = byteify(json.loads(request.body))
    incoming_data['phone'] = incoming_data['contact']['urn'].replace("tel:", "")
    incoming_data['text'] = incoming_data['results']['rapport1']['input']
    return incoming_data


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def send_sms_through_rapidpro(args):
    ''' This function sends messages through rapidpro. Contact(s) and the message to send to them must be in args['data'] '''
    url = 'https://api.rapidpro.io/api/v2/broadcasts.json'
    token = getattr(settings, 'TOKEN', '')

    response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data=json.dumps(args))
    print response
