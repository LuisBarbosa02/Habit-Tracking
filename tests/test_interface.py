import pytest
from main import Interface
from habit_tracker import Habit


@pytest.fixture
def interface():
    return Interface()

def test_habit_added(interface):
    errors = []

    num_habits = len(interface.habit_tracker.habits)
    interface.add_habit()
    if len(interface.habit_tracker.habits) != num_habits + 1:
        errors.append("No habit was stored!")
    if not isinstance(interface.habit_tracker.habits[-1], Habit):
        errors.append("The object stored is not a Habit!")

    assert not errors

def test_habits_visualized(interface):
    assert interface.habit_tracker.view_habits() == ', '.join([habit.name for habit in interface.habit_tracker.habits])
