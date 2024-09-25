import datetime
from dateutil.relativedelta import relativedelta
from habit_tracker import HabitTracker


habit_tracker = HabitTracker()

habit1 = ("Drink Water", "daily", "Drink 2 liters of water.")
habit2 = ("Read", "daily", "Read for at least 30 min.")
habit3 = ("Exercise", "weekly", "Make physical exercises for at least 3 days a week.")
habit4 = ("Week Planning", "weekly", "Plan the upcoming week.")
habit5 = ("Complete Book", "monthly", "Read one book for the period of one month.")


def create_logs(diff_current_date_days, diff_start_date_months_days, diff_log_months_days, num_breaks, current_streak):
    months, days = diff_start_date_months_days
    log_months, log_days = diff_log_months_days

    current_date = datetime.datetime.today() - relativedelta(days=diff_current_date_days)
    start_date = current_date - relativedelta(months=months, days=days)
    log = []
    while current_date > start_date:
        log.append(current_date)
        current_date = current_date - relativedelta(months=log_months, days=log_days)

    for i in range(num_breaks-1):
        current_date = current_date - relativedelta(months=log_months, days=log_days+10)
        log.append(current_date)

    log.reverse()
    latest_date = log[-1] + relativedelta(months=log_months, days=log_days+3)
    log.append(latest_date)
    for i in range(current_streak):
        log.append(log[-1] + relativedelta(months=log_months, days=log_days))

    return log


def create_habit_example(habits_char, diff_current_date_days, diff_start_date_months_days,
                         diff_log_months_days, num_breaks, current_streak):
    logs = create_logs(diff_current_date_days, diff_start_date_months_days, diff_log_months_days, num_breaks,
                       current_streak)
    habit_tracker.add_habit(*habits_char, logs[0].date())
    for log in logs:
        habit_tracker.complete_habit(habits_char[0], log)


def run_examples():
    create_habit_example(habit1, 0, (1, 15), (0, 1),
                     11, 2)
    create_habit_example(habit2, 1, (1, 11), (0, 1),
                     6, 3)
    create_habit_example(habit3, 2, (1, 23), (0, 7),
                     2, 2)
    create_habit_example(habit4, 3, (1, 27), (0, 7),
                     3, 4)
    create_habit_example(habit5, 4, (3, 9), (1, 0),
                     1, 1)
