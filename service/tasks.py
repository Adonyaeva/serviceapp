import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from serviceapp.celery import app
from service.models import Ticket


@app.task
def send_email(time_slot_id):
    try:
        ticket = Ticket.objects.get(time_slot_id=time_slot_id)
        from_address = getattr(settings, 'EMAIL_FROM_ADDRESS')
        recipient_list = [ticket.user.email, from_address]
        subject = 'Статус заявки был изменен'
        body = 'Изменен статус заявки ' + ticket.id
        msg = EmailMultiAlternatives(subject, body, from_address, recipient_list)
        msg.send()
    except Ticket.DoesNotExist:
        logging.warning('Problem with sending of changed status email for user' + ticket.user.id)
