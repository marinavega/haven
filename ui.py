from state import HavenState
from actions import ACTIONS

WEATHER_ICONS = {
    "clear": "☀️",
    "rain": "🌧️",
    "cloudy": "☁️",
    "storm": "⛈️",
    "snow": "❄️",
    "heatwave": "🔥",
}


def show_intro() -> None:
    print(
        r"""⠀⠀⠀⠀⠀⠀⠀⠀🌲      🌲         🌲⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀🌲⠀⠀⠀🌲⠀⠀⠀⠀⠀🌲⠀⠀⠀⠀⠀⠀⠀⠀🌲⠀⠀⠀🌲⠀

⠀⠀⠀🌲⠀⠀⠀⠀⢀⣴⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🌲⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣷⠀⠀⠀🔥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⠟⠀⠀⠀⠀⢀⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠸⣿⣿⣿⣷⣄⠀⠀⠀🌲⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀🌲⠀⠀⠀⠀⠀🏚⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣧⠀⠀⠀🌲⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀🏚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🌲⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

⠀⠀⠀⠀⠀⠀⠀⠀⭐ The wilderness is silent… for now ⭐"""
    )
    input("\nPress Enter to begin...\n")


def _bar(icon: str, value: int, *, scale: int = 5, max_icons: int = 10) -> str:
    """
    Compact visual bar for a resource.

    value     -> numeric value (e.g. food)
    scale     -> how much each icon represents
    max_icons -> max icons to draw before showing '+'
    """
    if value <= 0:
        return "—"
    n = value // scale
    if n <= 0:
        n = 1
    if n > max_icons:
        return icon * max_icons + " +"
    return icon * n


def _morale_face(morale: int) -> str:
    if morale >= 70:
        return "😄"
    if morale >= 40:
        return "😐"
    return "😣"


def print_state(state: HavenState) -> None:
    weather_icon = WEATHER_ICONS.get(state.weather, "?")
    pregnancies_due = sorted(d - state.day for d in state.pregnancies)

    print(f"\n=== Day {state.day} ===")
    print(f"Season: {state.season}   Weather: {weather_icon}  ({state.weather})\n")

    rows = [
        ("👤", "Population",  state.population, _bar("👤", state.population, scale=2)),
        ("🏚", "Shelters",    state.shelters,   _bar("🏚", state.shelters, scale=1)),
        ("🍞", "Food",        state.food,       _bar("🍞", state.food, scale=10)),
        ("🪵", "Wood",        state.wood,       _bar("🪵", state.wood, scale=10)),
        ("🛡", "Defense",     state.defense,    _bar("🛡", state.defense, scale=5)),
        ("🙂", "Morale",      state.morale,     _morale_face(state.morale)),
        ("🤰", "Pregnancies", len(state.pregnancies),
         f"(due in {pregnancies_due or '[]'} days)"),
    ]

    label_width = max(len(label) for _, label, _, _ in rows)

    for icon, label, value, details in rows:
        print(f"{icon} {label:<{label_width}} {value:>3}  {details}")

    print()


def choose_action() -> int:
    for idx, (label, _) in enumerate(ACTIONS, start=1):
        print(f"{idx}. {label}")
    choice = input("\nChoose an action (number): ").strip()
    try:
        return int(choice) - 1
    except ValueError:
        return -1
