from service.models import Address


def get_or_create_adress(req_address):
    try:
        address = Address.objects.get(
            street_name=req_address['street_name'],
            house_number=req_address['house_number'],
            flat_number=req_address['flat_number'],
        )
    except Address.DoesNotExist:
        address = Address.objects.create(
            street_name=req_address['street_name'],
            house_number=req_address['house_number'],
            house_id=req_address['house_id'],
            flat_number=req_address['flat_number'],
            flat_id=req_address['flat_id'],
        )
    return address
