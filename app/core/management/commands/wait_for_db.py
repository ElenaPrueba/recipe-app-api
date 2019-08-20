import time
# Podemos usarlo para hacer que nuestras aplicaciones 'duerman' unos segundos
# entre cada día de la base de verificación

from django.db import connections
# Para comprobar si la bbdd esta disponible desde django para importar
# conexiones

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for the database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
