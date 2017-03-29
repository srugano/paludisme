import datetime
import urllib
from django.http import JsonResponse


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

