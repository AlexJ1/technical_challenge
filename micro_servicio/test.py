import unittest
from micro_service import app
from flask import json


class TestReportarDependencias(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_reportar_dependencias_formato_incorrecto(self):
        response = self.client.post('/api/reportar', json={"dato_incorrecto": "valor"})
        self.assertEqual(response.status_code, 400)

    def test_reportar_dependencias_sin_dependencias(self):
        # Envia POST sin dependencias
        response = self.client.post('/api/reportar', json={"repositorio": "mi-repositorio"})
        self.assertEqual(response.status_code, 400)

    def test_reportar_dependencias_correcto(self):
        # Envia POST correctamente mapeado
        data = {
            "repositorio": "TEST-REPO",
            "dependencias": [
                {"groupId": "SPRING FRAMEWORK", 
                 "COM SPRING": "ARTEFACTO",
                 "version": "1.0.0"
                 }
            ]
        }
        response = self.client.post('/api/reportar', json=data)
        self.assertEqual(response.status_code, 200)

    def test_consulta_get_status(self):
        # Consulta GET
        response = self.client.get('/api/repositorios')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
