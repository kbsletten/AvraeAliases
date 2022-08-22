#!gvar edit f90efd6e-d7ce-44e0-b0c9-0b3438a14271

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMS = "0123456789"

def get_settings(comb):
  settings = {}
  for note in comb.note.split(" | ") if comb.note else []:
    key, _, value = note.partition(": ")
    if not value:
      value = key
      key = "Note"
    settings[key] = value
  return settings

def set_settings(comb, settings):
  comb.set_note(" | ".join([f"{key}: {value}" for key, value in settings.items()]))

def parse_coord(location):
  y = 0
  x = 0
  for ch in location:
    if ch in CHARS:
      x = x * 26 + CHARS.index(ch) + 1
    elif ch in NUMS:
      y = y * 10 + NUMS.index(ch)
  return (x, y)

def get_coords(comb):
  settings = get_settings(comb)
  location = settings["Location"] if "Location" in settings else None
  size = settings["Size"] if "Size" in settings else None
  if not location:
    return [None, None]
  x, y = parse_coord(location)
  diameter = 4 if size == "c" else 3 if size == "g" else 2 if size == "h" else 1 if size == "l" else 0
  return [(x, y), (x + diameter, y + diameter)]

def to_alpha(x, y):
  coord = ""
  for _ in range(0, 3):
    if x > 0:
      remainder = (x - 1) % 26
      x = (x - 1) // 26
      coord = CHARS[remainder] + coord
  return f"{coord}{y}"

def get_map_options(init):
  map_options = {}
  if not init:
    return (map_options, None)
  for comb in init.combatants:
    map_attack = ([attack for attack in comb.attacks if attack.name == "map"] + [None])[0]
    if not map_attack:
      continue
    for effect in map_attack.raw["automation"][0]["text"].split(" ~ "):
      key, _, value = effect.partition(": ")
      map_options[key] = value
    return (map_options, comb)
  return (map_options, None)

def set_map_options(comb, map_options):
  comb.remove_effect("map")
  map_attack = {
    "attack": {
      "name": "map",
      "automation": [
        { "type": "text", "text": " ~ ".join(f"{key}: {value}" for key, value in map_options.items()) }
      ],
      "_v": 2
    }
  }
  comb.add_effect("map", attacks=[map_attack])

