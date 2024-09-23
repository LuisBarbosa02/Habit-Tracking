import pytest
from ..habit_tracker import Habit, HabitTracker
import sqlite3


@pytest.fixture
def tracker():
    return HabitTracker()


def test_add_habit(tracker):
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

def test_view_habits(tracker):
    assert tracker.view_habits() == ', '.join([habit.name for habit in tracker.habits])

def test_load_habits(tracker):
    assert all(isinstance(habit, Habit) for habit in tracker.habits)
