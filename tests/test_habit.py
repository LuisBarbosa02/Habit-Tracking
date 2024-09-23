import pytest
from ..habit_tracker import Habit
import datetime


@pytest.fixture
def habit():
    return Habit(1, "Testing", "daily", "Just a simple test.", datetime.date.today())


def test_name_property(habit):
    assert habit.name == "Testing"
