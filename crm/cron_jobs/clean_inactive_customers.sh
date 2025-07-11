#!/bin/bash

cwd="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(dirname "$cwd")" || exit 1

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

if [ $? -eq 0 ]; then
  echo "$timestamp - Deleted $deleted_count inactive customers." >> /tmp/customer_cleanup_log.txt
else
  echo "$timestamp - Failed to delete customers." >> /tmp/customer_cleanup_log.txt
fi
