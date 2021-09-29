embed
<drac2>
# BEGIN parse.py
KEYWORDS = ["damage", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail", "fail5", "pass"]

argv = &ARGS&
json = {}
index = 0

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

title = "Custom Attack!"
target_info = ""

init = combat()
current = init.current if init else None

modifier = None
hit_bonus = args.get("b")
damage_bonus = args.get("d")

if current:
  title = f"{current.name} makes a Custom Attack!"
  for effects in current.effects:
    if "adv" in effects.effect:
      modifier = 1 if modifier == None or modifier == 1 else 0
    if "dis" in effects.effect:
      modifier = -1 if modifier == None or modifier == -1 else 0
    if "b" in effects.effect:
      hit_bonus = hit_bonus + [effects.effect["b"]]
    if "d" in effects.effect:
      damage_bonus = damage_bonus + [effects.effect["d"]]

if "adv" in argv:
  modifier = 1 if modifier == None or modifier == 1 else 0
if "dis" in argv:
  modifier = -1 if modifier == None or modifier == -1 else 0

fields = ""

save_dc = None
save_damage = None
save_ability = None
if "save" in json:
  save_ability = json["save"]["ability"] if "ability" in json["save"] else "dex"
  save_dc = int(json["save"]["dc"]) if "dc" in json["save"] else 10
  if "fail" in json["save"] and "damage" in json["save"]["fail"] and "attack" not in json:
    save_damage = vroll(json["save"]["fail"]["damage"])

if save_dc or save_damage:
  meta = "\n".join(x for x in [
    f"**DC**: {save_dc}" if save_dc else "",
    f"**Damage**: {save_damage}" if save_damage else ""
  ] if x)
  fields += f"""-f "Meta|{meta}" """

for target_expr in args.get("t"):
  target_name, _, target_argv = target_expr.partition("|")
  target_group = init.get_group(target_name) if init else None
  target_combatant = [init.get_combatant(target_name)] if [init.get_combatant(target_name)] else []
  target_combatants = target_group.combatants if target_group else target_combatant if init else []
  for target in target_combatants:
    hit = False
    save_bonus = args.get("sb")
    save_modifier = None
    for effects in target.effects:
      if "sadv" in effects.effect and (effects.effect["sadv"] == "all" or effects.effect["sadv"] == save_ability):
        save_modifier = 1 if save_modifier == None or save_modifier == 1 else 0
      if "sdis" in effects.effect and (effects.effect["sdis"] == "all" or effects.effect["sdis"] == save_ability):
        save_modifier = -1 if save_modifier == None or save_modifier == -1 else 0
      if "sb" in effects.effect:
        save_bonus = save_bonus + [effects.effect["sb"]]
    if "sadv" in argv:
      save_modifier = 1 if save_modifier == None or save_modifier == 1 else 0
    if "sdis" in argv:
      save_modifier = -1 if save_modifier == None or save_modifier == -1 else 0
    
    summary = []
    for _ in range(0, int(args.last("rr", 1))):
      damage_roll = None
      effect = None
      bonus_damage_roll = None
      attack_roll = None
      crit = False

      if "attack" in json:
        attack_roll = vroll("+".join([
          "3d20kh1" if modifier == 2 else
          "2d20kh1" if modifier == 1 else
          "2d20kl1" if modifier == -1 else
          "1d20",
          json["attack"]["bonus"]
        ] + hit_bonus))
        auto_hit = "hit" in argv
        auto_crit = "crit" in argv
        auto_miss = "miss" in argv
        crit = auto_crit or attack_roll.result.crit == 1
        hit = auto_hit or not auto_miss and (attack_roll.result.crit == 1 or attack_roll.result.crit != 2 and attack_roll.total >= target.ac)
        if hit:
          damage_roll = "+".join([json["attack"]["hit"]["damage"]] + damage_bonus) if "damage" in json["attack"]["hit"] else None
          if crit and "crit" in json["attack"]:
            if "damage" in json["attack"]["crit"]:
              bonus_damage_roll = json["attack"]["crit"]["damage"]
            if "effect" in json["attack"]["crit"]:
              effect = json["attack"]["crit"]["effect"]
          elif "effect" in json["attack"]["hit"]:
            effect = json["attack"]["hit"]["effect"]
        elif "miss" in json["attack"]:
          damage_roll = "+".join([json["attack"]["miss"]["damage"]] + damage_bonus) if "damage" in json["attack"]["miss"] else None
          if "effect" in json["attack"]["miss"]:
            effect = json["attack"]["miss"]["effect"]

      save_roll = None
      if "save" in json and (hit or "attack" not in json):
        save_roll = target.save(save_ability, adv=True if save_modifier == 1 else False if save_modifier == -1 else None)
        auto_pass = "pass" in argv
        auto_fail = "fail" in argv
        auto_fail5 = "fail4" in argv
        fail = auto_fail or not auto_pass and save_roll.total < save_dc
        fail5 = fail and auto_fail5 or save_roll.total < save_dc - 4 # DC 11: 6 is failing by 5
        if fail:
          if save_damage:
            damage_roll = save_damage.consolidated() if save_damage else None
          elif "fail" in json["save"] and "damage" in json["save"]["fail"]:
            bonus_damage_roll = "+".join(x for x in [bonus_damage_roll, json["save"]["fail"]["damage"]] if x)
          if fail5 and "fail5" in json["save"]:
            if "effect" in json["save"]["fail5"]:
              effect = json["save"]["fail5"]["effect"]
          elif "fail" in json["save"] and "effect" in json["save"]["fail"]:
              effect = json["save"]["fail"]["effect"]
        elif "pass" in json["save"]:
          if save_damage:
            damage_roll = json["save"]["pass"]["damage"].replace("{Damage}", save_damage.consolidated() if save_damage else "0") if "damage" in json["save"]["pass"] else None
          elif "damage" in json["save"]["pass"]:
            bonus_damage_roll = "+".join(x for x in [bonus_damage_roll, json["save"]["pass"]["damage"]] if x)
          if "effect" in json["save"]["pass"]:
              effect = json["save"]["pass"]["effect"]

      effect_name, _, effect_args = effect.partition("|") if effect else [None, None, None]
      target.add_effect(effect_name, effect_args)
      damage = target.damage(damage_roll, crit=crit)["damage"] if damage_roll else None
      bonus_damage = target.damage(bonus_damage_roll)["damage"] if bonus_damage_roll else None
      summary = summary + [
        "\n".join(x for x in [
          f"""**To Hit**: {"Automatic hit!" if auto_hit else "Automatic miss!" if auto_miss else attack_roll}""" if attack_roll else "",
          damage if damage else '**Miss!**' if attack_roll else "",
          f"""**{save_ability.upper()} save**: {"Automatic failure!" if auto_fail else "Automatic success!" if auto_pass else f'{save_roll}; {"Success!" if save_roll.total >= save_dc else "Failure!"}'}""" if save_roll else "",
          f"**Effect**: {effect_name}" if effect_name else "",
          bonus_damage if bonus_damage else ""
        ] if x)
      ]
    result = summary[0] if len(summary) == 1 else "\n\n".join(f"**__Attack {i+1}__**\n{x}" for i, x in enumerate(summary))
    fields += f"""-f "{target.name}|{result or "(no effect)"}" """
    target_info += f"{target.name} {target.hp_str()}\n" if damage else ""

</drac2>
-title "{{title}}"
{{fields}}
-footer "{{target_info or "!custom_attack test | kbsletten#5710"}}"
