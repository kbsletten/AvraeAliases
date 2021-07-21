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
DISPLAY = {
  "dex": "Dexterity",
  "dexterity": "Dexterity",
  "cha": "Charisma",
  "charisma": "Charisma",
  "con": "Constitution",
  "constitution": "Constitution",
  "int": "Intelligence",
  "intelligence": "Intelligence",
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

save_name = argv[0] if argv else ''
save_name = [name for name in DISPLAY.keys() if save_name in name] if save_name else None
save_name = save_name[0] if save_name else 'dex'

formatted = DISPLAY[save_name]

is_proficient = "pro" in argv or (cl_info and save_name and save_name in cl_info["saves"])
ret_bonus = 3 + (3 if is_proficient else 0)

title = f"{char.name} doesn't have a retainer!"
if ret_name:
  title = f"{ret_name} makes a {formatted} save!"
fields = ""
desc = ""

base_bonus = [str(ret_bonus)] + args.get("b") + ([effect.effect["sb"] for effect in ret_comb.effects if "sb" in effect.effect] if ret_comb else [])

reroll = max(1, int(args.last("rr", 1)))
dc = int(args.last("dc")) if args.last("dc") else None

if dc:
  desc = f"""**DC {dc}**
"""

success = 0
failure = 0

level = max(0, int(args.last("l")) if args.last("l") else 0)
harm = 0

for i in range(1, reroll + 1):
  has_adv = "adv" in argv or f"adv{i}" in argv
  has_dis = "dis" in argv or f"dis{i}" in argv
  adv = 1 if has_adv and not has_dis else -1 if has_dis and not has_adv else 0
  adv = 2 if adv == 1 and "ea" in argv else adv
  save = {
    -1: "2d20kl1",
    0: "1d20",
    1: "2d20kh1",
    2: "3d20kh1"
  }[adv]
  bonus = base_bonus + args.get(f"b{i}")
  check_roll = vroll("+".join([save] + bonus))
  if dc:
    if check_roll.total >= dc:
      success += 1
      harm += int(floor(level / 2))
    else:
      failure += 1
      harm += level
  if reroll == 1:
    desc += f"{check_roll}"
  else:
    fields += f"""-f "Check {i}|{check_roll}|inline" """

fields += "\n".join([f"""-f "{field}" """ for field in args.get("f")])

if harm and char and char.cc_exists("Retainer HP"):
  char.mod_cc("Retainer HP", -harm)

</drac2>
-title "{{args.last("title").replace("[name]", ret_name).replace("[sname]", formatted) if args.last("title") else title}}"
{{f"""-phrase "{args.last("phrase")}" """ if args.last("phrase") else ""}}
{{f"""-desc "{desc}" """ if desc else ""}}
{{fields}}
-footer "{{f"""{ret_name} {char.cc_str("Retainer HP")} (-{harm})""" if level and char and char.cc_exists("Retainer HP") else f"{success} Successes | {failure} Failures" if reroll > 1 and dc else "Success!" if success else "Failure!" if failure  else "!retainer save | kbsletten#5710"}}"
-color <color> -thumb {{get("_retainerImage") if "-h" not in argv else ""}}
