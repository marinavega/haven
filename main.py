from state import HavenState
from environment import update_environment
from systems import apply_upkeep, apply_weather_effects, handle_pregnancies, check_end
from events import random_events
from actions import ACTIONS
from ui import show_intro, print_state, choose_action


def game_loop() -> None:
    show_intro()

    state = HavenState()

    print("Welcome to Haven. Keep your people alive long enough to build a future.\n")

    while True:
        update_environment(state)
        print_state(state)

        action_index = choose_action()
        if not (0 <= action_index < len(ACTIONS)):
            print("Invalid choice.")
            continue

        label, fn = ACTIONS[action_index]
        print(f"\n>>> {label}")
        messages = fn(state)
        for msg in messages:
            print(msg)

        for system_fn in (apply_upkeep, apply_weather_effects, handle_pregnancies, random_events):
            for msg in system_fn(state):
                print(msg)

        game_over, end_message = check_end(state)
        if game_over:
            print(f"\n{end_message}")
            break

        state.day += 1

    print("\nHaven simulation complete.\n")


if __name__ == "__main__":
    game_loop()
