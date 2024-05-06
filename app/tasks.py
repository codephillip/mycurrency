from django.core.management import call_command
from datetime import datetime

from mycurrency.constants import DATE_FORMAT


def fetch_daily_dummy_rates_task():
    call_command('fetch_exchange_rates', date=datetime.now().strftime(DATE_FORMAT))
