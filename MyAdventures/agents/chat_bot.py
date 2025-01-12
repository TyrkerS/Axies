import time
import google.generativeai as genai
import textwrap
from MyAdventures.agents.Agent import Agent
from MyAdventures.mcpi import minecraft

# Configuración de la API Key
GOOGLE_API_KEY = "AIzaSyDMur7u2uhnNE9awl7MJ2tiZvO2CquWF6k"
genai.configure(api_key=GOOGLE_API_KEY)

# Función para formatear texto (opcional)
def to_markdown(text):
    """Formatea texto con indentación de Markdown."""
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

class ChatBot(Agent):
    def __init__(self, name, mc):
        super().__init__(name, mc)
        self.model = genai.GenerativeModel("gemini-pro")  # Cambia "gemini-pro" si necesitas otro modelo

    def _run(self, *args):
        while self.running:
            try:
                # Escuchar mensajes del chat
                events = self.mc.events.pollChatPosts()
                for event in events:
                    message = event.message
                    print(f"Received message: {message}")  # Depuración
                    if message.lower().startswith("chatbot:"):
                        user_input = message[8:].strip()  # Obtener el mensaje del usuario
                        print(f"User input: {user_input}")  # Depuración
                        self.post_to_chat("Thinking...")
                        response = self.get_gemini_response(user_input)
                        self.post_to_chat(response)
                        print(f"Posted to chat: {response}")  # Depuración

            except Exception as e:
                print(f"Error in ChatBot _run: {e}")
            time.sleep(0.01)

    def get_gemini_response(self, prompt):
        """Enviar una solicitud a Google Gemini y obtener la respuesta."""
        try:
            print(f"Sending prompt to Google Gemini: {prompt}")  # Depuración
            response = self.model.generate_content(prompt)
            formatted_response = to_markdown(response.text)
            print(f"Response from Gemini: {formatted_response}")  # Depuración
            return formatted_response
        except Exception as e:
            print(f"Unexpected error with Gemini: {e}")
            return "An error occurred while processing the request."

# Bloque de testeo directo
if __name__ == "__main__":
    # Conectar a Minecraft
    mc = minecraft.Minecraft.create()
    print("Conexión establecida con el servidor de Minecraft.")

    # Crear y ejecutar ChatBot
    bot = ChatBot("ChatBot", mc)
    bot.start()  # Iniciar el bot

    try:
        while True:
            time.sleep(1)  # Mantener el hilo principal activo
    except KeyboardInterrupt:
        print("Stopping ChatBot...")
        bot.stop()