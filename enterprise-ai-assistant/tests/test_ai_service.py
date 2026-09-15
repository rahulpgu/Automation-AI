import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.ai_service import AIService


class FakeCompletions:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Hello there"))]
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


class AIServiceTests(unittest.TestCase):
    def test_ask_returns_model_response(self):
        fake_client = FakeClient()

        with patch("app.services.ai_service.OpenAI", return_value=fake_client):
            service = AIService()
            response = service.ask("Hello")

        self.assertEqual(response, "Hello there")
        self.assertEqual(fake_client.chat.completions.calls[0]["model"], "openai/gpt-4.1-mini")


if __name__ == "__main__":
    unittest.main()
