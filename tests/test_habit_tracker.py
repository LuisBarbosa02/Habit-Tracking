import pytest
from ..habit_tracker import Habit, HabitTracker


@pytest.fixture
def tracker():
    return HabitTracker()


def test_add_habit(tracker):
    num_habits = len(tracker.habits)
    tracker.add_habit("Test", "daily", "Simple test.")
    errors = []
    if not len(tracker.habits) == num_habits + 1:
        errors.append("Anything was stored.")
    if not isinstance(tracker.habits[-1], Habit):
        errors.append("Something else than a Habit was stored.")
    assert not errors, "\n{}".format("\n".join(errors))

def test_view_habits(tracker):
    assert tracker.view_habits() == ', '.join([habit.name for habit in tracker.habits])
