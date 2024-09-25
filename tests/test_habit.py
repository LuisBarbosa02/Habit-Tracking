import pytest
from ..habit_tracker import Habit
import datetime


@pytest.fixture
def habit():
    return Habit(1, "Testing", "daily", "Just a simple test.", datetime.date.today(),
                 0, 0, 0)


def test_name_property(habit):
    assert habit.name == "Testing"

def test_is_complete(habit):
    habit.is_complete()
    assert isinstance(habit.log[-1], datetime.datetime)
