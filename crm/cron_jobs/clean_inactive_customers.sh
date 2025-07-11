#!/bin/bash

timestamp=$(date '+%Y-%m-%d %H:%M:%S')

deleted_count=$(python manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)

customers_to_delete = Customer.objects.exclude(
    id__in=Order.objects.filter(order_date__gte=one_year_ago).values_list('customer_id', flat=True)
)

count, _ = customers_to_delete.delete()
print(count)
EOF
)

echo "$timestamp - Deleted $deleted_count inactive customers." >> /tmp/customer_cleanup_log.txt
