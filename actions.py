import random
from typing import List, Callable, Tuple
from state import HavenState


ActionFn = Callable[[HavenState], List[str]]


def gather_food(state: HavenState) -> List[str]:
    messages: List[str] = []
    base = random.randint(4, 12)

    if state.season == "winter":
        base -= random.randint(2, 5)
    elif state.season == "summer" and state.weather in ("clear", "heatwave"):
        base += random.randint(1, 4)

    if state.rain_bonus > 0:
        base += state.rain_bonus
        state.rain_bonus -= 1
        messages.append("Recent rain makes foraging easier.")

    gained = max(0, base)
    state.food += gained
    state.morale += random.randint(-2, 0)
    messages.append(f"Foraging yields {gained} food.")
    return messages


def gather_wood(state: HavenState) -> List[str]:
    messages: List[str] = []
    base = random.randint(3, 10)

    if state.season == "winter" and state.weather == "snow":
        base -= random.randint(1, 4)
        messages.append("Snow slows wood gathering.")

    gained = max(0, base)
    state.wood += gained
    state.morale += random.randint(-2, 0)
    messages.append(f"Wood gathering yields {gained} wood.")
    return messages


def build_shelter(state: HavenState) -> List[str]:
    messages: List[str] = []
    cost = 12

    if state.wood < cost:
        messages.append("Not enough wood to build a shelter.")
        return messages

    state.wood -= cost
    state.shelters += 1
    morale_gain = random.randint(1, 4)
    state.morale += morale_gain
    messages.append(f"Shelter built (+{morale_gain} morale).")
    return messages


def train_guards(state: HavenState) -> List[str]:
    messages: List[str] = []
    cost = 6

    if state.food < cost:
        messages.append("Not enough food to train guards.")
        return messages

    state.food -= cost
    defense_gain = random.randint(2, 5)
    morale_gain = random.randint(0, 3)
    state.defense += defense_gain
    state.morale += morale_gain
    messages.append(f"Guards trained (+{defense_gain} defense, +{morale_gain} morale).")
    return messages


def rest(state: HavenState) -> List[str]:
    messages: List[str] = []
    morale_gain = random.randint(3, 7)
    extra_food = max(0, state.population // random.randint(2, 4))
    state.morale += morale_gain
    state.food -= extra_food
    messages.append(f"Day of rest (+{morale_gain} morale, -{extra_food} food).")
    return messages


def big_hunt(state: HavenState) -> List[str]:
    messages: List[str] = []
    if state.population < 3:
        messages.append("Not enough hunters for a big hunt.")
        return messages

    roll = random.random()
    if roll < 0.2:
        lost = random.randint(1, min(3, state.population))
        state.population -= lost
        penalty = 8 + lost
        state.morale -= penalty
        messages.append(f"Big hunt fails: {lost} hunters die (-{penalty} morale).")
    elif roll < 0.6:
        gained = random.randint(10, 20)
        state.food += gained
        state.morale += 1
        messages.append(f"Big hunt yields {gained} food (+1 morale).")
    else:
        gained = random.randint(20, 40)
        state.food += gained
        state.morale += 6
        messages.append(f"Huge success: {gained} food (+6 morale).")
    return messages


def festival(state: HavenState) -> List[str]:
    messages: List[str] = []
    min_food = max(10, state.population * 2)

    if state.food < min_food:
        messages.append("Not enough food for a proper festival.")
        return messages

    state.food -= min_food
    morale_gain = random.randint(8, 15)
    state.morale += morale_gain
    messages.append(f"Festival held (+{morale_gain} morale, -{min_food} food).")

    if random.random() < 0.35:
        newcomers = random.randint(1, 4)
        state.population += newcomers
        state.morale += 2
        messages.append(f"Celebration draws {newcomers} wanderers (+2 morale).")

    return messages


def build_watchtower(state: HavenState) -> List[str]:
    messages: List[str] = []
    cost = 18

    if state.wood < cost:
        messages.append("Not enough wood to build a watchtower.")
        return messages

    state.wood -= cost
    defense_gain = random.randint(4, 8)
    morale_gain = random.randint(1, 3)
    state.defense += defense_gain
    state.morale += morale_gain
    messages.append(
        f"Watchtower constructed (+{defense_gain} defense, +{morale_gain} morale)."
    )
    return messages


ACTIONS: list[tuple[str, ActionFn]] = [
    ("Gather food", gather_food),
    ("Gather wood", gather_wood),
    ("Build shelter", build_shelter),
    ("Train guards", train_guards),
    ("Rest", rest),
    ("Big hunt", big_hunt),
    ("Festival", festival),
    ("Build watchtower", build_watchtower),
]
