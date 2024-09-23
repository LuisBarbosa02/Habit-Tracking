import pytest
from ..habit_tracker import Habit, HabitTracker
import sqlite3


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

    def test_view_habits(self, tracker):
        assert tracker.view_habits() == ', '.join([habit.name for habit in tracker.habits])

    def test_get_habit(self, tracker):
        habit = tracker._get_habit("Test")
        assert habit.habit_id == [habit.habit_id for habit in tracker.habits if habit.name == "Test"][0]


    def test_load_habits(self, tracker):
        assert all(isinstance(habit, Habit) for habit in tracker.habits)

    def test_delete_habit(self, tracker):
        num_habits = len(tracker.habits)
        del_habit = tracker._get_habit("Test")
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

        assert not errors, "\n".join(errors)
