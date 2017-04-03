from __future__ import unicode_literals
from bdiadmin.models import CDS
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from paludisme.utils import phone_regex


class Dosage(models.Model):
    dosage = models.CharField(max_length=30)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.dosage

    class Meta:
        ordering = ('dosage',)


class Product(models.Model):
    ''' This model will be used to store products '''
    designation = models.CharField(max_length=40)
    dosages = models.ManyToManyField(Dosage)
    code = models.CharField(max_length=3, blank=True)

    def __unicode__(self):
        return self.designation

    class Meta:
        ordering = ('designation',)


class Reporter(models.Model):
    '''In this model, we will store reporters'''
    facility = models.ForeignKey(CDS)
    phone_number = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)
    supervisor_phone_number = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)

    def __unicode__(self):
        return "Tel: {0} on {1} cds".format(self.phone_number, self.facility)

    class Meta:
        ordering = ('phone_number',)


class Report(models.Model):
    ''' In this model, we will store all reports sent by reporters '''
    facility = models.ForeignKey(CDS)
    reporting_date = models.DateField()
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=3, choices=settings.KNOWN_PREFIXES)

    def __unicode__(self):
        return "Report of {0}, containing {1}".format(self.category, self.text)

    class Meta:
        ordering = ('reporting_date',)


class StockProduct(models.Model):
    report = models.ForeignKey(Report)
    product = models.ForeignKey(Product)
    dosage = models.ForeignKey(Dosage)
    quantity = models.FloatField(default=0.0)
    reporting_date = models.DateField(default=timezone.now)

    def __unicode__(self):
        return "{0} - {1}".format(self.report.text, self.quantity)

    class Meta:
        ordering = ('report',)


class Temporary(models.Model):
    '''
    This model will be used to temporary store a reporter who doesn't finish his self registration
    '''
    facility = models.ForeignKey(CDS)
    phone_number = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact the sender.'), max_length=16)
    supervisor_phone_number = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact your supervisor.'), max_length=16)

    def __unicode__(self):
        return self.phone_number


class StockOutReport(models.Model):
    ''' Informations given in a stock out report are stored in this model '''
    report = models.ForeignKey(Report)
    product = models.ForeignKey(Product)
    remaining = models.FloatField(default=0.0)
    reporting_date = models.DateField(default=timezone.now)

    def __unicode__(self):
        return "{0} => Remaining quantity: {1}".format(self.produit.designation, self.remaining)
