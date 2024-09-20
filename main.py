import sys
from habit_tracker import HabitTracker


class Interface:
    """
    Interface that simplifies the interaction with the program.
    """

    def __init__(self):
        """Initializes the class that will keep track of all habits."""
        self.habit_tracker = HabitTracker()
        self.choices = {"1": self.habit_tracker.add_habit, "2": self.exit}

    @staticmethod
    def display_menu():
        """Displays the main menu."""
        print("\n=== Habit Tracker Menu ===")
        print("1. Add habit")
        print("2. Exit")
        print("")

    @staticmethod
    def exit():
        """Terminate the program`s execution"""
        sys.exit()

    def run(self):
        """Main loop that runs the interface."""
        while True:
            self.display_menu()
            choice = input("Choose an option: ")
            choice = self.choices.get(choice)
            choice()


if __name__ == "__main__":
    interface = Interface()
    interface.run()
