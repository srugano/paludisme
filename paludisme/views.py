from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from paludisme.utils import validate_date, split_message
from stock.models import Report, Reporter, Product
from stock.views import create_stockproduct
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import JsonResponse
from django.conf import settings as conf_settings


@csrf_exempt
def add_report(request):
    response_data = split_message(request)
    if Reporter.objects.filter(phone_number=response_data['phone']).count() == 0:
        return JsonResponse({'Ok': "False", 'info_to_contact': "Ntimwanditse. Banza mwiyandikishe."}, safe=False)
    if response_data['text']:
        facility = Reporter.objects.get(phone_number=response_data['phone']).facility
        if response_data['text'] != "":
            # import ipdb; ipdb.set_trace()
            message = response_data['text'].split(" ")
            if message[0].upper() not in [y[0] for x, y in enumerate(conf_settings.KNOWN_PREFIXES)]:
                return JsonResponse({'Ok': "False", 'info_to_contact': "Rapport mwarungitse ntibaho. Rungika iyitanguzwa na SF, SR, REG canke RUP"}, safe=False)
            if len(message) > 7:
                return JsonResponse({'Ok': "False", 'info_to_contact': "Mwarungitse ibintu vyinshi. Subiramwo nkuko twabigishije."}, safe=False)
            date_updated = validate_date(message[1])
            if isinstance(date_updated, JsonResponse):
                return JsonResponse({'Ok': "False", 'info_to_contact': 'Itariki ntiyandikwa uko.', 'error': message[1]}, safe=False)
            if date_updated.date() > datetime.datetime.today().date():
                return JsonResponse({'Ok': "False", 'info_to_contact': 'Itariki ntishobora kuba muri kazoza. Subira urungike mesaje.', 'error': date_updated}, safe=False)
            report, created = Report.objects.get_or_create(facility=facility, reporting_date=date_updated, category=message[0].upper(), text__icontains=message[2])
            if created:
                report.text = response_data["text"]
                report.save()
                created = "Report created"
                product = Product.objects.get(code=message[2])
                create_stockproduct(product=product, report=report)
            else:
                report.text = response_data["text"]
                report.save()
                created = "Report updated"
            return JsonResponse({"facility": facility.name, "date_updated": date_updated, "message": message[0].upper(), "report": created}, safe=False)


def home(request):
    return render(request, 'home.html')


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

