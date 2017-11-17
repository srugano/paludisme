from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger
import datetime
from stock.models import Report, Product
from stock.views import create_stockproduct, update_stockproduct
from stock.resources import CasesPaluResource, StockProductResource
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from quick_publisher.celery import app
logger = get_task_logger(__name__)


@task(bind=True, name="export_cases_palu")
def export_cases_palu(request):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=request.user.id)
        send_mail(
            'Export for cases palu are ready',
            'Follow this to download your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logger.warning("Tried to send download email to non-existing user '%s'" % request.user)


@periodic_task(run_every=(crontab(minute='*/45')), name="update_cds_task", ignore_result=True)
def update_cds_task():
    reports_created, reports_updated = 0, 0
    for r in Report.objects.filter(category='SF', reporting_date__year=datetime.datetime.today().year):
        product = Product.objects.get(code=r.text.split(' ')[2])
        dt = r.reporting_date + datetime.timedelta(weeks=1)
        start = dt - datetime.timedelta(days=dt.weekday())
        report, created = Report.objects.get_or_create(reporting_date=start, category='SD', facility=r.facility)
        report.text = r.text.replace('SF', 'SD', 1)
        report.save()
        if created:
            create_stockproduct(report=report, product=product)
            reports_created += 1
        else:
            update_stockproduct(report=report, product=product)
            reports_updated += 1
    logger.info("Finished updating reports with {0} reports created and  {1} reports updated".format(reports_created, reports_updated))




