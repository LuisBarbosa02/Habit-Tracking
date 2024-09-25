import pytest
from habit_tracker import HabitTracker
from tests.habit_examples import run_examples
import habit_statistics


@pytest.fixture
def tracker():
    return HabitTracker()


class TestHabitStatistics:
    @classmethod
    def setup_class(cls):
        run_examples()

    @classmethod
    def teardown_class(cls):
        habit_tracker = HabitTracker()
        for name in ["Drink Water", "Read", "Exercise", "Week Planning", "Complete Book"]:
           habit_tracker.delete_habit(name)

    def test_longest_streak_all(self, tracker):
        max_val = [habit.longest_streak for habit in tracker.habits]
        longest_streak = [f"{habit.name}: {habit.longest_streak}" for habit in tracker.habits
                          if habit.longest_streak == max(max_val)]

        result = habit_statistics.longest_streak_all(tracker)
        errors = []

        for name in longest_streak:
            if name not in result:
                errors.append(f"{name} not in result.")

        all_names_in_result = result.split(", ")
        for name in all_names_in_result:
            if name not in longest_streak:
                errors.append(f"{name} was not supposed to be in the result.")

        assert not errors, '\n'.join(errors)

    def test_longest_streak_habit(self, tracker):
        result = habit_statistics.longest_streak_habit("Read", tracker)
        habit = tracker.get_habit("Read")
        assert result == f'"{habit.name}" longest streak: {habit.longest_streak}'

    def test_most_struggled_habit(self, tracker):
        max_val = [habit.streak_breaks for habit in tracker.habits]
        streak_breaks = [f"{habit.name}: {habit.streak_breaks}" for habit in tracker.habits
                          if habit.streak_breaks == max(max_val)]

        result = habit_statistics.most_struggled_habit(tracker)
        errors = []

        for name in streak_breaks:
            if name not in result:
                errors.append(f"{name} not in result.")

        all_names_in_result = result.split(", ")
        for name in all_names_in_result:
            if name not in streak_breaks:
                errors.append(f"{name} was not supposed to be in the result.")

        assert not errors, '\n'.join(errors)

