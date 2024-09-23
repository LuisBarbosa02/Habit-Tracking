import sys
from habit_tracker import HabitTracker


class Interface:
    """
    Interface that simplifies the interaction with the program.

    :ivar habit_tracker.HabitTracker habit_tracker: The class that manages all the habits'
    """

    def __init__(self):
        """Initializes the class that will keep track of all habits."""
        self.habit_tracker = HabitTracker()
        self.choices = {"1": self.add_habit, "2": self.view_habits, "3": self.delete_habit, "4": self.exit}

    @staticmethod
    def display_menu():
        """Displays the main menu."""
        print("\n=== Habit Tracker Menu ===")
        print("1. Add habit")
        print("2. View habits")
        print("3. Delete habit")
        print("4. Exit")
        print("")

    def add_habit(self):
        """Create a new habit."""
        name = input("Choose a habit`s name: ").strip()
        while name in [habit.name for habit in self.habit_tracker.habits]:
            name = input("This name already exists, choose another: ").strip()

        periodicity = input("Choose between daily, weekly, or monthly periodicity: ").strip().lower()
        while periodicity not in ["daily", "weekly", "monthly"]:
            periodicity = input("Choose a valid periodicity: ").strip().lower()

        description = input("Clearly and concisely describe the habits` task: ")
        self.habit_tracker.add_habit(name, periodicity, description)

    def view_habits(self):
        """View the name of all habits."""
        print(self.habit_tracker.view_habits())

    def delete_habit(self):
        name = input("What is the name of the habit to be deleted? ")
        while name not in [habit.name for habit in self.habit_tracker.habits]:
            name = input("That habit does not exists, choose a valid name: ")

        self.habit_tracker.delete_habit(name)

    @staticmethod
    def exit():
        """Terminate the program's execution."""
        sys.exit()

    def run(self):
        """Main loop that runs the interface."""
        while True:
            self.display_menu()
            choice = input("Choose an option: ")
            choice = self.choices.get(choice)
            while choice is None:
                choice = input("Choose a valid option: ")
                choice = self.choices.get(choice)
            choice()


if __name__ == "__main__":
    interface = Interface()
    interface.run()
