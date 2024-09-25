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
        self.choices = {"1": self.add_habit, "2": self.view_habits_menu, "3": self.complete_habit,
                        "4": self.delete_habit, "5": self.exit}

    @staticmethod
    def display_menu():
        """Displays the main menu."""
        print("\n=== Habit Tracker Menu ===")
        print("1. Add habit")
        print("2. View habits")
        print("3. Complete habit")
        print("4. Delete habit")
        print("5. Exit\n")

    def add_habit(self):
        """Create a new habit."""
        name = input("Choose a habit name: ").strip()
        while name in [habit.name for habit in self.habit_tracker.habits]:
            name = input("This name already exists, choose another: ").strip()

        periodicity = input("Choose between daily, weekly, or monthly periodicity: ").strip().lower()
        while periodicity not in ["daily", "weekly", "monthly"]:
            periodicity = input("Choose a valid periodicity: ").strip().lower()

        description = input("Clearly and concisely describe the habits' task: ")
        self.habit_tracker.add_habit(name, periodicity, description)

    def view_habits_menu(self):
        """Menu for the visualization of habits."""
        print("\n=== Habits Menu ===")
        print("1. View all habits")
        print("2. View habits per periodicity")
        print("3. Specific habit information\n")

        choice = input("Choose an option: ")
        while choice not in ["1", "2", "3"]:
            choice = input("Choose a valid option: ")

        if not self.habit_tracker.habits:
            print("No habits' defined, create a new one first.")
            self.run()
        elif choice == "1":
            print("\n" + self.habit_tracker.view_habits(periodicity=''))
        elif choice == "2":
            periodicity = input("Choose between daily, weekly, or monthly: ").strip().lower()
            while periodicity not in ["daily", "weekly", "monthly"]:
                periodicity = input("Choose a valid periodicity: ").strip().lower()
            print("\n" + self.habit_tracker.view_habits(periodicity=periodicity))
        elif choice == "3":
            name = input("Choose a habit by name: ")
            while name not in [habit.name for habit in self.habit_tracker.habits]:
                name = input("This habit does not exist, choose a valid one: ")
            print(self.habit_tracker.get_habit(name))

    def complete_habit(self):
        """Mark a habit as completed."""
        if not self.habit_tracker.habits:
            print("There aren't any habits to complete.")
            self.run()

        print("\nAvailable habits:\n" + self.habit_tracker.view_habits(periodicity='') + "\n")
        name = input("Choose habit to complete: ")
        while name not in [habit.name for habit in self.habit_tracker.habits]:
            name = input("Choose a valid habit: ")

        self.habit_tracker.complete_habit(name)
        print("Habit completed.")

    def delete_habit(self):
        """Delete a habit."""
        if not self.habit_tracker.habits:
            print("There aren't any habits to delete.")
            self.run()

        name = input("What is the name of the habit to be deleted? ")
        while name not in [habit.name for habit in self.habit_tracker.habits]:
            name = input("That habit does not exists, choose a valid name: ")

        self.habit_tracker.delete_habit(name)
        print(f"{name} successfully deleted.")

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
