# mycurrency

This document outlines the setup, usage, and design of mycurrency.

## Tools
- **Python3:** Programming language used by the driver and workers.
- **Django:** Facilitates REST communication implementation.
- **Django Rest Framework:** Extends Django for building RESTful APIs.
- **requests:** Executes HTTP requests.
- **unsync:** Performs asynchronous tasks.
- **cronjob:** Manages periodic tasks.
- **sqlite3:** Temporary test database for storage.

## Setup

- Create a virtual environment and activate env `python3 -m venv venv & source venv/bin/activate`
- Install requirements using `pip3 install -r requirements.txt`
- Run migrations `./manage.py migrate`
- Run server `./manage.py runserver`
- Create admin user `./manage.py createsuperuser`
- Set up cronjob. `python manage.py crontab add`
- Upload exchange data using either the commands, cronjob or [bulk upload](http://127.0.0.1:8000/api/uploadExchangesJson)
- Load the postman collection

## Usage
### Authentication
- Navigate to the [login page](http://127.0.0.1:8000/auth/token/login)
- Enter username and password
- Copy the `token` and add it to the postman envs

### Normal User URLs
- Load the Postman collection: [`mycurrency.postman_collection.json`](#).

### Admin URLs
- [Currency Exchange](http://127.0.0.1:8000/admin/app/currencyexchangerate/currencyExchange/)
- [Exchange Rate Graph](http://127.0.0.1:8000/admin/app/currencyexchangerate/exchangeRateGraph/)

### Cronjob
- Add daily exchange importer from real server to the database: `python manage.py crontab add`.

### Commands

- fetch_exchange_rates: add dummy exchange data
`python manage.py fetch_exchange_rates --date='2024-04-30'`


- provider_importer: adds new exchange provider that fetches data from real server

```
python3 manage.py provider_importer \
--code="""
from provider_service import Provider
from datetime import datetime
from typing import List
import requests

class Fixer(Provider):
    def execute_api(self, source_currency, exchanged_currencies, valuation_date):
        params = {
            'access_key': self.apikey,
            'base': source_currency,
            'symbols': exchanged_currencies
        }
        return requests.get(url=self.url + f'/{valuation_date}', params=params)

    def get_exchange_rate_data(self, source_currency: str, exchanged_currencies: List[str],
                               valuation_date=datetime.now()):
        response = self.execute_api(source_currency, exchanged_currencies, valuation_date.strftime('%Y-%m-%d'))
        return response.json()['rates'] if response.status_code == 200 else None

url = 'http://data.fixer.io/api'
apikey = 'YOUR_KEY'
provider = Fixer(url, apikey)
""" --provider_name="fixer"
```

- provider_importer: adds new exchange provider that extracts data from precreated json files
NOTE: make sure a json file in this format(EUR_2024-05-22) has been uploaded before using the fixermock

```
python3 manage.py provider_importer \
--code="""
from provider_service import Provider
from datetime import datetime
from typing import List
import requests

import json
import os


class FixerMock(Provider):
    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f'File {file_path} not found.')
        except json.JSONDecodeError:
            print(f'Error decoding JSON from file {file_path}.')
        return None

    def execute_api(self, source_currency, exchanged_currencies, valuation_date):
        services_dir = os.path.join(os.getcwd(), 'app', 'json')
        file_path = os.path.join(services_dir, f'{source_currency}_{valuation_date}.json')
        return self.read_json_file(file_path)

    def get_exchange_rate_data(self, source_currency: str, exchanged_currencies: List[str], valuation_date: datetime):
        return self.execute_api(source_currency, exchanged_currencies, valuation_date.strftime('%Y_%m_%d'))

provider = FixerMock('url', 'apikey')
""" --provider_name="fixermock"
```


