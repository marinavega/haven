import random
from typing import Tuple, List
from config import END_DAY
from state import HavenState


def apply_upkeep(state: HavenState) -> List[str]:
    messages: List[str] = []

    food_needed = state.population

    if state.weather == "heatwave":
        food_needed += max(1, state.population // 2)

    if state.season == "winter":
        food_needed += max(0, state.population // 3)

    state.food -= food_needed

    if state.food < 0:
        deficit = -state.food
        lost = max(1, deficit // 3)
        lost = min(lost, state.population)
        state.population -= lost
        state.food = 0
        state.morale -= 8
        messages.append(f"Food shortage: {lost} people die (-8 morale).")
    else:
        if state.weather not in ("storm", "snow", "heatwave"):
            drift = random.randint(0, 2)
            state.morale += drift
            if drift:
                messages.append(f"People feel a bit better (+{drift} morale).")

    capacity = state.shelters * 5
    if state.population > capacity:
        overflow = state.population - capacity
        penalty = min(15, overflow * 2)
        state.morale -= penalty
        messages.append(f"Overcrowding: not enough shelters (-{penalty} morale).")

    return messages


def apply_weather_effects(state: HavenState) -> List[str]:
    messages: List[str] = []
    w = state.weather

    if w == "storm":
        lost_food = min(state.food, random.randint(1, 8))
        lost_wood = min(state.wood, random.randint(0, 6))
        state.food -= lost_food
        state.wood -= lost_wood
        morale_delta = random.randint(1, 3)
        state.morale -= morale_delta
        messages.append(
            f"Storm damage: -{lost_food} food, -{lost_wood} wood (-{morale_delta} morale)."
        )

    elif w == "snow":
        morale_delta = random.randint(1, 3)
        state.morale -= morale_delta
        messages.append(f"Cold and snow wear people down (-{morale_delta} morale).")

    elif w == "clear":
        morale_delta = random.randint(1, 3)
        state.morale += morale_delta
        messages.append(f"A clear day lifts spirits (+{morale_delta} morale).")

    elif w == "rain" and state.season == "spring":
        state.rain_bonus = min(3, state.rain_bonus + 1)
        messages.append("Spring rain nourishes the land. Foraging will be a bit better.")

    elif w == "heatwave":
        morale_delta = random.randint(1, 3)
        state.morale -= morale_delta
        messages.append(f"Brutal heat exhausts everyone (-{morale_delta} morale).")

    return messages


def handle_pregnancies(state: HavenState) -> List[str]:
    messages: List[str] = []
    births_today = 0
    remaining = []

    for due_day in state.pregnancies:
        if state.day >= due_day:
            births_today += 1
        else:
            remaining.append(due_day)

    state.pregnancies = remaining

    if births_today > 0:
        state.population += births_today
        morale_gain = births_today * 2
        state.morale += morale_gain
        messages.append(
            f"{births_today} birth(s) in the settlement (+{morale_gain} morale)."
        )

    if state.population >= 4 and state.morale >= 40 and state.food >= 20:
        base_chance = min(0.25, 0.05 + state.population * 0.01)
        if random.random() < base_chance:
            state.pregnancies.append(state.day + 9)
            messages.append("A couple is expecting a child (due in 9 days).")

    return messages


def check_end(state: HavenState) -> Tuple[bool, str]:
    if state.population <= 0:
        return True, "Everyone is gone. Nothing remains of your settlement."

    if state.food <= 0:
        return True, "Your people starved. The settlement is abandoned."

    if state.morale <= 0:
        return True, "Morale collapsed. People scatter to survive on their own."

    if state.day > END_DAY:
        msg = [f"You survived {END_DAY} days. The settlement has roots now."]
        thriving = state.population >= 12 and state.morale >= 60 and state.food >= 60
        if thriving:
            msg.append(
                "You don't just survive — you thrive. "
                "This could become a real town."
            )
        else:
            msg.append("You made it, but just barely. The future is uncertain.")
        return True, " ".join(msg)

    return False, ""
