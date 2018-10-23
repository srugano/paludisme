from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger
import datetime
from stock.models import Report, Product
from stock.recorders import create_stockproduct, update_stockproduct
from stock.resources import CasesPaluResource, StockProductResource
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging
from django.contrib.auth.models import User

logger = get_task_logger(__name__)


@task(name="export_cases_palu")
def export_cases_palu(user_id=None):
    user = User.objects.get(id=user_id)
    dataset = CasesPaluResource().export().xlsx
    file_name = "Cases_palu_{0}.xlsx".format(datetime.datetime.now())
    f = open(settings.MEDIA_ROOT + "/" + file_name, "wb")
    f.write(dataset)
    f.close()
    try:
        d = {"username": user.username, "link": file_name}
        plaintext = render_to_string("stock/download_case_palu.txt", d)
        htmly = render_to_string("stock/download_case_palu.html", d)

        subject, from_email, to = (
            "Download all cases palu",
            settings.DEFAULT_FROM_EMAIL,
            user.email,
        )
        msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
        msg.attach_alternative(htmly, "text/html")
        msg.send()
    except:
        logging.warning(
            "Tried to send download files to user {0} but it failed. ".format(user)
        )


@task(name="export_stock_product")
def export_stock_product(user_id=None):
    user = User.objects.get(id=user_id)
    dataset = StockProductResource().export().xlsx
    file_name = "Stock_product_{0}.xlsx".format(datetime.datetime.now())
    f = open(settings.MEDIA_ROOT + "/" + file_name, "wb")
    f.write(dataset)
    f.close()
    try:
        d = {"username": user.username, "link": file_name}
        plaintext = render_to_string("stock/download_case_palu.txt", d)
        htmly = render_to_string("stock/download_case_palu.html", d)

        subject, from_email, to = (
            "Download all cases palu",
            settings.DEFAULT_FROM_EMAIL,
            user.email,
        )
        msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
        msg.attach_alternative(htmly, "text/html")
        msg.send()
    except:
        logging.warning(
            "Tried to send download files to user {0} but it failed. ".format(user)
        )


@periodic_task(
    run_every=(crontab(minute="*/45")), name="update_cds_task", ignore_result=True
)
def update_cds_task():
    reports_created, reports_updated = 0, 0
    for r in Report.objects.filter(
        category="SF", reporting_date__year=datetime.datetime.today().year
    ):
        product = Product.objects.get(code=r.text.split(" ")[2])
        dt = r.reporting_date + datetime.timedelta(weeks=1)
        start = dt - datetime.timedelta(days=dt.weekday())
        report, created = Report.objects.get_or_create(
            reporting_date=start, category="SD", facility=r.facility
        )
        report.text = r.text.replace("SF", "SD", 1)
        report.save()
        if created:
            create_stockproduct(report=report, product=product)
            reports_created += 1
        else:
            update_stockproduct(report=report, product=product)
            reports_updated += 1
    logger.info(
        "Finished updating reports with {0} reports created and  {1} reports updated".format(
            reports_created, reports_updated
        )
    )
