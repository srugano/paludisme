from stock.models import Report
from django.http import HttpResponse
from import_export import resources
from django.views.decorators.csrf import csrf_exempt
import json


class BookResource(resources.ModelResource):

    class Meta:
        model = Report
        fields = ('id', 'facility__name', 'facility__district__name', 'facility__district__province__name', 'reporting_date', 'text', 'category')


@csrf_exempt
def export_to_excel(request, *args, **kwargs):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    queriset = Report.objects.all()
    if request.POST.get("enddate", ""):
        queriset = queriset.filter(reporting_date__lte=request.POST.get("enddate", ""))
    if request.POST.get("startdate", ""):
        queriset = queriset.filter(reporting_date__gte=request.POST.get("startdate", ""))
    if request.POST.get("cds", ""):
        queriset = queriset.filter(facility__code=json.loads(request.POST.get("cds", ""))['code'])
    if request.POST.get("district", ""):
        queriset = queriset.filter(facility__district__code=json.loads(request.POST.get("district", ""))['code'])
    if request.POST.get("province", ""):
        queriset = queriset.filter(facility__district__province__code=json.loads(request.POST.get("province", ""))['code'])
    dataset = BookResource().export(queriset)
    response.write(dataset.xls)
    return response
