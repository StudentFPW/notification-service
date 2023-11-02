import pytz

from datetime import datetime
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_it

from .models import Mailing, Client, Message, SetTimeZone


@receiver(post_save, sender=User)
def user_created(instance, created, **kwargs):
    """
    The above function adds the user to the "common users" group after the user is created.

    :param instance: The "instance" parameter refers to the instance of the User model that was just saved.
    In other words, it represents the specific user object that triggered the post_save signal

    :param created: The `created` parameter is a boolean value that indicates whether the instance being saved is a new
    object or an existing one being updated.
    It will be `True` if the instance is newly created, and `False` if it is being updated

    :return: the user object.
    """
    if created:
        user = instance
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user


@receiver(post_save, sender=Mailing)
def mailing_created(instance, created, **kwargs):
    """
    This function is a signal receiver that is triggered after a Mailing instance is saved, and it performs some action.

    :param instance: The instance parameter refers to the instance of the Mailing model that was just created or updated

    :param created: The "created" parameter is a boolean value that indicates whether a new instance of
    the Mailing model was created or an existing instance was updated.

    It will be True if a new instance was created and False if an existing instance was updated
    """
    if not created:
        return

    clients_data = Client.objects.filter(country_code=instance.country_code, tag=instance.tag)

    for client in clients_data:
        message = Message.objects.create(status="No sent", client_id=client.id, mailing_id=instance.id)

        data_to_send = {
            "id": int(message.id),
            "phone": int(client.phone_number),
            "text": str(instance.text)
        }

        message_id = message.id
        client_id = client.id
        mailing_id = instance.id

        obj = SetTimeZone.objects.all().last()
        zone = pytz.timezone(obj.timezone)
        time = datetime.now(zone)

        check_date = instance.date_start.date() <= time.date() <= instance.date_end.date()

        # The code block is checking if the current date falls within the range specified by `instance.date_start` and
        # `instance.date_end`.
        if check_date:
            send_it.apply_async((data_to_send, client_id, mailing_id, message_id), expires=instance.date_end)
        else:
            send_it.apply_async(
                (data_to_send, client_id, mailing_id, message_id),
                eta=instance.date_start,
                expires=instance.date_end,
            )
