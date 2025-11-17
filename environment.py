import random
from config import WEATHER_BY_SEASON
from state import HavenState


def get_season(day: int) -> str:
    """Return season name for a given day index (simple 32-day year)."""
    idx = (day - 1) % 32
    if idx < 8:
        return "spring"
    if idx < 16:
        return "summer"
    if idx < 24:
        return "autumn"
    return "winter"


def roll_weather(season: str) -> str:
    """Sample a weather type from the configured distribution for a season."""
    options, weights = zip(*WEATHER_BY_SEASON[season])
    return random.choices(options, weights=weights, k=1)[0]


def update_environment(state: HavenState) -> None:
    """Update season + weather for the new day."""
    state.season = get_season(state.day)
    state.weather = roll_weather(state.season)
