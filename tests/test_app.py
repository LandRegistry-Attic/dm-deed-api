from application import app
from application.deed.model import Deed
from tests.helper import DeedHelper
from flask.ext.api import status
import unittest
import json


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile("config.py")
        self.app = app.test_client()

    def test_health(self):
        self.assertEqual((self.app.get('/health')).status, '200 OK')

    def test_deed(self):
        self.assertEqual((self.app.get('/deed')).status,
                         '301 MOVED PERMANENTLY')

    def test_model(self):
        test_deed = Deed()
        test_token = test_deed.generate_token()
        self.assertTrue(len(test_token) == 6)

    def test_create(self):
        payload = json.dumps(DeedHelper._json_doc)
        response = self.app.post('/deed/', data=payload,
                                 headers={"Content-Type": "application/json"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
