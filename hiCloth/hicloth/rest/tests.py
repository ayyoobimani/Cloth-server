from django.test import SimpleTestCase
from django.test import Client
import json
from models import Image


class GetImageTests(SimpleTestCase):
    testClient = Client()
    testResponse = testClient.get('/rest/images/')
    testStatus = testResponse.status_code
    numberOfDictionaryKeys = 5

    def test_is_status_equal_to_200(self):
        self.assertEqual(self.testStatus, 200)

    def test_check_number_of_items_in_getImage_URL(self):
        self.assertEqual(len(json.loads(self.testResponse.content)["images"][0].keys()),
                         self.numberOfDictionaryKeys)