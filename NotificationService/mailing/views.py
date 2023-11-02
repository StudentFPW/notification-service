from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .serializers import MailingSerializer, ClientSerializer, MessageSerializer, SetTimeZoneSerializer
from .models import Mailing, Client, Message, SetTimeZone


class SetTimeZoneViewset(LoginRequiredMixin, viewsets.ModelViewSet):
    raise_exception = True
    queryset = SetTimeZone.objects.all()
    serializer_class = SetTimeZoneSerializer


class MailingViewset(LoginRequiredMixin, PermissionRequiredMixin, viewsets.ModelViewSet):
    permission_required = ('mailing.add_mailing', 'mailing.change_mailing', 'mailing.delete_mailing')
    raise_exception = True
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=False, methods=["get"])
    def general_statistics(self, request):
        """
        The `general_statistics` function retrieves general statistics on the created mailing lists
        and the number of sent messages on them, grouped by status.

        :param request: The `request` parameter is an object that represents the HTTP request made to the API.
        It contains information such as the request method (e.g., GET, POST), headers, query parameters,
        and the request body. In this case, the `request` parameter is used to handle a GET request

        :return: a Response object with the content dictionary. The content dictionary contains the total
        number of mailings and the number of messages sent, grouped by status.
        The number of messages sent is further broken down by the mailing ID.
        """
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values("id")

        content = {
            "Total number of mailings": total_count,
            "The number of messages sent": "",
        }
        result = {}

        for data in mailing:
            res = dict()

            get_mail_data = Message.objects.filter(mailing_id=data["id"]).all()

            sent = get_mail_data.filter(status="Sent").count()
            no_sent = get_mail_data.filter(status="No sent").count()
            pending = get_mail_data.filter(status="Pending").count()

            res["Total message"] = len(get_mail_data)
            res["Sent"] = sent
            res["No sent"] = no_sent
            res["Pending"] = pending

            result[data["id"]] = res

        content["The number of messages sent"] = result
        return Response(content)

    @action(detail=True, methods=["get"])
    def specific(self, request, pk=None):
        """
        The above function retrieves all messages associated with a specific mailing object.

        param request: The `request` parameter is an object that represents the HTTP request made by the client.
        It contains information such as the request method (GET, POST, etc.),
        headers, query parameters, and the request body

        param pk: The "pk" parameter stands for "primary key" and is used to identify a specific object in the database.
        In this case, it is used to retrieve a specific Mailing object based on its primary key value.
        The primary key is a unique identifier assigned to each object in the database

        return: The code is returning a response containing serialized
        data of messages that belong to a specific mailing.
        """
        get_queryset = Mailing.objects.all()

        get_object_or_404(get_queryset, pk=pk)

        queryset = Message.objects.filter(mailing_id=pk).all()

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)


class ClientViewset(LoginRequiredMixin, PermissionRequiredMixin, viewsets.ModelViewSet):
    permission_required = ('mailing.add_client', 'mailing.change_client', 'mailing.delete_client')
    raise_exception = True
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewest(LoginRequiredMixin, PermissionRequiredMixin, viewsets.ModelViewSet):
    permission_required = ('mailing.add_message', 'mailing.change_message', 'mailing.delete_message')
    raise_exception = True
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
