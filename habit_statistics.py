def longest_streak_all(habit_tracker):
    max_val = [habit.longest_streak for habit in habit_tracker.habits]
    longest_streak = [habit for habit in habit_tracker.habits if habit.longest_streak == max(max_val)]

    formatted_strings = []
    for habit in longest_streak:
        formatted_strings.append(f"{habit.name}: {habit.longest_streak}")

    return ", ".join(formatted_strings)
