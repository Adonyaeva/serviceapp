from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
# from serviceapp.celery import app


@app.task
def send_email(recipient_list, subject, body, from_address):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    if not from_address:
        from_address = getattr(settings, 'EMAIL_FROM_ADDRESS')

    msg = EmailMultiAlternatives(subject, body, from_address, recipient_list)
    msg.send()
