# La gestión de "command" va a ser una ayuda de los comandos que nos permite
# esperar a que la bbdd esté disponible antes de continuar ejecutando otros
# comandos

# Vamos a utilizarlo en el docker-compose cuando iniciemos nuestra app Django

# La razón por la que necesitamos este comando es porque a veces, cuando se
# usa Postgres con Docker-compose en una aplicación de Django, a veces django
# no se inicia debido a un error en la base de datos.

# Esto parece ser porque una vez empezados los servicios de postgres, hubo
# algunas instalaciones que necesitaban estar hechas antes de que esté listo
# para aceptar conexiones

# Esto significa es que una aplicación Django intentará conectarse a nuestra
# base de datos antes de que la base de datos esté lista y por lo tanto fallará
# con una excepción.

# Agregamos este comando auxiliar que podemos poner delante de todos los
# comandos que ejecutamos en docker-compiles y eso asegurará que una base de
# datos esté activa y lista para aceptar conexiones.

# Mocking
# Área avanzada de pruebas
# Mocking es cuando sobreescribes o cambias el comportamiento de las
# dependencias del código que estás probando

# Lo usamos para evitar efectos involuntarios y aislar piezas específicas de
# código que estamos probando

from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.retrun_value = True
            call_command('wait_for_db')  # El comando es wait_for_db
            self.assertEqual(gi.call_count, 1)  # call_count con mock objects

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # Comprueba si la conexión en cuestión genera el error operativo
        # Y si genera el error operativo, esperará un segundo y luego volverá
        # a intentarlo.

        # Para quitar el retraso
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
