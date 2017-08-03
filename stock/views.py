from stock.models import StockProduct, Product, StockOutReport, CasesPalu, Tests, PotentialCases, PotentialDeceased, Reporter, Report
from rest_framework import viewsets
import django_filters
from django.db.models.functions import Extract
from django.db.models import Sum, Count
from stock.serializers import StockProductSerializer, StockOutProductSerializer, ProductSerializer, CasesPaluSerializer, RateSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import re
from django.conf import settings
from paludisme.utils import send_sms_through_rapidpro
from bdiadmin.models import CDS


GROUPS = getattr(settings, 'RUPTURE_GROUPS', '')


class StockProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(name="report", lookup_expr='category')

    class Meta:
        model = StockProduct
        fields = ['dosage', 'product', 'report', 'category']


class StockProductViewsets(viewsets.ModelViewSet):
    queryset = StockProduct.objects.filter(report__category='SF')
    serializer_class = StockProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('report__facility__district__province', 'report__facility__district', 'report__facility')

    def get_queryset(self):
        list_of_ids = []
        for i in CDS.objects.all():
            raba = Report.objects.filter(category='SF', facility=i)
            if raba:
                list_of_ids.append(raba.latest('reporting_date').id)
        return self.queryset.filter(report__id__in=list_of_ids)


class StockOutProductViewsets(viewsets.ModelViewSet):
    queryset = StockOutReport.objects.all()
    serializer_class = StockOutProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('report__facility__district__province', 'report__facility__district', 'report__facility')


class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('code', 'id')


class CasesPaluViewsets(viewsets.ModelViewSet):
    queryset = CasesPalu.objects.annotate(year=Extract('reporting_date', 'year'), week=Extract('reporting_date', 'week')).values('year', 'week').annotate(simple=Sum('simple')).annotate(acute=Sum('acute')).annotate(pregnant_women=Sum('pregnant_women')).annotate(decease=Sum('decease')).order_by('year', 'week')
    serializer_class = CasesPaluSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('report__facility__district__province', 'report__facility__district', 'report__facility')


class RateViewsets(viewsets.ModelViewSet):
    queryset = Report.objects.annotate(year=Extract('reporting_date', 'year'), week=Extract('reporting_date', 'week')).values('year', 'week').annotate(nombre=Count('pk'))
    serializer_class = RateSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('facility__district__province', 'facility__district', 'facility')

    def get_serializer_context(self):
        return {'nombre_cds': self.queryset.values('facility').distinct().count()}


@login_required
def show_reports_sf(request):
    return render(request, "stock/sf.html")


@login_required
def show_reports_sr(request):
    return render(request, "stock/sr.html")


@login_required
def show_reports_rp(request):
    return render(request, "stock/rp.html")


def create_stockproduct(report=None, product=None, *args, **kwargs):
    values = report.text.split(" ")[2:]
    if re.match(r'^(CA)\s+(\d{6})(\s+\d+){4}$', report.text, re.I):
        cp = CasesPalu.objects.create(report=report, simple=values[0], acute=values[1], pregnant_women=values[2], decease=values[3])
        cp.save()
        return "Kuri {0}, handitswe ko hari abagwayi ba malaria {1}, abaremvye {2}, abagore bibungeze bayigwaye {3}, abitavye Imana ni {4}. Murakoze".format(report.facility, cp.simple, cp.acute, cp.pregnant_women, cp.decease)
    if re.match(r'^(TS)\s+(\d{6})(\s+\d+){2}$', report.text, re.I):
        ts = Tests.objects.create(report=report, ge=values[0], tdr=values[1])
        ts.save()
        return "Kuri {0}, handitswe ko hakozwe ama test ge {1}, na TDR {2}. Murakoze".format(report.facility, ts.ge, ts.tdr)
    if re.match(r'^(RP)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+)$', report.text, re.I):
        reporter = Reporter.objects.get(phone_number=kwargs['phone'])
        st, created = StockOutReport.objects.get_or_create(product=product, report=report)
        st.remaining = values
        st.save()
        send_sms_through_rapidpro({'urns': ["tel:"+reporter.supervisor_phone_number, ], "groups": [GROUPS], 'text': "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(report.facility, st.remaining, product.designation, st.reporting_date.strftime('%Y-%m-%d'))})
        return "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(report.facility, st.remaining, product.designation, st.reporting_date.strftime('%Y-%m-%d'))

    if re.match(r'^(HBD|HBC)\s+(\d{6})(\s+\d+){8}$', report.text, re.I):
        ps = None
        if "HBC" in report.text.split(" "):
            ps = PotentialCases.objects.create(report=report, fpa=values[0], cholera=values[0], meningit=values[0], rougeole=values[0], tnn=values[0], fievre_hemoragique=values[0], paludisme=values[0], other=values[0])
        else:
            ps = PotentialDeceased.objects.create(report=report, fpa=values[0], cholera=values[0], meningit=values[0], rougeole=values[0], tnn=values[0], fievre_hemoragique=values[0], paludisme=values[0], other=values[0])
        ps.save()
        return "Kuri {0}, handitswe hari abagwaye FPA {1}, Cholera {2}, Menengite {3}, Rougeole {4}, TNN {5}, Fievre Hemoragique {6}, Paludisme {7}, n'abandi {8}. Murakoze".format(report.facility, ps.fpa, ps.cholera, ps.meningit, ps.rougeole, ps.tnn, ps.fievre_hemoragique, ps.paludisme, ps.other)
    elif re.match(r'^(SF)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+){1,3}$', report.text, re.I):
        values = report.text.split(" ")[3:]
        products = [m.code for m in Product.objects.all().distinct()]
        if product.code in products:
            if report.text.split(" ")[0] in ["RP"]:
                st = StockOutReport.objects.create(product=product, report=report, remaining=values[0])
                st.save()
                return "Kuri {0}, handitswe ko hasigaye {1}, za {2} kw'itariki {3}. Murakoze".format(report.facility, values[0], product.designation, st.reporting_date.strftime('%Y-%m-%d'))
            else:
                message = ""
                dosages = product.dosages.all()
                for dose in dosages:
                    sp = StockProduct.objects.create(product=product, report=report, dosage=dose, quantity=values[dose.rank])
                    sp.save()
                    message += sp.quantity + " (" + dose.dosage + "), "
                return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)
    else:
        return "Ivyo mwanditse sivyo. Andika uko bakwigishije."


def update_stockproduct(report=None, product=None, *args, **kwargs):
    values = report.text.split(" ")[2:]
    if re.match(r'^(CA)\s+(\d{6})(\s+\d+){4}$', report.text, re.I):
        cp, created = CasesPalu.objects.get_or_create(report=report)
        cp.simple, cp.acute, cp.pregnant_women, cp.decease = values
        cp.save()
        return "Kuri {0}, handitswe ko hari abagwayi ba malaria {1}, abaremvye {2}, abagore bibungeze bayigwaye {3}, abitavye Imana ni {4}. Murakoze".format(report.facility, cp.simple, cp.acute, cp.pregnant_women, cp.decease)

    if re.match(r'^(TS)\s+(\d{6})(\s+\d+){2}$', report.text, re.I):
        # import ipdb; ipdb.set_trace()
        ts, created = Tests.objects.get_or_create(report=report)
        ts.ge, ts.tdr = values
        ts.save()
        return "Kuri {0}, handitswe ko hakozwe ama test ge {1}, na TDR {2}. Murakoze".format(report.facility, ts.ge, ts.tdr)

    if re.match(r'^(HBD|HBC)\s+(\d{6})(\s+\d+){8}$', report.text, re.I):
        ps = None
        if "HBC" in report.text.split(" "):
            ps, created = PotentialCases.objects.get_or_create(report=report)
        else:
            ps, created = PotentialDeceased.objects.get_or_create(report=report)
        ps.fpa, ps.cholera, ps.meningit, ps.rougeole, ps.tnn, ps.fievre_hemoragique, ps.paludisme, ps.other = values
        ps.save()
        return "Kuri {0}, handitswe hari abagwaye FPA {1}, Cholera {2}, Menengite {3}, Rougeole {4}, TNN {5}, Fievre Hemoragique {6}, Paludisme {7}, n'abandi {8}. Murakoze".format(report.facility, ps.fpa, ps.cholera, ps.meningit, ps.rougeole, ps.tnn, ps.fievre_hemoragique, ps.paludisme, ps.other)
    if re.match(r'^(RP)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+)$', report.text, re.I):
        reporter = Reporter.objects.get(phone_number=kwargs['phone'])
        st, created = StockOutReport.objects.get_or_create(product=product, report=report)
        st.remaining = values[1]
        st.save()
        send_sms_through_rapidpro({'urns': ["tel:"+reporter.supervisor_phone_number, ], "groups": [GROUPS], 'text': "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(report.facility, st.remaining, product.designation, st.reporting_date.strftime('%Y-%m-%d'))})
        return "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(report.facility, st.remaining, product.designation, st.reporting_date.strftime('%Y-%m-%d'))

    elif re.match(r'^(SF)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+){1,3}$', report.text, re.I):
        values = report.text.split(" ")[3:]
        dosages = product.dosages.all()
        message = ""
        for dose in dosages:
            sp, created = StockProduct.objects.get_or_create(product=product, report=report, dosage=dose)
            sp.quantity = values[dose.rank]
            sp.save()
            message += sp.quantity + " (" + dose.dosage + "), "

        return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)

    else:
        return "Ivyo mwanditse sivyo. Andika uko bakwigishije."
