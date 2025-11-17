from dataclasses import dataclass, field
from typing import List


@dataclass
class HavenState:
    """Core game state for Haven.

    This stays intentionally small and serialisation-friendly so we can
    easily save/load or swap storage backends later (JSON, DB, etc).
    """

    day: int = 1
    population: int = 8
    food: int = 45
    wood: int = 20
    defense: int = 0
    morale: int = 55
    shelters: int = 2
    rain_bonus: int = 0
    pregnancies: List[int] = field(default_factory=list)
    season: str = "spring"
    weather: str = "clear"
