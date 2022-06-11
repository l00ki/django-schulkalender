from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.db import models
from django import forms


class Event(models.Model):
    title = models.CharField("Titel", max_length=100)
    author = models.CharField(max_length=100)
    recipients = models.CharField("Addressaten", max_length=100, blank=True, null=True)
    location = models.CharField("Ort", max_length=100, blank=True, null=True)
    start_date = models.DateField("Datum")
    start_period = models.IntegerField("Startstunde", blank=True, null=True)
    start_time = models.TimeField("Startzeit", blank=True, null=True)
    end_date = models.DateField("Enddatum", blank=True, null=True)
    end_period = models.IntegerField("Endstunde", blank=True, null=True)
    end_time = models.TimeField("Endzeit", blank=True, null=True)
    all_day = models.BooleanField("Ganztag?")
    description = models.TextField("Beschreibung", blank=True, null=True)

    def __repr__(self):
        return f"Event(\"{self.title}\", \"{self.author}\", \"{self.location}\", " \
               f"{self.start_date}, {self.start_time}, {self.end_date}, {self.end_time}, " \
               f"{self.all_day}, \"{self.description}\", \"{self.recipients}\")"

    def __str__(self):
        return f"{self.title} am {self.start_date} ({self.recipients}) von {self.author}"

    def echo(self):
        return self.__str__()
