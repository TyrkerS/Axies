import unittest
from unittest.mock import MagicMock
from MyAdventures.agents.tnt_bot import TNTBot
from MyAdventures.mcpi import block
import time


class TestTNTBot(unittest.TestCase):
    def setUp(self):
        """Set up a mock Minecraft instance and a TNTBot instance."""
        self.mock_mc = MagicMock()  # Simula el servidor de Minecraft
        self.bot = TNTBot("TNTBot", self.mock_mc)

    def test_start_and_stop(self):
        """Test that the bot starts and stops correctly."""
        self.bot.start(0.1)  # Intervalo de 0.1 segundos
        self.assertTrue(self.bot.running)
        self.bot.stop()
        self.assertFalse(self.bot.running)

    def test_deploy_tnt(self):
        """Test that the bot deploys TNT at the correct coordinates."""
        x, y, z = 10, 20, 30
        self.bot.deploy_tnt(x, y, z)
        self.mock_mc.setBlock.assert_called_with(x, y, z, block.TNT.id, 1)
        self.mock_mc.postToChat.assert_called_with("[TNTBot]: TNT deployed at (10, 20, 30)")

    def test_run_generates_positions(self):
        """Test that the bot generates the correct TNT positions."""
        # Mock player position
        self.mock_mc.player.getTilePos.return_value = MagicMock(x=10, y=20, z=30)

        # Mock deploy_tnt to avoid executing real logic
        self.bot.deploy_tnt = MagicMock()

        self.bot.start(0.1)
        time.sleep(0.15)  # Ajusta el tiempo para que solo ejecute una iteración
        self.bot.stop()

        # Verifica solo las primeras posiciones generadas
        expected_positions = [(13, 20, 30), (14, 20, 30), (15, 20, 30)]
        actual_positions = [call[0] for call in self.bot.deploy_tnt.call_args_list[:len(expected_positions)]]
        self.assertEqual(expected_positions, actual_positions)


if __name__ == "__main__":
    unittest.main()