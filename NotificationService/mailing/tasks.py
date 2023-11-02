import os
import pytz
import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
from dotenv import load_dotenv

from .models import Mailing, Client, Message

# The line `logger = get_task_logger(__name__)` is creating a logger object specific to the current task. The
# `get_task_logger()` function is a utility function provided by Celery that returns a logger object configured to log
# messages related to the current task. The `__name__` argument is used to specify the name of the logger, which is
# typically set to the name of the current module. This logger can be used to log messages at different levels (e.g.,
# info, error) during the execution of the task.
logger = get_task_logger(__name__)

# `load_dotenv()` is a function from the `dotenv` library that loads environment variables from a `.env` file into the
# current environment.
load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


@shared_task(bind=True, retry_kwargs={'max_retries': 10, 'countdown': 5})
def send_it(self, content, client_id, mailing_id, message_id):
    """
    The function "send_it" is a shared task in Python that takes in parameters such as
    content, client_id, mailing_id, and message_id, and has retry options set to a maximum
    of 10 retries with a countdown of 5 seconds between each retry.

    :param content: The content of the message that you want to send

    :param client_id: The client ID is a unique identifier for the client that the message is being sent to. It helps in
    identifying the recipient of the message

    :param mailing_id: The mailing_id parameter is used to identify the specific mailing that the content is associated
    with. It could be an ID or a unique identifier for the mailing

    :param message_id: The `message_id` parameter is used to identify a specific message that needs to be sent. It is
    typically a unique identifier assigned to each message in the system
    """
    head = {
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-Type": "application/json",
    }

    client = Client.objects.get(pk=client_id)
    zone = pytz.timezone(client.timezone)
    time = datetime.now(zone)

    url_to_send = URL + str(message_id)

    the = Mailing.objects.get(id=mailing_id)

    time_correct = the.date_start.time() <= time.time() <= the.date_end.time()

    # This code block is responsible for sending a POST request to a specified URL with the provided content ↓.
    if time_correct:
        try:
            requests.post(url=url_to_send, headers=head, json=content)
        # This code block is handling an exception that occurs when there is a problem with the POST request ↓.
        except requests.exceptions.RequestException as problem:
            logger.error(f"Problem: message id - ({message_id})")
            raise self.retry(exc=problem, countdown=5)
        else:
            logger.info(f"Successfully sent message: message id - ({message_id})")
            Message.objects.filter(pk=message_id).update(status="Sent")
    # This code block is executed when the current time is not within the specified time range for sending the message ↓
    else:
        Message.objects.filter(pk=message_id).update(status="Pending")
        # This code block is executed when the current time is not within the specified time range for sending the
        # message, but the hour of the start time matches the current hour ↓.
        if the.date_start.time().hour == time.time().hour:
            minute_seconds = (int(the.date_start.time().minute) * 60) - (int(time.minute) * 60) + 60
            logger.info(
                f"Message id: {content['id']}, "
                f"restarting task after {minute_seconds} seconds"
            )
            return self.retry(countdown=minute_seconds)
        else:
            # This code block is calculating the time difference between the current time and the start time of the
            # message ↓.
            hour_minute_seconds = ((int(the.date_start.time().hour) * 60) - (int(time.hour) * 60) * 60)
            minute_seconds = (int(the.date_start.time().minute) - (int(time.minute) * 60) * 60)
            time_result = hour_minute_seconds + minute_seconds + 60

            logger.info(
                f"Message id: {content['id']}, "
                f"restarting task after {time_result} seconds"
            )
            return self.retry(countdown=time_result)
