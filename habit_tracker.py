import sqlite3
import datetime
from dateutil.relativedelta import relativedelta


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

    def __init__(self,habit_id, name, periodicity, description, creation_date, current_streak, longest_streak,
                 streak_breaks):
        self.habit_id = habit_id
        self._name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = creation_date
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.streak_breaks = streak_breaks
        self.log = []

    @property
    def name(self):
        """Get the name of the habit."""
        return self._name

    def is_complete(self, date=datetime.datetime.today()):
        """
        Add the date and time of a habit completion.

        :param date: The date and time the habit was completed.
        :return:
        """
        self.log.append(date)

    def calculate_streak(self):
        """Calculate streaks for the habits."""
        diff = relativedelta(self.log[-1],
                             self.creation_date if len(self.log) == 1 else self.log[-2])

        if self.periodicity == "daily":
            if diff.days < 1 or (diff.days == 1 and diff.hours == 0 and diff.minutes == 0):
                self.current_streak += 1
            else:
                self.longest_streak = max(self.current_streak, self.longest_streak)
                self.current_streak = 0
                self.streak_breaks += 1

        elif self.periodicity == "weekly":
            if diff.days < 7 or (diff.days == 7 and diff.hours == 0 and diff.minutes == 0):
                self.current_streak += 1
            else:
                self.longest_streak = max(self.current_streak, self.longest_streak)
                self.current_streak = 0
                self.streak_breaks += 1

        elif self.periodicity == "monthly":
            if diff.months < 1 or (diff.months == 1 and diff.days == 0 and diff.hours == 0 and diff.minutes == 0):
                self.current_streak += 1
            else:
                self.longest_streak = max(self.current_streak, self.longest_streak)
                self.current_streak = 0
                self.streak_breaks += 1

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE habits SET current_streak = ?, longest_streak = ?, streak_breaks = ?"
                        "WHERE habit_id = ?", (self.current_streak, self.longest_streak, self.streak_breaks,
                                               self.habit_id))
            conn.commit()

    def __str__(self):
        """It shows the name, periodicity, creation date, and description if a habit instance is printed."""
        return (f"\n{"Name":13s}: {self.name}\n{"Periodicity":13s}: {self.periodicity}"
                f"\n{"Creation Date":13s}: {self.creation_date}\n{"Description":13s}: {self.description}")


class HabitTracker:
    """
    A class that manages habit classes.

    :ivar list habits: A list containing the defined habits.
    """

    def __init__(self):
        """Initializes an empty list that will contain habits."""
        self.habits = []
        self.load_habits()

    def add_habit(self, name, periodicity, description, creation_date=datetime.date.today(),
                  current_streak=0, longest_streak=0, streak_breaks=0):
        """
        Define and store a habit inside a database, and inside the class.

        :param name: The habit's name.
        :param periodicity: The period in which the habit must be completed.
        :param description: Clear and concise description of the habit's task.
        :param creation_date: The date and time the habit was created.
        :param current_streak: The habits' current streak.
        :param longest_streak: The habits' longest streak.
        :param streak_breaks: The habits' number of streaks broken.
        :return:
        """
        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO habits (name, periodicity, description, creation_date)
                            VALUES (?, ?, ?, ?);""",
                (name, periodicity, description, creation_date.strftime("%Y-%m-%d")))
            habit_id = cur.lastrowid
            conn.commit()

        habit = Habit(habit_id, name, periodicity, description, creation_date, current_streak, longest_streak,
                      streak_breaks)
        self.habits.append(habit)

    def complete_habit(self, name, date=datetime.datetime.today()):
        """
        Mark a chosen habit as completed, adding to its internal log and a database.

        :param name: The habits' name.
        :param date: The date and time the habit was completed.
        :return:
        """
        habit = self.get_habit(name)
        habit.is_complete(date)
        habit.calculate_streak()

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO habits_log (habit_id, date) VALUES (?, ?);",
                        (habit.habit_id, habit.log[-1].strftime("%Y-%m-%d %H-%M-%S")))
            conn.commit()

    def delete_habit(self, name):
        """
        Delete a habit from the database, and inside the class.

        :param str name: Name of the habit to be deleted.
        :return:
        """
        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM habits WHERE habit_id = ?;", (self.get_habit(name).habit_id,))
            cur.execute("DELETE FROM habits_log WHERE habit_id = ?;", (self.get_habit(name).habit_id,))
            conn.commit()

        self.habits = [habit for habit in self.habits if habit.name != name]

    def view_habits(self, periodicity):
        """Returns a string containing habits' names.

        :param str periodicity: Filter the habits' visualization by its periodicity.
        :return: The name of all habits, or the name of habits filtered by its periodicity.
        :rtype: str
        """
        if periodicity == '':
            return ", ".join([habit.name for habit in self.habits])
        else:
            return ", ".join([habit.name for habit in self.habits if habit.periodicity == periodicity])

    def load_habits(self):
        """Load habits and its logs from a database into the class."""
        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS habits(
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                description TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                streak_breaks INTEGER DEFAULT 0);
            """)

            cur.execute("""CREATE TABLE IF NOT EXISTS habits_log(
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE);
            """)

            habits_data = cur.execute("""SELECT habit_id, name, periodicity, description, creation_date, current_streak,
                                        longest_streak, streak_breaks
                                        FROM habits;""").fetchall()
            for habit_id, name, periodicity, description, creation_date, current_streak, longest_streak, \
                    streak_breaks in habits_data:
                habit = Habit(habit_id, name, periodicity, description,
                              datetime.datetime.strptime(creation_date, "%Y-%m-%d").date(),
                              current_streak, longest_streak, streak_breaks)
                self.habits.append(habit)

                log_data = cur.execute("SELECT date FROM habits_log WHERE habit_id = ?;",
                                       (habit_id,)).fetchall()
                for date in log_data:
                    habit.log.append(datetime.datetime.strptime(date[0], "%Y-%m-%d %H-%M-%S"))

            conn.commit()

    def get_habit(self, name):
        """
        Get an instance of a Habit by its name.

        :param str name: Name of the habit.
        :return: An instance of the habit.
        """
        return [habit for habit in self.habits if habit.name == name][0]
