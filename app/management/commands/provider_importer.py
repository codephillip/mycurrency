import os

from django.core.management.base import BaseCommand

from app.models import ProviderModel


class Command(BaseCommand):
    help = 'Imports new provider directly without reloading the app'

    def add_arguments(self, parser):
        parser.add_argument('--code', type=str, help='Provider code to import')
        parser.add_argument('--provider_name', type=str, help='Provider name')

    def handle(self, *args, **options):
        code = options.get('code')
        provider_name = options.get('provider_name')
        if not code or not provider_name:
            self.stdout.write(self.style.ERROR('Arguments not provided'))
            return
        filename = f'provider_gen_{abs(hash(code))}.py'
        services_dir = os.path.join(os.getcwd(), 'app', 'services')
        file_path = os.path.join(services_dir, filename)

        try:
            with open(file_path, 'w') as f:
                f.write(code)
        except OSError as e:
            print(e)
            self.stdout.write(self.style.ERROR('Provider import failed'))
            return

        module_name = os.path.splitext(os.path.basename(file_path))[0]
        module_dir = os.path.dirname(file_path)
        ProviderModel.objects.create(name=provider_name, module_dir=module_dir, module_name=module_name)

        self.stdout.write(self.style.SUCCESS('Successfully imported provider'))
