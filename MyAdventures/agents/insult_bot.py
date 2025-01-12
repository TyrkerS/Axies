import random
import time
from MyAdventures.mcpi import minecraft
from MyAdventures.agents.Agent import Agent


class InsultBot(Agent):
    def __init__(self, name, mc, insults):
        super().__init__(name, mc)
        self.insults = insults
        self.interval = 0  # Valor predeterminado del intervalo

    def start(self, interval):
        """Start the bot and set the interval."""
        self.interval = interval  # Almacenar el intervalo
        super().start()  # Llamar al método start de la clase base

    def _run(self):
        while self.running:
            try:
                print(f"{self.name} is running...")  # Depuración
                # Transformar los insultos a mayúsculas usando programación funcional
                transformed_insults = list(map(str.upper, self.insults))
                insult = random.choice(transformed_insults)
                self.post_to_chat(insult)
            except Exception as e:
                print(f"Unexpected error in InsultBot _run: {e}")
            time.sleep(self.interval)
        print(f"{self.name} has stopped.")  # Depuración al salir del bucle


# Example usage
if __name__ == "__main__":
    # Connect to Minecraft
    mc = minecraft.Minecraft.create()
    print("Conexión establecida con el servidor de Minecraft.")

    # Define insults
    insults = [
        "You're as sharp as a marble!",
        "Is your brain a black hole? Nothing escapes!",
        "You have something on your chin... no, the third one down.",
        "You're proof that even evolution can take a coffee break."
    ]

    # Create and start InsultBot
    bot = InsultBot("InsultBot", mc, insults)
    bot.start(10)  # Sends an insult every 10 seconds

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Stopping InsultBot...")
        bot.stop()
