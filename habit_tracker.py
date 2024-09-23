class Habit:
    """
    A class storing information about habits.

    :ivar int id: A unique habit id.
    :ivar str _name: The habit`s name.
    :ivar str periodicity: Period in which the habit must be completed.
    :ivar str description: Clear and concise description of the habit`s task.
    :ivar datetime.datetime creation_date: The date the habit was created.
    :ivar int current_streak: The habit`s current completions in a row.
    :ivar int longest_streak: Habit`s longest completions in a row.
    :ivar int streak_breaks: Number of times this habit was "broken".
    :ivar list log: A list containing the date and time the habit was completed.
    """

    def __init__(self, name, periodicity, description):
        """
        Initializes a habit with name, periodicity, and description.

        :param str name: The habit`s name.
        :param str periodicity: Period in which the habit must be completed.
        :param str description: lear and concise description of the habit`s task.
        """
        self.id = None
        self._name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = None
        self.current_streak = 0
        self.longest_streak = 0
        self.streak_breaks = 0
        self.log = []

    @property
    def name(self):
        return self._name


class HabitTracker:
    """
    A class that manages habit classes.

    :ivar list habits: A list containing the defined habits.
    """

    def __init__(self):
        """Initializes an empty list that will contain habits."""
        self.habits = []

    def add_habit(self, name, periodicity, description):
        """
        Define and store a habit.

        :param name: The habit`s name.
        :param periodicity: The period in which the habit must be completed.
        :param description: Clear and concise description of the habit`s task.
        :return:
        """
        habit = Habit(name, periodicity, description)
        self.habits.append(habit)

    def view_habits(self):
        return ", ".join([habit.name for habit in self.habits])
