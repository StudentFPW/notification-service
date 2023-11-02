from .models import Mailing, Client, Message, SetTimeZone
from rest_framework import serializers


class SetTimeZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SetTimeZone
        fields = "__all__"


class MailingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

# The above code defines serializers for the SetTimeZone, Mailing, Client, and Message models in Python.
