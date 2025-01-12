import unittest
from unittest.mock import MagicMock, patch
from MyAdventures.agents.chat_bot import ChatBot
import time


class TestChatBot(unittest.TestCase):
    def setUp(self):
        """Set up a mock Minecraft instance and a ChatBot instance."""
        self.mock_mc = MagicMock()  # Simula el servidor de Minecraft
        self.bot = ChatBot("ChatBot", self.mock_mc)

    @patch("MyAdventures.agents.chat_bot.ChatBot.get_gemini_response")
    def test_get_gemini_response(self, mock_gemini):
        """Test that the bot gets a response from the Gemini API."""
        # Simula una respuesta de la API de Google Gemini
        mock_gemini.return_value = "> This is a test response."

        # Llama al método
        response = self.bot.get_gemini_response("Test prompt")

        # Verifica que la respuesta sea la esperada
        self.assertEqual(response, "> This is a test response.")

    def test_post_to_chat(self):
        """Test that the bot sends messages to the Minecraft chat."""
        self.bot.post_to_chat = MagicMock()  # Mock para capturar las salidas al chat
        self.bot.post_to_chat("Test message")
        self.bot.post_to_chat.assert_called_with("Test message")

    @patch("MyAdventures.agents.chat_bot.ChatBot.get_gemini_response")
    def test_run_process_message(self, mock_gemini):
        """Test that the bot processes messages and calls Gemini."""
        # Mockea eventos del chat
        self.mock_mc.events.pollChatPosts.side_effect = [
            [MagicMock(message="chatbot: Hello!")],  # Devuelve un solo mensaje en la primera iteración
            []  # Luego, no devuelve más mensajes
        ]

        # Mockea el método get_gemini_response
        mock_gemini.return_value = "> Hello, user!"

        # Mockea post_to_chat para capturar las salidas
        self.bot.post_to_chat = MagicMock()

        # Ejecuta el bot por un ciclo breve
        self.bot.start()
        time.sleep(0.1)  # Permite que el bot procese el mensaje
        self.bot.stop()

        # Verifica que el bot pensó y respondió
        self.bot.post_to_chat.assert_any_call("Thinking...")
        self.bot.post_to_chat.assert_any_call("> Hello, user!")
        mock_gemini.assert_called_once_with("Hello!")  # Verifica que se llama una sola vez

    def test_no_messages(self):
        """Test that the bot does nothing if no relevant messages are posted."""
        self.mock_mc.events.pollChatPosts.return_value = []  # No hay mensajes
        self.bot.post_to_chat = MagicMock()

        # Ejecuta el bot
        self.bot.start()
        time.sleep(0.2)
        self.bot.stop()

        # Verifica que no se enviaron mensajes
        self.bot.post_to_chat.assert_not_called()


if __name__ == "__main__":
    unittest.main()
