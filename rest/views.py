from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db import transaction
from django.db import models
from django.utils import timezone
from .models import Deal
import csv


@api_view(['GET'])
def get_processing_result(request):
    with transaction.atomic():
        top5 = Deal.objects.values('customer') \
            .annotate(total=models.Sum('total')) \
            .order_by('-total')[0:5]

        top5 = list(top5)
        customers = [x['customer'] for x in top5]
        
        # Since nested query for all (customer, item) pairs, such that each customer is 
        # part of top5 and each gem was chosen by at least two members of top5
        multipick = Deal.objects.values('item') \
            .filter(customer__in=customers) \
            .annotate(count=models.Count('customer', distinct=True)) \
            .filter(count__gte=2) \
            .values('item') # query for all gems picked at least twice
        gems = Deal.objects.values('item', 'customer') \
            .filter(customer__in=customers) \
            .filter(item__in=multipick) \
            .distinct()
        gems = list(gems)

    result = {c['customer']: {'username': c['customer'], 'money_spent': c['total'], 'gems': []} for c in top5}
    for gem_pair in gems:
        username = gem_pair['customer']
        gem = gem_pair['item']
        result[username]['gems'].append(gem)

    result = list(result.values())
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['POST'])
def process_deals(request):
    try:
        deals = request.FILES.get('deals')
        if deals is None:
            raise ValidationError("Request must contain csv file `deals`")

        deals_csv = csv.reader(x.decode('UTF-8') for x in deals)
        deals_data = validate_csv(deals_csv)
        with transaction.atomic():
            Deal.objects.all().delete()
            Deal.objects.bulk_create(deals_data)
        return Response(status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(data={'Desc': e.data['detail']}, status=status.HTTP_400_BAD_REQUEST)
    except csv.Error as e:
        return Response(data={'Desc': 'Error handling csv file: `{}`'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    except UnicodeDecodeError:
        return Response(data={'Desc': 'Csv file must have UTF-8 encoding'}, status=status.HTTP_400_BAD_REQUEST)


def processing_result(request):
    raise Exception('Unimplemented')


def validate_csv(deal_iter):
    """
    Validate csv and return list of objects of type `Deal`
    """
    def try_row_to_deal(deal_csv_row):
        customer, item, total, quantity, date = tuple(deal_csv_row)
        return Deal(None, customer, item, total, quantity, timezone.make_aware(date))

    header = next(deal_iter)
    expected_header = ['customer', 'item', 'total', 'quantity', 'date']
    if header != expected_header:
        raise ValidationError('Must contain header `{}`'.format(', '.join(expected_header)))
    try:
        return [try_row_to_deal(x) for x in deal_iter]
    except ValueError:
        raise ValidationError('Must contain following columns: {}'.format(', '.join(expected_header)))

