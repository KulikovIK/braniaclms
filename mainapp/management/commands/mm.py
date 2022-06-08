from django.core.management .base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = (
        "This command using call 'makemessages' whith flags:\n"
        "--licale=ru --no-location and --ignore=venv"
    )

    def handle(self, *args, **options):
        call_command("makemessages", "--locale=ru", "--ignore=venv", "--no-location")