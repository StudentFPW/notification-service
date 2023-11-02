import pytz

from django.db import models


class SetTimeZone(models.Model):
    """
    The SetTimeZone class is a model in Python that allows users to select a timezone from a list of available options.
    """
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Mailing(models.Model):
    """
    The Mailing class represents a mailing with a start and end date, start and end time,
    text content, country code, and tag, and has a property to check if the mailing is within the date range to be sent.
    """
    date_start = models.DateTimeField(blank=False, null=False)
    text = models.TextField(max_length=300, blank=False, null=False)
    country_code = models.CharField(max_length=5, blank=False, null=False)
    tag = models.CharField(max_length=10, default="")
    date_end = models.DateTimeField(blank=False, null=False)


class Client(models.Model):
    """
    The `Client` class represents a client with attributes such as phone number, country code, tag, and timezone.
    """
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    country_code = models.CharField(max_length=5, blank=False, null=False)
    tag = models.CharField(max_length=10, default="")

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Message(models.Model):
    """
    The `Message` class represents a message with a start date, start time, status, and related mailing and client.
    """
    SENT = "sent"
    NO_SENT = "no sent"
    PENDING = "pending"

    STATUS_CHOICES = [
        (SENT, "Sent"),
        (NO_SENT, "No sent"),
        (PENDING, "Pending"),
    ]

    date_start = models.DateField(auto_now_add=True)
    time_start = models.TimeField(auto_now_add=True)

    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
