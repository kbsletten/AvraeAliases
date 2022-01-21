embed
<drac2>
argv = &ARGS&
export_yaml = "yaml" in argv
argv = [arg for arg in argv if arg != "yaml"]

# BEGIN parse.py
KEYWORDS = ["damage", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail", "fail5", "pass"]

json = {}
index = 1

if index < len(argv) and argv[index] == "use":
  index += 1
  json["use"] = {}
  if index < len(argv) and argv[index] == "spell":
    index += 1
    if index < len(argv):
      json["use"]["spell"] = argv[index]
      index += 1
  if index < len(argv) and argv[index] == "counter":
    index += 1
    if index < len(argv):
      json["use"]["counter"] = argv[index]
      index += 1

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

args = argparse(argv[index:])

save_damage = { "type": "roll", "name": "Damage", "dice": json["save"]["fail"]["damage"] } if "save" in json and "fail" in json["save"] and "damage" in json["save"]["fail"] else None
save_json = { "type": "save", "stat": json["save"]["ability"], "dc": json["save"]["dc"], "fail": [], "success": [] } if "save" in json else None
attack_json = { "type": "attack", "attackBonus": json["attack"]["bonus"], "hit": [], "miss": [] } if "attack" in json else None

if "save" in json:
  if "pass" in json["save"]:
    j = json["save"]["pass"]
    save_json["success"] = [x for x in [
      { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
      {
        "type": "ieffect",
        "name": j["effect"].partition("|")[0],
        "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
        "effects": j["effect"].partition("|")[2]
      } if "effect" in j else None
    ] if x]
  if "fail" in json["save"]:
    j = json["save"]["fail"]
    save_json["fail"] = [x for x in [
      { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
      {
        "type": "ieffect",
        "name": j["effect"].partition("|")[0],
        "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
        "effects": j["effect"].partition("|")[2]
      } if "effect" in j else None
    ] if x]
  if "fail5" in json["save"]:
    j = json["save"]["fail5"]
    save_json["fail"] = {
      "type": "condition",
      "condition": "lastSaveRollTotal <= (lastSaveDC-5)",
      "onTrue": [x for x in [
        { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
        {
          "type": "ieffect",
          "name": j["effect"].partition("|")[0],
          "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
          "effects": j["effect"].partition("|")[2]
        } if "effect" in j else None
      ] if x],
      "onFalse": save_json["fail"]
    }

if "attack" in json:
  if "miss" in json["attack"]:
    j = json["attack"]["miss"]
    attack_json["miss"] = [x for x in [
      { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
      {
        "type": "ieffect",
        "name": j["effect"].partition("|")[0],
        "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
        "effects": j["effect"].partition("|")[2]
      } if "effect" in j else None
    ] if x]
  if "hit" in json["attack"]:
    j = json["attack"]["hit"]
    attack_json["hit"] = [x for x in [
      { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
      {
        "type": "ieffect",
        "name": j["effect"].partition("|")[0],
        "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
        "effects": j["effect"].partition("|")[2]
      } if "effect" in j else None,
      save_json
    ] if x]
  if "crit" in json["attack"]:
    j = json["attack"]["crit"]
    attack_json["hit"] = attack_json["hit"] + [{
      "type": "condition",
      "condition": "lastAttackDidCrit",
      "onTrue": [x for x in [
        { "type": "damage", "damage": j["damage"] } if "damage" in j else None,
        {
          "type": "ieffect",
          "name": j["effect"].partition("|")[0],
          "duration": int(argparse(j["effect"].partition("|")[2]).last("dur", -1)),
          "effects": j["effect"].partition("|")[2]
        } if "effect" in j else None
      ] if x],
      "onFalse": []
    }]

use_json = []
if "use" in json and "spell" in json["use"]:
  use_json = use_json + [{ "type": "counter", "counter": { "slot": json["use"]["spell"] }, "amount": 1 }]
if "use" in json and "counter" in json["use"]:
  use_json = use_json + [{ "type": "counter", "counter": json["use"]["counter"], "amount": 1 }]

automation = {
  "name": argv[0],
  "automation": [{ "type": "target", "target": "each", "effects": [attack_json] + use_json }] if attack_json else [x for x in [save_damage, { "type": "target", "target": "all", "effects": [save_json] }] + use_json if x],
  "_v": 2,
  "proper": args.last("proper") == "True",
  "verb": args.last("verb"),
  "extra_crit_damage": json["attack"]["crit"]["damage"] if "attack" in json and "crit" in json["attack"] and "damage" in json["attack"]["crit"] else None
}
desc = dump_json(automation).replace("\"", "\\\"").replace(": ", ":") if not export_yaml else f"""```
<avrae hidden>
{dump_yaml(automation)}
</avrae>
```"""
</drac2>
-title "Export Attack!"
-desc "{{desc}}"
-footer "!custom_attack export | kbsletten#5710"
