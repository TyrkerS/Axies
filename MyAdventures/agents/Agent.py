from threading import Thread

class Agent:
    def __init__(self, name, mc):
        self.name = name
        self.mc = mc
        self.running = False
        self.thread = None

    def start(self, *args):
        """Start the bot's main functionality."""
        if not self.running:
            self.running = True
            self.thread = Thread(target=self._run, args=args, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the bot and wait for the thread to terminate."""
        if self.running:
            print(f"Stopping {self.name}...")  # Depuración
            self.running = False
            if self.thread:
                self.thread.join()  # Espera a que el hilo termine
                self.thread = None
            print(f"{self.name} stopped.")  # Depuración

    def _run(self, *args):
        """This method should be implemented by subclasses."""
        raise NotImplementedError

    def post_to_chat(self, message):
        """Send a message to the Minecraft chat."""
        self.mc.postToChat(f"[{self.name}]: {message}")