from pathlib import Path
from django.core.management.base import BaseCommand
from import_export.services.import_workbook import ImportWorkbook

class Command(BaseCommand):
    help = 'Imports data from an Excel workbook into Django models.'

    def add_arguments(self, parser):
        parser.add_argument('app_label', type=str, help='Specify the app')
        parser.add_argument('--model', type=str, help='Optional: only import data for a specific model within the app')
        # model will fail if relies on choice_maps picked pu from earlier models, consider checking if choice map exists
        # before processing and refactoring with a patch to check and create if necessary/
    def handle(self, *args, **options):

        model = options.get('model')
        app_label = options.get('app_label')

        base_dir = Path(app_label) / "media" / "import_export" / "import_files"
        full_path = base_dir / f"{app_label}_import_file.xlsx"

        if Path(full_path).is_file():
            try:
                importer = ImportWorkbook(full_path, app_label)
                result = importer.import_workbook()
                if result["successes"] and result["failures"]:
                    self.stdout.write(self.style.SUCCESS("✔ Import Successes:"))
                    for line in result["successes"]:
                        self.stdout.write(self.style.SUCCESS(f"  - {line}"))
                    self.stdout.write(self.style.WARNING("⚠ Import Failures:"))
                    for line in result["failures"]:
                        self.stdout.write(self.style.WARNING(f"  - {line}"))
                elif result["successes"]:
                    self.stdout.write(self.style.SUCCESS("✔ Import Successes:"))
                    for line in result["successes"]:
                        self.stdout.write(self.style.SUCCESS(f"  - {line}"))
                else:
                    self.stdout.write(self.style.ERROR("⚠ Import Failed:"))
                    for line in result["failures"]:
                        self.stdout.write(self.style.ERROR(f"  - {line}"))
            except:
                self.stdout.write(self.style.ERROR("⚠ Import Failed:"))

        else:
            self.stdout.write(self.style.ERROR(f'File does not exist at {full_path}'))
