from textblob import TextBlob

class EmotionEngine:
    def __init__(self):
        self.mood = "focused"
        self.energy = 80
        self.curiosity = 90
        self.mood_colors = {
            "happy": "#00ff88",
            "focused": "#00d4ff",
            "agitated": "#ff4444",
            "thoughtful": "#aa88ff",
            "empathetic": "#ff88aa"
        }

    def update_emotion(self, message):
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            self.mood = "happy"
        elif polarity < -0.3:
            self.mood = "agitated"
        elif "sad" in message.lower() or "ked" in message.lower():
            self.mood = "empathetic"
        else:
            self.mood = "focused"

    def get_state(self):
        return {
            'mood': self.mood,
            'energy': self.energy,
            'curiosity': self.curiosity,
            'color': self.mood_colors.get(self.mood, '#00d4ff')
        }