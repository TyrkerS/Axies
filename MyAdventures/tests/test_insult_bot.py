import unittest
from unittest.mock import MagicMock
from MyAdventures.agents.insult_bot import InsultBot
import time


class TestInsultBot(unittest.TestCase):
    def setUp(self):
        """Set up a mock Minecraft instance and an InsultBot instance."""
        self.mock_mc = MagicMock()  # Simula el servidor de Minecraft
        self.insults = [
            "You're as sharp as a marble!",
            "Is your brain a black hole?",
            "You have something on your chin... no, the third one down.",
            "You're proof that even evolution can take a coffee break."
        ]
        self.bot = InsultBot("InsultBot", self.mock_mc, self.insults)

    def test_start_and_stop(self):
        """Test that the bot starts and stops correctly."""
        self.bot.start(0.1)  # Intervalo de 0.1 segundos
        self.assertTrue(self.bot.running)
        self.bot.stop()
        self.assertFalse(self.bot.running)

    def test_post_to_chat(self):
        """Test that the bot sends insults to the chat."""
        self.bot.post_to_chat = MagicMock()  # Mock post_to_chat para verificar llamadas
        self.bot.start(0.1)  # Arranca el bot con intervalo pequeño
        time.sleep(0.2)  # Deja que el bot envíe al menos un insulto
        self.bot.stop()
        self.bot.post_to_chat.assert_called()  # Verifica que se llamó post_to_chat

    def test_transformed_insults(self):
        """Test that the insults are transformed correctly to uppercase."""
        self.bot.post_to_chat = MagicMock()
        self.bot.start(0.1)
        time.sleep(0.2)
        self.bot.stop()

        # Asegúrate de que se envían insultos en mayúsculas
        for call in self.bot.post_to_chat.call_args_list:
            insult = call[0][0]  # Primer argumento de la llamada
            self.assertIn(insult, map(str.upper, self.insults))


if __name__ == "__main__":
    unittest.main()

