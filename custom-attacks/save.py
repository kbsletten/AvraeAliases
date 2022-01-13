embed
<drac2>
argv = &ARGS&
index = 2

saved_json = load_json(get("_customAttacks", "{}"))

monster_name = argv[0] if argv else None
attack_name = argv[1] if argv and len(argv) > 1 else None

# BEGIN parse.py
KEYWORDS = ["damage", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail", "fail5", "pass"]

json = {}

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

argv = argv[index:]
args = argparse(argv)

json["desc"] = args.last("desc")
json["verb"] = args.last("verb")
json["proper"] = bool(args.last("proper", False))

if monster_name and monster_name not in saved_json:
  saved_json[monster_name] = {}
if monster_name and attack_name:
  saved_json[monster_name][attack_name] = json

set_uvar("_customAttacks", dump_json(saved_json))

</drac2>
-title "Saving a Custom Attack!"
{{f"""-f "{monster_name}|Added {attack_name}" """ if monster_name and attack_name else ""}}
-footer "!custom_attack save | kbsletten#5710"
