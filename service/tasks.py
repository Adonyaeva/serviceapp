import logging
from django.conf import settings
from django.core.mail import send_mail
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
        try:
            send_mail(
                subject,
                body,
                from_address,
                recipient_list,
                fail_silently=False,
            )
        except:
            logging.warning('Email about changed status can not been sent.')
    except Ticket.DoesNotExist:
        logging.warning('Problem with sending email of changed status of ticket: no ticket with such id '
                        + str(ticket_id))
