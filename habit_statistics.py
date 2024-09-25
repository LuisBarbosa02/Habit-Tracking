def longest_streak_all(habit_tracker):
    max_val = [habit.longest_streak for habit in habit_tracker.habits]
    longest_streak = [habit for habit in habit_tracker.habits if habit.longest_streak == max(max_val)]

    formatted_strings = []
    for habit in longest_streak:
        formatted_strings.append(f"{habit.name}: {habit.longest_streak}")

    return ", ".join(formatted_strings)

def longest_streak_habit(name, habit_tracker):
    habit = habit_tracker.get_habit(name)
    return f'"{habit.name}" longest streak: {habit.longest_streak}'

def most_struggled_habit(habit_tracker):
    max_val = [habit.streak_breaks for habit in habit_tracker.habits]
    streak_breaks = [habit for habit in habit_tracker.habits if habit.streak_breaks == max(max_val)]

    formatted_strings = []
    for habit in streak_breaks:
        formatted_strings.append(f"{habit.name}: {habit.streak_breaks}")

    return ", ".join(formatted_strings)
