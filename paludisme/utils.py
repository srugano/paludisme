import datetime
import urllib
from django.http import JsonResponse
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import re


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=
    _("Phone number in the format: '+25799999999'. Up to 15 digits allowed."))


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


def split_message(request):
    response_data = {}
    liste_data = request.body.split("&")
    for i in liste_data:
        response_data[i.split("=")[0]] = urllib.unquote_plus(i.split("=")[1]).upper()

    return response_data


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

