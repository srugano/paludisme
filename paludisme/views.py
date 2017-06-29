from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from paludisme.utils import validate_date, split_message, validate_phone, get_or_none, send_sms_through_rapidpro
from stock.models import Report, Reporter, Product, Temporary
from stock.views import create_stockproduct, update_stockproduct
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import JsonResponse
from django.conf import settings as conf_settings
from bdiadmin.models import CDS


@csrf_exempt
def add_report(request):
    response_data = split_message(request)
    if Reporter.objects.filter(phone_number=response_data['phone']).count() == 0:
        return JsonResponse({'Ok': "False", 'info_to_contact': "Ntimwanditse. Banza mwiyandikishe."}, safe=False)
    if response_data['text']:
        facility = Reporter.objects.get(phone_number=response_data['phone']).facility
        if response_data['text'] != "":
            message = response_data['text'].split(" ")
            if message[0] not in [y[0] for x, y in enumerate(conf_settings.KNOWN_PREFIXES)]:
                return JsonResponse({'Ok': "False", 'info_to_contact': "Rapport mwarungitse ntibaho. Rungika iyitanguzwa na REG, SF, SR, RP, CA, TS, HBC, HBD canke X"}, safe=False)
            date_updated = validate_date(message[1])
            if isinstance(date_updated, JsonResponse):
                return JsonResponse({'Ok': "False", 'info_to_contact': 'Itariki ntiyandikwa uko.', 'error': message[1]}, safe=False)
            if date_updated.date() > datetime.datetime.today().date():
                return JsonResponse({'Ok': "False", 'info_to_contact': 'Itariki ntishobora kuba muri kazoza. Subira urungike mesaje.', 'error': date_updated}, safe=False)
            if message[2] in ["ACT", "QUI", "ART", "TDR", "SP"] or message[0] in ["CA", "TS", "HBD", "HBC"]:
                product = get_or_none(Product, code=message[2])
                report, created = Report.objects.get_or_create(facility=facility, reporting_date=date_updated, category=message[0].upper(), text__icontains=message[2])
                if created:
                    report.text = response_data["text"]
                    report.save()
                    created = "Report created"
                    info_to_contact = create_stockproduct(product=product, report=report, phone=response_data['phone'])
                else:
                    report.text = response_data["text"]
                    report.save()
                    created = "Report updated"
                    info_to_contact = update_stockproduct(product=product, report=report, phone=response_data['phone'])
            return JsonResponse({'Ok': "True", 'info_to_contact': info_to_contact}, safe=False)


@csrf_exempt
def add_reporter(request):
    response_data = split_message(request)
    message = response_data['text'].split(" ")
    if message[0] == "REG":
        if not CDS.objects.filter(code=message[1]):
            return JsonResponse({'Ok': "False", 'info_to_contact': "Iryo vuriro ntiribaho."}, safe=False)
        if not (validate_phone(message[2]) and validate_phone(message[3])):
            return JsonResponse({'Ok': "False", 'info_to_contact': "Terefone ntizanditse neza."}, safe=False)
        present = get_or_none(Reporter, phone_number__icontains=message[2])
        if not present:
            temporary, created = Temporary.objects.get_or_create(facility=CDS.objects.get(code=message[1]), phone_number=validate_phone(message[2]), supervisor_phone_number=validate_phone(message[3]))
            if created:
                return JsonResponse({'Ok': "True", 'info_to_contact': "Subira wandike numero zawe n'izuwugutwara gusa."}, safe=False)
            else:
                return JsonResponse({'Ok': "True", 'info_to_contact': "Rungika gusa izo nimero za terefone."}, safe=False)
        else:
            cds = get_or_none(CDS, code=message[1])
            if not cds:
                return JsonResponse({'Ok': "False", 'info_to_contact': "Iryo vuriro ntiribaho."}, safe=False)
            else:
                present.facility = cds
            present.supervisor_phone_number = validate_phone(message[3])
            present.save()
            return JsonResponse({'Ok': "Ok", 'info_to_contact': "Muhejeje guhindura inimero {0} izohora itanga raporo kuri {1}.".format(present.phone_number, present.facility)}, safe=False)
    else:
        return JsonResponse({'Ok': "False", 'info_to_contact': "Ivyo mwanditse sivyo."}, safe=False)


@csrf_exempt
def confirm_reporter(request):
    response_data = split_message(request)
    message = response_data['text'].split(" ")
    temporary = get_or_none(Temporary, phone_number__icontains=validate_phone(message[0]), supervisor_phone_number__icontains=validate_phone(message[1]))
    if temporary:
        reporter, created = Reporter.objects.get_or_create(phone_number=temporary.phone_number, supervisor_phone_number=temporary.supervisor_phone_number)
        reporter.facility = temporary.facility
        reporter.save()
        temporary.delete()
        send_sms_through_rapidpro({'urns': ["tel:"+reporter.supervisor_phone_number, ], 'text': "Mwandikishijwe kuzoja muronka raporo za rupture kuri {0}".format(reporter.facility)})
        return JsonResponse({'Ok': "True", 'info_to_contact': "Murahejeje kwandikisha inimero {0} izohora itanga raporo.".format(reporter.phone_number)}, safe=False)
    else:
        return JsonResponse({'Ok': "False", 'info_to_contact': "Izo numero mwanditse ntizibaho"}, safe=False)


@csrf_exempt
def add_stockout(request):
    pass


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

