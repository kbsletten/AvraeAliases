action import
<drac2>
# BEGIN parse.py
KEYWORDS = ["damage", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail", "fail5", "pass"]

argv = &ARGS&
json = {}
index = 1

if index < len(argv) and argv[index] == "attack":
  index += 1
  json["attack"] = { "bonus": argv[index] }
  index += 1
  for attack in ATTACK:
    if index < len(argv) and argv[index] == attack:
      index += 1
      json["attack"][attack] = {}
      for keyword in KEYWORDS:
        if index < len(argv) and argv[index] == keyword:
          index += 1
          json["attack"][attack][keyword] = argv[index]
          index += 1

if index < len(argv) and argv[index] == "save":
  index += 1
  json["save"] = { "ability": argv[index] }
  index += 1
  json["save"]["dc"] = argv[index]
  index += 1
  for save in SAVE:
    if index < len(argv) and argv[index] == save:
      index += 1
      json["save"][save] = {}
      for keyword in KEYWORDS:
        if index < len(argv) and argv[index] == keyword:
          index += 1
          json["save"][save][keyword] = argv[index]
          index += 1
      if index < len(argv) and argv[index] == "half":
        index += 1
        json["save"][save]["damage"] = "({Damage})/2" if "attack" not in json else f"""({json["save"]["fail"]["damage"]})/2"""
# END parse.py

save_damage = { "type": "roll", "name": "Damage", "dice": json["save"]["fail"]["damage"] } if "save" in json and "fail" in json["save"] and "damage" in json["save"]["fail"] else None
save_json = { "type": "save", "stat": json["save"]["ability"], "dc": json["save"]["dc"], "fail": [], "success": [] } if "save" in json else None
attack_json = { "type": "attack", "attackBonus": json["attack"]["bonus"], "hit": [], "miss": [] } if "attack" in json else None

if "save" in json:
  if "pass" in json["save"]:
    save_json["success"] = [x for x in [
      { "type": "damage", "damage": json["save"]["pass"]["damage"] } if "damage" in json["save"]["pass"] else None,
      { "type": "ieffect", "name": json["save"]["pass"]["effect"], "duration": -1, "effects": "" } if "effect" in json["save"]["pass"] else None
    ] if x]
  if "fail" in json["save"]:
    save_json["fail"] = [x for x in [
      { "type": "damage", "damage": "{Damage}" if "attack" not in json else json["save"]["fail"]["damage"] } if "damage" in json["save"]["fail"] else None,
      { "type": "ieffect", "name": json["save"]["fail"]["effect"], "duration": -1, "effects": "" } if "effect" in json["save"]["fail"] else None
    ] if x]
  if "fail5" in json["save"]:
    save_json["fail"] = {
      "type": "condition",
      "condition": "lastSaveRollTotal <= (lastSaveDC-5)",
      "onTrue": [x for x in [
        { "type": "damage", "damage": json["save"]["fail5"]["damage"] } if "damage" in json["save"]["fail5"] else None,
        { "type": "ieffect", "name": json["save"]["fail5"]["effect"], "duration": -1, "effects": "" } if "effect" in json["save"]["fail5"] else None
      ] if x],
      "onFalse": save_json["fail"]
    }

if "attack" in json:
  if "miss" in json["attack"]:
    attack_json["miss"] = [x for x in [
      { "type": "damage", "damage": json["attack"]["miss"]["damage"] } if "damage" in json["attack"]["miss"] else None,
      { "type": "ieffect", "name": json["attack"]["miss"]["effect"], "duration": -1, "effects": "" } if "effect" in json["attack"]["miss"] else None
    ] if x]
  if "hit" in json["attack"]:
    attack_json["hit"] = [x for x in [
      { "type": "damage", "damage": json["attack"]["hit"]["damage"] } if "damage" in json["attack"]["hit"] else None,
      { "type": "ieffect", "name": json["attack"]["hit"]["effect"], "duration": -1, "effects": "" } if "effect" in json["attack"]["hit"] else None,
      save_json
    ] if x]
  if "crit" in json["attack"]:
    attack_json["hit"] = attack_json["hit"] + [{
      "type": "condition",
      "condition": "lastAttackDidCrit",
      "onTrue": [x for x in [
        { "type": "ieffect", "name": json["attack"]["crit"]["effect"], "duration": -1, "effects": "" } if "effect" in json["attack"]["crit"] else None
      ] if x],
      "onFalse": []
    }]

automation = {
  "name": argv[0],
  "automation": [{ "type": "target", "target": "each", "effects": [attack_json] }] if attack_json else [x for x in [save_damage, { "type": "target", "target": "all", "effects": [save_json] }] if x],
  "_v": 2,
  "proper": False,
  "verb": "commands their Retainer to attack with",
  "extra_crit_damage": json["attack"]["crit"]["damage"] if "attack" in json and "crit" in json["attack"] and "damage" in json["attack"]["crit"] else None
}
</drac2>
{{dump_json(automation)}}
