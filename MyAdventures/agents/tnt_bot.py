import time
from MyAdventures.mcpi import minecraft, block
from MyAdventures.agents.Agent import Agent

class TNTBot(Agent):
    def __init__(self, name, mc):
        super().__init__(name, mc)
        self.interval = 0  # Intervalo predeterminado

    def deploy_tnt(self, x, y, z):
        """Place TNT at the specified coordinates."""
        self.mc.setBlock(x, y, z, block.TNT.id, 1)
        self.post_to_chat(f"TNT deployed at ({x}, {y}, {z})")

    def deploy_fire(self, x, y, z):
        """Place fire at the specified coordinates to ignite TNT."""
        self.mc.setBlock(x, y, z, block.FIRE.id)  # Coloca fuego encima de la TNT
        self.post_to_chat(f"Fire placed at ({x}, {y}, {z})")

    def start(self, interval):
        """Start the bot and set the interval."""
        self.interval = interval
        super().start()

    def _run(self):
        while self.running:
            try:
                player_pos = self.mc.player.getTilePos()
                # Generar posiciones usando map
                tnt_positions = list(
                    map(lambda offset: (player_pos.x + offset, player_pos.y, player_pos.z), range(3, 6))
                )
                for pos in tnt_positions:
                    self.deploy_tnt(*pos)
                    self.deploy_fire(pos[0], pos[1] + 1, pos[2])
            except Exception as e:
                print(f"Unexpected error in TNTBot _run: {e}")
            time.sleep(self.interval)

# Example usage
if __name__ == "__main__":
    # Connect to Minecraft
    mc = minecraft.Minecraft.create()
    print("Conexión establecida con el servidor de Minecraft.")

    # Create and start TNTBot
    tnt_bot = TNTBot("TNTBot", mc)
    tnt_bot.start(10)  # Deploy TNT every 10 seconds

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Stopping TNTBot...")
        tnt_bot.stop()