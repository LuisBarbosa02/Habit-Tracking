class Habit:
    def __init__(self, name, periodicity, description):
        self.id = None
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = None
        self.current_streak = 0
        self.longest_streak = 0
        self.streak_breaks = 0
        self.log = []


class HabitTracker:
    def __init__(self):
        self.habits = []