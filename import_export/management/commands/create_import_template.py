import sys
from pathlib import Path
from django.apps import apps
from django.core.management.base import BaseCommand
from import_export.services.import_template_builder import ImportTemplateBuilder


class Command(BaseCommand):
    help = 'Export a model import template for all managed models in the given app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='create import template for this app')

    def handle(self, *args, **options):
        app_name = options['app_name']
        try:
            apps.get_app_config(app_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(
                f"LookupError: App named '{app_name}' not found in Django project '{__package__ or __name__}'"
            ))
            sys.exit(1)

        # Create template directory
        template_dir = Path(app_name) / 'media' / 'import_export' / 'templates'
        template_dir.mkdir(parents=True, exist_ok=True)
        # Create directory for completed import templates
        import_dir = Path(app_name) / "media" / "import_export" / "import_files"
        import_dir.mkdir(parents=True, exist_ok=True)

        output_file = template_dir / f"{app_name}_import_file.xlsx"

        if output_file.exists():
            output_file.unlink()

        # Build the workbook
        builder = ImportTemplateBuilder(app_name)
        workbook = builder.build_workbook()
        workbook.save(output_file)

        self.stdout.write(self.style.SUCCESS(f'✔ Import template saved to {output_file}'))
