import os

from django.core.management.base import BaseCommand

from app.models import ProviderModel
from mycurrency.constants import PROVIDER_IMPORT_SUCCESS, PROVIDER_IMPORT_FAILURE, CODE_HELP, PROVIDER_HELP, ARGS_ERROR


class Command(BaseCommand):
    help = PROVIDER_HELP

    def add_arguments(self, parser):
        parser.add_argument('--code', type=str, help=CODE_HELP)
        parser.add_argument('--provider_name', type=str)

    def handle(self, *args, **options):
        code = options.get('code')
        provider_name = options.get('provider_name')
        if not code or not provider_name:
            self.stdout.write(self.style.ERROR(ARGS_ERROR))
            return
        filename = f'provider_gen_{abs(hash(code))}.py'
        services_dir = os.path.join(os.getcwd(), 'app', 'services')
        file_path = os.path.join(services_dir, filename)

        try:
            with open(file_path, 'w') as f:
                f.write(code)
        except OSError as e:
            print(e)
            self.stdout.write(self.style.ERROR(PROVIDER_IMPORT_FAILURE))
            return

        module_name = os.path.splitext(os.path.basename(file_path))[0]
        module_dir = os.path.dirname(file_path)
        ProviderModel.objects.create(name=provider_name, module_dir=module_dir, module_name=module_name)

        self.stdout.write(self.style.SUCCESS(PROVIDER_IMPORT_SUCCESS))
