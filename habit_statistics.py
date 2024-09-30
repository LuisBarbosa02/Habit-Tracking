def longest_streak_all(habit_tracker):  # Calculate the longest streak of all habits
    """
    The longest streak of all defined habits.

    :param habit_tracker: The habit manager class.
    :return: The name(s) of the habit(s) with the longest streak(s).
    :rtype: str
    """
    max_val = [habit.longest_streak for habit in habit_tracker.habits]
    longest_streak = [habit for habit in habit_tracker.habits if habit.longest_streak == max(max_val)]

    formatted_strings = []
    for habit in longest_streak:
        formatted_strings.append(f"{habit.name}: {habit.longest_streak}")

    return ", ".join(formatted_strings)

def longest_streak_habit(name, habit_tracker):  # Calculate the longest streak of a specific habit
    """
    The longest streak of a specific habit.

    :param name: The habit's name.
    :param habit_tracker: The habit manager class.
    :return: The longest streak of a habit.
    :rtype: str
    """
    habit = habit_tracker.get_habit(name)
    return f'"{habit.name}" longest streak: {habit.longest_streak}'

def most_struggled_habit(habit_tracker):  # Calculate the most broken of all habits
    """
    The most broken habits.

    :param habit_tracker: The habit manager class.
    :return: The name(s) of the habit(s) with the most broken streak(s).
    :rtype: str
    """
    max_val = [habit.streak_breaks for habit in habit_tracker.habits]
    streak_breaks = [habit for habit in habit_tracker.habits if habit.streak_breaks == max(max_val)]

    formatted_strings = []
    for habit in streak_breaks:
        formatted_strings.append(f"{habit.name}: {habit.streak_breaks}")

    return ", ".join(formatted_strings)
