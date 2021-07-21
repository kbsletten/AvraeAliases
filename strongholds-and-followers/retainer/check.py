embed
<drac2>
argv = &ARGS&
args = argparse(argv)
GVARS = load_json(get_gvar("c1ee7d0f-750d-4f92-8d87-70fa22c07a81"))
CLASSES = [load_json(get_gvar(gvar)) for gvar in GVARS]
ABILITIES = {
  "dex": "dex",
  "dexterity": "dex",
  "cha": "cha",
  "charisma": "cha",
  "con": "con",
  "constitution": "con",
  "int": "int",
  "intelligence": "int",
  "str": "str",
  "strength": "str",
  "wis": "wis",
  "wisdom": "wis"
}
SKILLS = {
  "acrobatics": "dex",
  "animalhandling": "wis",
  "athletics": "str",
  "arcana": "int",
  "deception": "cha",
  "history": "int",
  "investigation": "int",
  "insight": "wis",
  "intimidation": "cha",
  "medicine": "wis",
  "nature": "int",
  "perception": "wis",
  "performance": "cha",
  "persuasion": "cha",
  "religion": "int",
  "sleightofhand": "dex",
  "survival": "wis",
  "stealth": "dex"
}
DISPLAY = {
  "acrobatics": "Acrobatics",
  "animalhandling": "Animal Handling",
  "athletics": "Athletics",
  "arcana": "Arcana",
  "deception": "Deception",
  "dex": "Dexterity",
  "dexterity": "Dexterity",
  "cha": "Charisma",
  "charisma": "Charisma",
  "con": "Constitution",
  "constitution": "Constitution",
  "history": "History",
  "investigation": "Investigation",
  "insight": "Insight",
  "int": "Intelligence",
  "intelligence": "Intelligence",
  "intimidation": "Intimidation",
  "medicine": "Medicine",
  "nature": "Nature",
  "perception": "Perception",
  "performance": "Performance",
  "persuasion": "Persuasion",
  "religion": "Religion",
  "sleightofhand": "Sleight of Hand",
  "survival": "Survival",
  "stealth": "Stealth",
  "str": "Strength",
  "strength": "Strength",
  "wis": "Wisdom",
  "wisdom": "Wisdom"
}

char = character()
ret_name = get("_retainerName")
ret_class = get("_retainerClass")

init = combat()
ret_comb = init.get_combatant(ret_name) if init and ret_name else None
ret_name = "An unknown creature" if "-h" in argv else ret_comb.name if ret_comb else ret_name

cl_info = [c for c in CLASSES if c["name"] == ret_class]
cl_info = cl_info[0] if cl_info else None

check_name = argv[0] if argv else ''
check_name = [name for name in DISPLAY.keys() if check_name in name] if check_name else None
check_name = check_name[0] if check_name else 'acrobatics'

if check_name in ABILITIES.keys():
  ability_name = ABILITIES[check_name]
  check_name = None
else:
  ability_name = argv[1] if argv and len(argv) > 1 else None
  ability_name = [name for name in ABILITIES.keys() if ability_name in name] if ability_name else None
  ability_name = ABILITIES[ability_name[0] if ability_name else SKILLS[check_name]]

formatted = f"{DISPLAY[ability_name]} ({DISPLAY[check_name]})" if check_name else DISPLAY[ability_name]

is_primary = cl_info and ability_name == cl_info["primary"]
is_proficient = "pro" in argv or (cl_info and check_name and check_name in cl_info["skills"])
ret_bonus = 3 + (1 if is_primary else 0) + (2 if is_proficient else 0)

title = f"{char.name} doesn't have a retainer!"
if ret_name:
  title = f"{ret_name} makes a {formatted} check!"
fields = ""
desc = ""

base_bonus = [str(ret_bonus)] + args.get("b") + ([effect.effect["cb"] for effect in ret_comb.effects if "cb" in effect.effect] if ret_comb else [])

reroll = max(1, int(args.last("rr", 1)))
dc = int(args.last("dc")) if args.last("dc") else None

if dc:
  desc = f"""**DC {dc}**
"""

success = 0
failure = 0

for i in range(1, reroll + 1):
  has_adv = "adv" in argv or f"adv{i}" in argv
  has_dis = "dis" in argv or f"dis{i}" in argv
  adv = 1 if has_adv and not has_dis else -1 if has_dis and not has_adv else 0
  adv = 2 if adv == 1 and "ea" in argv else adv
  check = {
    -1: "2d20kl1",
    0: "1d20",
    1: "2d20kh1",
    2: "3d20kh1"
  }[adv]
  check = f"""{check}mi{args.last("mc")}""" if args.last("mc") else check
  bonus = base_bonus + args.get(f"b{i}")
  check_roll = vroll("+".join([check] + bonus))
  if dc:
    if check_roll.total >= dc:
      success += 1
    else:
      failure += 1
  if reroll == 1:
    desc += f"{check_roll}"
  else:
    fields += f"""-f "Check {i}|{check_roll}|inline" """

fields += "\n".join([f"""-f "{field}" """ for field in args.get("f")])

</drac2>
-title "{{args.last("title").replace("[name]", ret_name).replace("[cname]", formatted) if args.last("title") else title}}"
{{f"""-phrase "{args.last("phrase")}" """ if args.last("phrase") else ""}}
{{f"""-desc "{desc}" """ if desc else ""}}
{{fields}}
-footer "{{f"{success} Successes | {failure} Failures" if reroll > 1 and dc else "Success!" if success else "Failure!" if failure  else "!retainer check | kbsletten#5710"}}"
-color <color> -thumb {{get("_retainerImage") if "-h" not in argv else ""}}
