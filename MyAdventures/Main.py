from MyAdventures.mcpi import minecraft
from MyAdventures.agents.oracle_bot import OracleBot
from MyAdventures.agents.insult_bot import InsultBot
from MyAdventures.agents.chat_bot import ChatBot
from MyAdventures.agents.tnt_bot import TNTBot
import time
# Connect to Minecraft
mc = minecraft.Minecraft.create()

# Verificar conexión con el servidor
if mc.conn:
    print("Conexión establecida con el servidor de Minecraft.")
else:
    print("Error: No se pudo establecer la conexión con el servidor de Minecraft.")

# Define bots
responses = ["Yes.", "No.", "Maybe.", "Ask again later.", "42 is the answer."]
insults = [
    "You're as sharp as a marble!",
    "Is your brain a black hole? Nothing escapes!",
    "You have something on your chin... no, the third one down.",
    "You're proof that even evolution can take a coffee break."
]

oracle_bot = OracleBot("OracleBot", mc, responses)
insult_bot = InsultBot("InsultBot", mc, insults)
tnt_bot = TNTBot("TNTBot", mc)
chat_bot = ChatBot("ChatBot", mc)

# Store bot states
bots = {
    "oraclebot": oracle_bot,
    "insultbot": insult_bot,
    "tntbot": tnt_bot,
    "chatbot": chat_bot
}

# Post information about commands
mc.postToChat("Available bots: OracleBot, InsultBot, TNTBot")
mc.postToChat("Type 'start <bot_name>' to activate a bot.")
mc.postToChat("Type 'stop <bot_name>' to deactivate a bot.")

# Clear events to avoid residual issues
mc.events.clearAll()

# Main loop to listen for commands
try:
    while True:
        events = mc.events.pollChatPosts()
        for event in events:
            message = event.message.strip().lower()
            if message.startswith("start"):
                bot_name = message.split(" ")[1]
                if bot_name in bots:
                    if not bots[bot_name].running:
                        print(f"Starting {bot_name}...")  # Depuración
                        mc.events.clearAll()  # Limpia eventos antes de iniciar el bot
                        if bot_name == "tntbot":
                            bots[bot_name].start(5)  # Intervalo de 5 segundos para TNTBot
                        elif bot_name == "insultbot":
                            bots[bot_name].start(10)  # Intervalo de 10 segundos para InsultBot
                        else:
                            bots[bot_name].start()  # Otros bots no necesitan argumentos
                        mc.postToChat(f"{bot_name.capitalize()} activated.")
                    else:
                        mc.postToChat(f"{bot_name.capitalize()} is already running.")
                else:
                    mc.postToChat(f"Bot '{bot_name}' not found.")
            elif message.startswith("stop"):
                bot_name = message.split(" ")[1]
                if bot_name in bots:
                    if bots[bot_name].running:
                        print(f"Attempting to stop {bot_name}...")  # Depuración
                        bots[bot_name].stop()
                        mc.postToChat(f"{bot_name.capitalize()} deactivated.")
                        print(f"{bot_name.capitalize()} successfully stopped.")  # Depuración
                    else:
                        mc.postToChat(f"{bot_name.capitalize()} is not running.")
                        print(f"{bot_name.capitalize()} was not running.")  # Depuración
                else:
                    mc.postToChat(f"Bot '{bot_name}' not found.")
        time.sleep(0.2)  # Reducir la frecuencia del bucle principal
except KeyboardInterrupt:
    print("Stopping all bots...")
    for bot in bots.values():
        bot.stop()