from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient
import json
from backend.app import app
from api.database import init_models


class AuthTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        pass

    async def test_register_user(self):
        await init_models()

        request_payload = {
              "name": "string",
              "address": "string",
              "email": "user@example.com",
              "status": "CON",
              "password": "string"
            }
        response_payload = {
              "name": "string",
              "address": "string",
              "email": "user@example.com",
              "status": "CON",
              "id": 1,
              "use_email_notification": True
            }
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post('/auth/register', content=json.dumps(request_payload))
            response_json = response.json()
            response_json.pop('password')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response_payload, response_json)

