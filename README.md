# Haven

A small proof-of-concept settlement survival game played in the terminal.

You manage a tiny settlement in the wilderness: food, wood, morale, shelters,
defense, and population. Seasons, weather, random events, and births/deaths
shape your run.

## Structure

- `config.py` – balancing constants and weather tables
- `state.py` – `HavenState` dataclass holding game state
- `environment.py` – season + weather logic
- `systems.py` – daily upkeep, weather effects, pregnancies, end conditions
- `events.py` – random animal attacks, accidents, travellers
- `actions.py` – player actions and their effects
- `ui.py` – terminal input/output helpers (intro, state display, action menu)
- `main.py` – main game loop wiring everything together

## Running

From this directory:

```bash
python -m haven.main
```

(or `python3` depending on your system.)

Make sure the parent folder is on your `PYTHONPATH`, e.g.:

```bash
cd /path/to/parent
python -m haven.main
```
