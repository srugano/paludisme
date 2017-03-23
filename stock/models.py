from __future__ import unicode_literals
from bdiadmin.models import CDS
from django.db import models
from django.utils.translation import ugettext_lazy as _


REPORT_CHOICES = (
    ("SDG", _("Stock Start of Day")),
    ("REC", _("Received")),
    ("DIS", _("Distributed")),
)


class Dosage(models.Model):
    dosage = models.CharField(max_length=30)

    def __unicode__(self):
        return self.dosage

    class Meta:
        ordering = ('dosage',)


class Product(models.Model):
    ''' This model will be used to store products '''
    designation = models.CharField(max_length=40)
    dosages = models.ManyToManyField(Dosage)

    def __unicode__(self):
        return self.designation

    class Meta:
        ordering = ('designation',)


class Reporter(models.Model):
    '''In this model, we will store reporters'''
    facility = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return "Tel: {0} on {1} cds".format(self.phone_number, self.facility)

    class Meta:
        ordering = ('phone_number',)


class Report(models.Model):
    ''' In this model, we will store all reports sent by reporters '''
    facility = models.ForeignKey(CDS)
    reporting_date = models.DateField()
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=3, choices=REPORT_CHOICES)

    def __unicode__(self):
        return "Report of {0}, containing {1}".format(self.category, self.text)

    class Meta:
        ordering = ('reporting_date',)


class StockProduct(models.Model):
    report = models.ForeignKey(Report)
    product = models.ForeignKey(Product)
    dosage = models.ForeignKey(Dosage)
    quantity = models.FloatField(default=0.0)

    def __unicode__(self):
        return "{0} - {1}".format(self.report.text, self.quantity)

    class Meta:
        ordering = ('report',)
