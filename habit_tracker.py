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

    def is_complete(self):
        """Add the date and time of a habit completion."""
        self.log.append(datetime.datetime.today())

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

    def complete_habit(self, name):
        """
        Mark a chosen habit as completed, adding to its internal log and a database.

        :param name: The habits' name.
        :return:
        """
        habit = self.get_habit(name)
        habit.is_complete()

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO habits_log (habit_id, date) VALUES (?, ?)",
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
                creation_date TEXT NOT NULL);
            """)

            cur.execute("""CREATE TABLE IF NOT EXISTS habits_log(
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE);
            """)

            habits_data = cur.execute("""SELECT habit_id, name, periodicity, description, creation_date
                                        FROM habits;""").fetchall()
            for habit_id, name, periodicity, description, creation_date in habits_data:
                habit = Habit(habit_id, name, periodicity, description,
                              datetime.datetime.strptime(creation_date, "%Y-%m-%d").date())
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
