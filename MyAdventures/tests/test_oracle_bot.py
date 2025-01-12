import unittest
from unittest.mock import MagicMock
from MyAdventures.agents.oracle_bot import OracleBot
import time


class TestOracleBot(unittest.TestCase):
    def setUp(self):
        """Set up a mock Minecraft instance and an OracleBot instance."""
        self.mock_mc = MagicMock()  # Simula el servidor de Minecraft
        self.responses = ["Yes.", "No.", "Maybe.", "Ask again later.", "42 is the answer."]
        self.bot = OracleBot("OracleBot", self.mock_mc, self.responses)

    def test_start_and_stop(self):
        """Test that the bot starts and stops correctly."""
        self.bot.start()
        self.assertTrue(self.bot.running)
        self.bot.stop()
        self.assertFalse(self.bot.running)

    def test_post_to_chat(self):
        """Test that the bot sends a response to the chat."""
        self.mock_mc.events.pollChatPosts.return_value = [
            MagicMock(message="oracle: What is the meaning of life?")
        ]
        self.bot.post_to_chat = MagicMock()  # Mock para capturar la salida del chat

        self.bot.start()
        time.sleep(0.2)  # Permitir que el bot procese los eventos
        self.bot.stop()

        self.bot.post_to_chat.assert_called()  # Verifica que se llamó a post_to_chat
        response = self.bot.post_to_chat.call_args[0][0]
        self.assertTrue(response.startswith("Answer: "))
        self.assertIn(response[8:], self.responses)  # Verifica que la respuesta sea válida

    def test_no_questions(self):
        """Test that the bot does nothing if no questions are posted."""
        self.mock_mc.events.pollChatPosts.return_value = []  # No hay mensajes
        self.bot.post_to_chat = MagicMock()

        self.bot.start()
        time.sleep(0.2)
        self.bot.stop()

        self.bot.post_to_chat.assert_not_called()  # Verifica que no se enviaron respuestas

    def test_multiple_questions(self):
        """Test that the bot processes multiple questions in a single cycle."""
        # Simula mensajes del jugador con múltiples preguntas
        self.mock_mc.events.pollChatPosts.side_effect = [
            [
                MagicMock(message="oracle: Is the sky blue?"),
                MagicMock(message="oracle: Will it rain tomorrow?")
            ],
            []  # Después de la primera llamada, no hay más eventos
        ]

        # Mock post_to_chat
        self.bot.post_to_chat = MagicMock()

        # Ejecuta el bot por un breve tiempo
        self.bot.start()
        time.sleep(0.15)  # Suficiente tiempo para una iteración
        self.bot.stop()

        # Verifica que se respondieron exactamente 2 preguntas
        self.assertEqual(self.bot.post_to_chat.call_count, 2)

        # Verifica que las respuestas sean válidas
        responses = [call[0][0] for call in self.bot.post_to_chat.call_args_list]
        for response in responses:
            self.assertTrue(response.startswith("Answer: "))
            self.assertIn(response[8:], self.responses)  # Verifica que las respuestas sean válidas

if __name__ == "__main__":
    unittest.main()
