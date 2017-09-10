from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from bdiadmin.models import CDS, District, Province
from stock.models import CasesPalu, CasesPaluCDS, CasesPaluDis, CasesPaluProv, Tests
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/15')), name="update_province_task", ignore_result=True)
def update_province_task():
    for p in Province.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility__district__province=p, reporting_date__week=r).exists():
                raba = CasesPalu.objects.filter(report__facility__district__province=p, reporting_date__week=r).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluProv.objects.update_or_create(province=p, week='W{0}'.format(r))
                obj.simple, obj.acute, obj.pregnant_women, obj.decease = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases']
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility__district__province=p).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility__district__province=p).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()

    logger.info("Finished updating Provinces")


@periodic_task(run_every=(crontab(minute='*/30')), name="update_district_task", ignore_result=True)
def update_district_task():
    for d in District.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility__district=d, reporting_date__week=r).exists():
                raba = CasesPalu.objects.filter(report__facility__district=d, reporting_date__week=r).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluDis.objects.update_or_create(province=d, week='W{0}'.format(r))
                obj.simple, obj.acute, obj.pregnant_women, obj.decease = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases']
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility__district=d).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility__district=d).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()

    logger.info("Finished updating Districts")


@periodic_task(run_every=(crontab(minute='*/59')), name="update_cds_task", ignore_result=True)
def update_cds_task():
    for c in CDS.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility=c, reporting_date__week=r).exists():
                raba = CasesPalu.objects.filter(report__facility=c, reporting_date__week=r).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluCDS.objects.update_or_create(province=c, week='W{0}'.format(r))
                obj.simple, obj.acute, obj.pregnant_women, obj.decease = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases']
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility=c).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility=c).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()

    logger.info("Finished updating Cds")
