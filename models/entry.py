class Entry():
    def __init__(self, id, concept, entry, mood_id, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.moodId = mood_id
        self.date = date
        self.mood = None
        self.tags = None
