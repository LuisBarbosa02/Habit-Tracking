import pytest
from ..habit_tracker import Habit, HabitTracker
import sqlite3
import datetime


@pytest.fixture
def tracker():
    return HabitTracker()


class TestHabitTracker:
    def test_add_habit(self, tracker):
        num_habits = len(tracker.habits)
        tracker.add_habit("Test", "daily", "Simple test.")
        added_habit = tracker.habits[-1]
        errors = []

        if not len(tracker.habits) == num_habits + 1:
            errors.append("Anything was stored.")
        if not isinstance(added_habit, Habit):
            errors.append("Something else than a Habit was stored.")

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("""SELECT habit_id, name, description FROM habits
                            WHERE habit_id = ?;""", (tracker.habits[-1].habit_id,))
            added_row = cur.fetchone()
            if not added_row:
                errors.append("Data was not stored in database.")
            if not all([added_habit.habit_id == added_row[0], added_habit.name == added_row[1],
                    added_habit.description == added_row[2]]):
                errors.append("That is not the habit supposed to be added.")

        assert not errors, "\n{}".format("\n".join(errors))

    def test_get_habit(self, tracker):
        habit = tracker.get_habit("Test")
        assert habit.habit_id == [habit.habit_id for habit in tracker.habits if habit.name == "Test"][0]

    def test_complete_habit(self, tracker):
        habit = tracker.get_habit("Test")
        num_log = len(habit.log)
        tracker.complete_habit("Test")
        errors = []

        if len(habit.log) != num_log + 1:
            errors.append("Nothing was added to the log.")
        if not isinstance(habit.log[-1], datetime.datetime):
            errors.append("The log added was not a date and time.")

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM habits_log ORDER BY log_id DESC LIMIT 1;")

            try:
                _, habit_id, date = cur.fetchone()

                if habit_id != habit.habit_id:
                    errors.append("This log is not referencing the right habit.")
                if not isinstance(datetime.datetime.strptime(date, "%Y-%m-%d %H-%M-%S"), datetime.datetime):
                    errors.append("This log did not retrieve a date and time.")
            except ValueError:
                errors.append("No log was added to the database table.")

        assert not errors, "\n".join(errors)

    def test_load_habits(self, tracker):
        assert all(isinstance(habit, Habit) for habit in tracker.habits)

    def test_delete_habit(self, tracker):
        num_habits = len(tracker.habits)
        del_habit = tracker.get_habit("Test")
        tracker.delete_habit("Test")
        errors = []

        if len(tracker.habits) != num_habits - 1:
            errors.append("Nothing was deleted.")
        if [habit for habit in tracker.habits if habit.name == "Test"]:
            errors.append("'Test' habit was not deleted.")

        with sqlite3.connect("habits.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM habits WHERE habit_id = ?;", (del_habit.habit_id,))
            if cur.fetchone():
                errors.append("The value was not excluded from the database.")

            cur.execute("SELECT * FROM habits_log WHERE habit_id = ?;", (del_habit.habit_id,))
            if cur.fetchall():
                errors.append("Its log was not deleted.")

        assert not errors, "\n".join(errors)

    def test_view_habits(self, tracker):
        tracker.add_habit("Test1", "daily", "Simple test 1.")
        tracker.add_habit("Test2", "weekly", "Simple test 2.")
        tracker.add_habit("Test3", "monthly", "Simple test 3.")
        errors = []

        if "Test1" not in tracker.view_habits("daily"):
            errors.append("Daily filter is not working.")
        if "Test2" not in tracker.view_habits("weekly"):
            errors.append("Weekly filter is not working.")
        if "Test3" not in tracker.view_habits("monthly"):
            errors.append("Monthly filter is not working.")
        if "Test1, Test2, Test3" not in tracker.view_habits(''):
            errors.append("Viewing all habits is not working")

        tracker.delete_habit("Test1")
        tracker.delete_habit("Test2")
        tracker.delete_habit("Test3")

        assert not errors, "\n".join(errors)
