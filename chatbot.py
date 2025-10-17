import random

class MiniChatBot:
    def __init__(self):
        # Einfaches Beispiel, kann beliebig erweitert werden
        self.train_data = [
            "What's your favorite movie?",
            "Do you like cats or dogs?",
            "What's a fun fact about you?",
            "Have you traveled anywhere recently?",
            "What's your favorite game?"
        ]

    def get_response(self, message: str) -> str:
        # Simpler Bot: Antwort entweder zufällig aus Liste oder Echo
        if "hello" in message.lower():
            return "Hi there! 👋"
        return random.choice(self.train_data)
import random

# Sample responses
responses = [
    "Hey there! How’s everything going today?",
    "Haha, that’s actually funny 😄",
    "I totally get what you mean.",
    "That’s a good question… let me think 🤔",
    "Interesting point — never thought about it like that.",
    "Yeah, it’s been a long day for me too.",
    "What are you up to right now?",
    "I like how you put that!",
    "Tell me more about that.",
    "Same here, honestly.",
    "That’s kinda true tho 😂",
    "Oh really? That’s cool!",
    "Do you play any games lately?",
    "I feel that 😅",
    "What’s your favorite movie or show?",
    "That reminds me of something funny actually.",
    "Lmao yeah that happens a lot",
    "What time is it for you right now?",
    "Do you usually stay up late?",
    "That’s awesome!",
]

def get_response(message_content):
    # Hier könntest du auch smartere Logik einbauen
    return random.choice(responses)
