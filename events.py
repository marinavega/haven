import random
from typing import List
from state import HavenState


def _animal_attack(state: HavenState) -> List[str]:
    messages: List[str] = []
    roll = random.random()

    if roll < 0.4:
        base_damage = random.randint(1, 4)
    elif roll < 0.7:
        base_damage = random.randint(1, 3)
    else:
        base_damage = random.randint(2, 5)

    damage = max(0, base_damage - state.defense // 4)

    if damage <= 0:
        state.morale += 1
        messages.append("Animals threaten the camp, but guards drive them away (+1 morale).")
        return messages

    lost = min(state.population, damage)
    state.population -= lost
    penalty = 4 + lost
    state.morale -= penalty
    messages.append(f"Animal attack kills {lost} (-{penalty} morale).")
    return messages


def _accident(state: HavenState) -> List[str]:
    messages: List[str] = []
    roll = random.random()

    if roll < 0.4 and state.population > 0:
        state.population -= 1
        state.morale -= 5
        messages.append("A work accident kills one (-5 morale).")
    elif roll < 0.75:
        lost_wood = min(state.wood, random.randint(2, 8))
        state.wood -= lost_wood
        state.morale -= 3
        messages.append(f"A fire destroys {lost_wood} wood (-3 morale).")
    else:
        if state.population > 4:
            lost = random.randint(1, min(3, state.population))
            state.population -= lost
            penalty = 3 + lost
            state.morale -= penalty
            messages.append(f"Illness spreads, killing {lost} (-{penalty} morale).")
        else:
            messages.append("A sickness threatens the camp, but no one dies this time.")

    return messages


def _travellers(state: HavenState) -> List[str]:
    messages: List[str] = []
    arrivals = random.randint(1, 5)
    state.population += arrivals
    state.morale += 2
    messages.append(f"{arrivals} travellers arrive and join you (+2 morale).")
    return messages


def random_events(state: HavenState) -> List[str]:
    messages: List[str] = []

    animal_chance = 0.15
    if state.defense < 5:
        animal_chance += 0.1
    if state.morale < 30:
        animal_chance += 0.05

    accident_chance = 0.1
    if state.population > 10:
        accident_chance += 0.05
    if state.wood > 20:
        accident_chance += 0.05

    traveller_chance = 0.1
    if state.food > 40 and state.morale > 45:
        traveller_chance += 0.1

    if random.random() < animal_chance:
        messages.extend(_animal_attack(state))

    if random.random() < accident_chance:
        messages.extend(_accident(state))

    if random.random() < traveller_chance:
        messages.extend(_travellers(state))

    return messages
