import unittest
from micro_service import app
from flask import json

class TestReportarDependencias(unittest.TestCase):

    def setUp(self):
        # Configurar la aplicación en modo de prueba
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_reportar_dependencias_formato_incorrecto(self):
        response = self.client.post('/api/reportar', json={"dato_incorrecto": "valor"})
        self.assertEqual(response.status_code, 400)

    def test_reportar_dependencias_sin_dependencias(self):
        # Enviar un JSON sin la clave 'dependencias'
        response = self.client.post('/api/reportar', json={"repositorio": "mi-repositorio"})
        self.assertEqual(response.status_code, 400)

    def test_reportar_dependencias_correcto(self):
        # Enviar un JSON correcto
        data = {
            "repositorio": "mi-repositorio",
            "dependencias": [
                {"groupId": "com.ejemplo", "artifactId": "mi-artefacto", "version": "1.0.0"}
            ]
        }
        response = self.client.post('/api/reportar', json=data)
        self.assertEqual(response.status_code, 200)

    # Agrega más pruebas según sea necesario

if __name__ == '__main__':
    unittest.main()
