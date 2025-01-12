import unittest
from unittest.mock import MagicMock
from MyAdventures.agents.Agent import Agent
from unittest.mock import patch

class TestAgent(unittest.TestCase):
    def setUp(self):
        """Set up a mock Minecraft instance and an Agent instance."""
        self.mock_mc = MagicMock()  # Simula el servidor de Minecraft
        self.agent = Agent("TestAgent", self.mock_mc)

    def test_start_and_stop(self):
        """Test that the agent starts and stops correctly."""
        with patch.object(self.agent, '_run', return_value=None):  # Mock _run para que no haga nada
            # Verifica que el agente comience
            self.agent.start()
            self.assertTrue(self.agent.running)
            self.assertIsNotNone(self.agent.thread)  # Verifica que el hilo fue creado

            # Verifica que el agente se detenga
            self.agent.stop()
            self.assertFalse(self.agent.running)
            self.assertIsNone(self.agent.thread)  # Verifica que el hilo fue eliminado

    def test_post_to_chat(self):
        """Test that the agent sends messages to the Minecraft chat."""
        message = "Hello, Minecraft!"
        self.agent.post_to_chat(message)
        # Verifica que el método `postToChat` fue llamado correctamente
        self.mock_mc.postToChat.assert_called_with("[TestAgent]: Hello, Minecraft!")

    def test_run_raises_not_implemented_error(self):
        """Test that _run raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.agent._run()  # Llama directamente a _run para verificar que lanza el error

if __name__ == "__main__":
    unittest.main()