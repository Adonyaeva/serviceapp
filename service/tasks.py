import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from serviceapp.celeryconf import app
from service.models import Ticket


@app.task
def send_status_email(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        from_address = getattr(settings, 'DEFAULT_FROM_EMAIL')
        recipient_list = [ticket.user.email, from_address]
        subject = 'Статус заявки был изменен'
        body = 'Изменен статус заявки ' + str(ticket.id)
        msg = EmailMultiAlternatives(subject, body, from_address, recipient_list)
        msg.send()
    except Ticket.DoesNotExist:
        logging.warning('Problem with sending of changed status of ticket id ' + ticket_id)
