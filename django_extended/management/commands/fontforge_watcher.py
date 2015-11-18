from django.conf import settings
from django.utils.module_loading import import_module
from django.core.management.base import BaseCommand
from ...contrib.fontforge import Watcher

class Command(BaseCommand):
    args = ''
    help = 'ex: ./manage.py fontforge_watcher'

    def handle(self, *args, **options):

        watcher = Watcher(command=self)
        watcher.watch()