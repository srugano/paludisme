import re
from stock.models import (
    StockProduct,
    StockOutReport,
    CasesPalu,
    Tests,
    PotentialCases,
    PotentialDeceased,
    Reporter,
)
from paludisme.utils import send_sms_through_rapidpro
from django.conf import settings


GROUPS = getattr(settings, "RUPTURE_GROUPS", "")


def create_stockproduct(report=None, product=None, *args, **kwargs):
    values = report.text.strip().split(" ")[2:]
    if re.match(r"^(CA)\s+(\d{6})(\s+\d+){4}$", report.text.strip(), re.I):
        cp = CasesPalu.objects.create(
            report=report,
            simple=values[0],
            acute=values[1],
            pregnant_women=values[2],
            decease=values[3],
        )
        cp.save()
        return "Kuri {0}, handitswe ko hari abagwayi ba malaria {1}, abaremvye {2}, abagore bibungeze bayigwaye {3}, abitavye Imana ni {4}. Murakoze".format(
            report.facility, cp.simple, cp.acute, cp.pregnant_women, cp.decease
        )
    if re.match(r"^(TS)\s+(\d{6})(\s+\d+){2}$", report.text.strip(), re.I):
        ts = Tests.objects.create(report=report, ge=values[0], tdr=values[1])
        ts.save()
        return "Kuri {0}, handitswe ko hakozwe ama test ge {1}, na TDR {2}. Murakoze".format(
            report.facility, ts.ge, ts.tdr
        )
    if re.match(
        r"^(RP)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+)$", report.text.strip(), re.I
    ):
        reporter = Reporter.objects.get(phone_number=kwargs["phone"])
        st, created = StockOutReport.objects.get_or_create(
            product=product, report=report
        )
        st.remaining = values
        st.save()
        send_sms_through_rapidpro(
            {
                "urns": ["tel:" + reporter.supervisor_phone_number],
                "groups": [GROUPS],
                "text": "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(
                    report.facility,
                    st.remaining,
                    product.designation,
                    st.reporting_date.strftime("%Y-%m-%d"),
                ),
            }
        )
        return "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(
            report.facility,
            st.remaining,
            product.designation,
            st.reporting_date.strftime("%Y-%m-%d"),
        )

    if re.match(r"^(HBD|HBC)\s+(\d{6})(\s+\d+){8}$", report.text.strip(), re.I):
        ps = None
        if "HBC" in report.text.strip().split(" "):
            ps = PotentialCases.objects.create(
                report=report,
                fpa=values[0],
                cholera=values[0],
                meningit=values[0],
                rougeole=values[0],
                tnn=values[0],
                fievre_hemoragique=values[0],
                paludisme=values[0],
                other=values[0],
            )
        else:
            ps = PotentialDeceased.objects.create(
                report=report,
                fpa=values[0],
                cholera=values[0],
                meningit=values[0],
                rougeole=values[0],
                tnn=values[0],
                fievre_hemoragique=values[0],
                paludisme=values[0],
                other=values[0],
            )
        ps.save()
        return "Kuri {0}, handitswe hari abagwaye FPA {1}, Cholera {2}, Menengite {3}, Rougeole {4}, TNN {5}, Fievre Hemoragique {6}, Paludisme {7}, n'abandi {8}. Murakoze".format(
            report.facility,
            ps.fpa,
            ps.cholera,
            ps.meningit,
            ps.rougeole,
            ps.tnn,
            ps.fievre_hemoragique,
            ps.paludisme,
            ps.other,
        )
    elif re.match(
        r"^(SF|SR|SD)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+){1,4}$",
        report.text.strip().strip(),
        re.I,
    ):
        values = report.text.strip().strip().split(" ")[3:]
        if (
            report.text.strip().strip().split(" ")[0] in ["SF"]
            and report.reporting_date.weekday() != 0
        ):
            return "Itariki mwandiste siyo, kuko itariki bandika ari iyo ku wambere. Bibwire uwubatwara."
        message = ""
        dosages = product.dosages.all()
        for dose in dosages:
            sp = StockProduct.objects.create(
                product=product, report=report, dosage=dose
            )
            try:
                sp.quantity = values[dose.rank]
            except IndexError:
                sp.quantity = 0
            sp.reporting_date = report.reporting_date
            try:
                sp.save()
            except ValueError:
                print values, report
            message += "{0}".format(sp.quantity) + " (" + dose.dosage + "), "
        return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(
            report.facility, message, product.designation
        )
    else:
        return "Ivyo mwanditse sivyo. Andika uko bakwigishije."


def update_stockproduct(report=None, product=None, *args, **kwargs):
    values = report.text.strip().split(" ")[2:]
    if re.match(r"^(CA)\s+(\d{6})(\s+\d+){4}$", report.text.strip(), re.I):
        cp, created = CasesPalu.objects.get_or_create(report=report)
        cp.simple, cp.acute, cp.pregnant_women, cp.decease = values
        cp.save()
        return "Kuri {0}, handitswe ko hari abagwayi ba malaria {1}, abaremvye {2}, abagore bibungeze bayigwaye {3}, abitavye Imana ni {4}. Murakoze".format(
            report.facility, cp.simple, cp.acute, cp.pregnant_women, cp.decease
        )

    if re.match(r"^(TS)\s+(\d{6})(\s+\d+){2}$", report.text.strip(), re.I):
        # import ipdb; ipdb.set_trace()
        ts, created = Tests.objects.get_or_create(report=report)
        ts.ge, ts.tdr = values
        ts.save()
        return "Kuri {0}, handitswe ko hakozwe ama test ge {1}, na TDR {2}. Murakoze".format(
            report.facility, ts.ge, ts.tdr
        )

    if re.match(r"^(HBD|HBC)\s+(\d{6})(\s+\d+){8}$", report.text.strip(), re.I):
        ps = None
        if "HBC" in report.text.strip().split(" "):
            ps, created = PotentialCases.objects.get_or_create(report=report)
        else:
            ps, created = PotentialDeceased.objects.get_or_create(report=report)
        ps.fpa, ps.cholera, ps.meningit, ps.rougeole, ps.tnn, ps.fievre_hemoragique, ps.paludisme, ps.other = (
            values
        )
        ps.save()
        return "Kuri {0}, handitswe hari abagwaye FPA {1}, Cholera {2}, Menengite {3}, Rougeole {4}, TNN {5}, Fievre Hemoragique {6}, Paludisme {7}, n'abandi {8}. Murakoze".format(
            report.facility,
            ps.fpa,
            ps.cholera,
            ps.meningit,
            ps.rougeole,
            ps.tnn,
            ps.fievre_hemoragique,
            ps.paludisme,
            ps.other,
        )
    if re.match(
        r"^(RP)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+)$", report.text.strip(), re.I
    ):
        reporter = Reporter.objects.get(phone_number=kwargs["phone"])
        st, created = StockOutReport.objects.get_or_create(
            product=product, report=report
        )
        st.remaining = values[1]
        st.save()
        send_sms_through_rapidpro(
            {
                "urns": ["tel:" + reporter.supervisor_phone_number],
                "groups": [GROUPS],
                "text": "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(
                    report.facility,
                    st.remaining,
                    product.designation,
                    st.reporting_date.strftime("%Y-%m-%d"),
                ),
            }
        )
        return "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(
            report.facility,
            st.remaining,
            product.designation,
            st.reporting_date.strftime("%Y-%m-%d"),
        )

    elif re.match(
        r"^(SF|SR|SD)\s+(\d{6})\s+(qui|ACT|ART|TDR|SP)(\s+\d+){1,4}$",
        report.text.strip(),
        re.I,
    ):
        if (
            report.text.strip().split(" ")[0] in ["SF"]
            and report.reporting_date.weekday() != 0
        ):
            return "Itariki mwandiste siyo, kuko itariki bandika ari iyo ku wambere. Bibwire uwubatwara."
        values = report.text.strip().split(" ")[3:]
        dosages = product.dosages.all()
        message = ""
        for dose in dosages:
            sp, created = StockProduct.objects.get_or_create(
                product=product, report=report, dosage=dose
            )
            sp.reporting_date = report.reporting_date
            try:
                sp.quantity = values[dose.rank]
            except IndexError:
                sp.quantity = 0
            try:
                sp.save()
            except ValueError:
                print values, report
            message += "{0}".format(sp.quantity) + " (" + dose.dosage + "), "

        return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(
            report.facility, message, product.designation
        )

    else:
        return "Ivyo mwanditse sivyo. Andika uko bakwigishije."
