from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce, Extract
from bdiadmin.models import CDS, District, Province
from stock.models import CasesPalu, CasesPaluCDS, CasesPaluDis, CasesPaluProv, Tests, StockProduct, StockProductProv, StockProductDis, StockProductCDS
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/15')), name="update_province_task", ignore_result=True)
def update_province_task():
    for p in Province.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility__district__province=p, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).exists():
                raba = CasesPalu.objects.filter(report__facility__district__province=p, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluProv.objects.update_or_create(province=p, week='W{0}'.format(r), year=datetime.datetime.today().year)
                obj.simple, obj.acute, obj.pregnant_women, obj.decease, obj.week_number = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases'], r
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility__district__province=p, reporting_date__year=datetime.datetime.today().year).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility__district__province=p, reporting_date__year=datetime.datetime.today().year).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()
            if StockProduct.objects.filter(report__facility__district__province=p, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year, report__category='SF').exists():
                raba = StockProduct.objects.filter(report__facility__district__province=p, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year, report__category='SF').annotate(year=Extract('reporting_date', 'year'), week=Extract('reporting_date', 'week')).values('year', 'week', 'product__designation', 'dosage__dosage').annotate(quantities=Sum('quantity'))
                for i in raba:
                    obj, created = StockProductProv.objects.update_or_create(province=p, week='W{0}'.format(r), year=datetime.datetime.today().year, product='{0}-{1}'.format(i['product__designation'], i['dosage__dosage']))
                    obj.quantity_sf, obj.week_number = i['quantities'], r
                    obj.quantity_sr = StockProduct.objects.filter(report__facility__district__province=p, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year, report__category='SR', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.quantity_sd = StockProduct.objects.filter(report__facility__district__province=p, reporting_date__week=r-1, reporting_date__year=datetime.datetime.today().year, report__category='SF', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.save()

    logger.info("Finished updating Provinces")


@periodic_task(run_every=(crontab(minute='*/30')), name="update_district_task", ignore_result=True)
def update_district_task():
    for d in District.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility__district=d, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).exists():
                raba = CasesPalu.objects.filter(report__facility__district=d, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluDis.objects.update_or_create(district=d, week='W{0}'.format(r), year=datetime.datetime.today().year)
                obj.simple, obj.acute, obj.pregnant_women, obj.decease, obj.week_number = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases'], r
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility__district=d, reporting_date__year=datetime.datetime.today().year).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility__district=d, reporting_date__year=datetime.datetime.today().year).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()
            if StockProduct.objects.filter(report__facility__district=d, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).exists():
                raba = StockProduct.objects.filter(report__facility__district=d, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).annotate(year=Extract('reporting_date', 'year'), week=Extract('reporting_date', 'week')).values('year', 'week', 'product__designation', 'dosage__dosage').annotate(quantities=Sum('quantity'))
                for i in raba:
                    obj, created = StockProductDis.objects.update_or_create(district=d, week='W{0}'.format(r), year=datetime.datetime.today().year, product='{0}-{1}'.format(i['product__designation'], i['dosage__dosage']))
                    obj.quantity_sf, obj.week_number = i['quantities'], r
                    obj.quantity_sr = StockProduct.objects.filter(report__facility__district=d, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year, report__category='SR', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.quantity_sd = StockProduct.objects.filter(report__facility__district=d, reporting_date__week=r-1, reporting_date__year=datetime.datetime.today().year, report__category='SF', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.save()
    logger.info("Finished updating Districts")


@periodic_task(run_every=(crontab(minute='*/59')), name="update_cds_task", ignore_result=True)
def update_cds_task():
    for c in CDS.objects.all():
        for r in range(1, datetime.datetime.today().isocalendar()[1]+1):
            if CasesPalu.objects.filter(report__facility=c, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).exists():
                raba = CasesPalu.objects.filter(report__facility=c, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).aggregate(simples=Sum('simple', filter=Q(simple__is_null=False)), acutes=Sum('acute', filter=Q(acute__is_null=False)), pregnant_womens=Sum('pregnant_women', filter=Q(pregnant_women__is_null=False)), deceases=Sum('decease', filter=Q(decease__is_null=False)))
                obj, created = CasesPaluCDS.objects.update_or_create(cds=c, week='W{0}'.format(r), year=datetime.datetime.today().year)
                obj.simple, obj.acute, obj.pregnant_women, obj.decease, obj.week_number = raba['simples'], raba['acutes'], raba['pregnant_womens'], raba['deceases'], r
                obj.ge = Tests.objects.filter(reporting_date__week=r, report__facility=c, reporting_date__year=datetime.datetime.today().year).aggregate(ges=Coalesce(Sum('ge'), 0))['ges']
                obj.tdr = Tests.objects.filter(reporting_date__week=r, report__facility=c, reporting_date__year=datetime.datetime.today().year).aggregate(tdrs=Coalesce(Sum('tdr'), 0))['tdrs']
                obj.save()
            if StockProduct.objects.filter(report__facility=c, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).exists():
                raba = StockProduct.objects.filter(report__facility=c, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year).annotate(year=Extract('reporting_date', 'year'), week=Extract('reporting_date', 'week')).values('year', 'week', 'product__designation', 'dosage__dosage').annotate(quantities=Sum('quantity'))
                for i in raba:
                    obj, created = StockProductCDS.objects.update_or_create(cds=c, week='W{0}'.format(r), year=datetime.datetime.today().year, product='{0}-{1}'.format(i['product__designation'], i['dosage__dosage']))
                    obj.quantity_sf, obj.week_number = i['quantities'], r
                    obj.quantity_sr = StockProduct.objects.filter(report__facility=c, reporting_date__week=r, reporting_date__year=datetime.datetime.today().year, report__category='SR', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.quantity_sd = StockProduct.objects.filter(report__facility=c, reporting_date__week=r-1, reporting_date__year=datetime.datetime.today().year, report__category='SF', product__designation=i['product__designation'], dosage__dosage=i['dosage__dosage']).aggregate(quantities=Coalesce(Sum('quantity'), 0))['quantities']
                    obj.save()

    logger.info("Finished updating Cds")
