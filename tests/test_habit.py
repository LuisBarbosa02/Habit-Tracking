import pytest
from ..habit_tracker import Habit


@pytest.fixture
def habit():
    return Habit("Testing", "daily", "Just a simple test.")


def test_name_property(habit):
    assert habit.name == "Testing"
