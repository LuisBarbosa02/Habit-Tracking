import sqlite3
import datetime


class Habit:
    """
    A class storing information about habits.

    :ivar int habit_id: A unique habit id.
    :ivar str _name: The habits' name.
    :ivar str periodicity: Period in which the habit must be completed.
    :ivar str description: Clear and concise description of the habits' task.
    :ivar datetime.date creation_date: The date the habit was created.
    :ivar int current_streak: The habits' current completions in a row.
    :ivar int longest_streak: Habits' longest completions in a row.
    :ivar int streak_breaks: Number of times this habit was "broken".
    :ivar list log: A list containing the date and time the habit was completed.
    """

    def __init__(self,habit_id, name, periodicity, description, creation_date):
        """
        Initializes a habit with name, periodicity, and description.

        :param str name: The habits' name.
        :param str periodicity: Period in which the habit must be completed.
        :param str description: lear and concise description of the habits' task.
        :param datetime.date creation_date: The date in which the habit was created.
        :param int habit_id: The habits' id.
        """
        self.habit_id = habit_id
        self._name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = creation_date
        self.current_streak = 0
        self.longest_streak = 0
        self.streak_breaks = 0
        self.log = []

    @property
    def name(self):
        """Get the name of the habit."""
        return self._name


class HabitTracker:
    """
    A class that manages habit classes.

    :ivar list habits: A list containing the defined habits.
    """

    def __init__(self):
        """Initializes an empty list that will contain habits."""
        self.habits = []
        self.load_habits()

    def add_habit(self, name, periodicity, description):
        """
        Define and store a habit inside a database, and inside the class.

        :param name: The habit's name.
        :param periodicity: The period in which the habit must be completed.
        :param description: Clear and concise description of the habit's task.
        :return:
        """
        creation_date = datetime.date.today()

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO habits (name, periodicity, description, creation_date)
                            VALUES (?, ?, ?, ?);""",
                (name, periodicity, description, creation_date.strftime("%Y-%m-%d")))
            habit_id = cur.lastrowid
            conn.commit()

        habit = Habit(habit_id, name, periodicity, description, creation_date)
        self.habits.append(habit)

    def delete_habit(self, name):
        """Delete a habit from the database, and inside the class."""
        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM habits WHERE habit_id = ?;", (self._get_habit(name).habit_id,))
            conn.commit()

        self.habits = [habit for habit in self.habits if habit.name != name]

    def view_habits(self, periodicity):
        """Returns a string containing all habits' names."""
        if periodicity == '':
            return ", ".join([habit.name for habit in self.habits])
        else:
            return ", ".join([habit.name for habit in self.habits if habit.periodicity == periodicity])

    def load_habits(self):
        """Load habits from a database into the class."""
        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS habits(
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                description TEXT NOT NULL,
                creation_date TEXT NOT NULL);
            """)

            habits_data = cur.execute("""SELECT habit_id, name, periodicity, description, creation_date
                                        FROM habits;""").fetchall()
            for habit_id, name, periodicity, description, creation_date in habits_data:
                self.habits.append(Habit(habit_id, name, periodicity, description,
                                         datetime.datetime.strptime(creation_date, "%Y-%m-%d").today()))

            conn.commit()

    def _get_habit(self, name):
        """Get an instance of a Habit by its name."""
        return [habit for habit in self.habits if habit.name == name][0]
