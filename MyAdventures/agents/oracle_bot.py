import time
from MyAdventures.mcpi import minecraft
import random
from MyAdventures.agents.Agent import Agent

class OracleBot(Agent):
    def __init__(self, name, mc, responses):
        super().__init__(name, mc)
        self.responses = responses
        self.running = False

    def _run(self, *args):
        while self.running:
            try:
                # Obtener y filtrar eventos con programación funcional
                events = self.mc.events.pollChatPosts()
                questions = list(filter(lambda e: e.message.lower().startswith("oracle:"), events))

                # Procesar cada pregunta
                for event in questions:
                    question = event.message[7:].strip()
                    response = random.choice(self.responses)
                    self.post_to_chat(f"Answer: {response}")

            except Exception as e:
                print(f"Error in OracleBot _run: {e}")
            time.sleep(0.1)

# Example usage
if __name__ == "__main__":
    # Connect to Minecraft
    mc = minecraft.Minecraft.create()
    print("Conexión establecida con el servidor de Minecraft.")

    # Define OracleBot responses
    responses = [
        "Yes.", "No.", "Maybe.", "Ask again later.", "42 is the answer."
    ]

    # Create and start OracleBot
    oracle_bot = OracleBot("OracleBot", mc, responses)
    oracle_bot.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Stopping OracleBot...")
        oracle_bot.stop()
