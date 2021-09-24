embed
<drac2>
argv = &ARGS&
attack_name = argv[0] if argv else None
args = argparse(argv[1:])
saved_json = load_json(get("_customAttacks", "{}"))

init = combat()
current = init.current if init else None
if args.last("as"):
  current = init.get_combatant(args.last("as"))

monster_name = current.monster_name if current else None
attack_options = [key for key in saved_json[monster_name].keys() if attack_name.lower() in key.lower()] if monster_name in saved_json else None
attack_name = attack_options[0] if attack_options else attack_name
json = saved_json[monster_name][attack_name] if monster_name in saved_json and attack_name in saved_json[monster_name] else {}

# BEGIN test.py
title = "Custom Attack!"
target_info = ""

modifier = None
hit_bonus = args.get("b")
damage_bonus = args.get("d")

if current:
  title = f"{current.name} attacks with a {attack_name}!"
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
  target_combatant = [init.get_combatant(target_name)] if init and init.get_combatant(target_name) else []
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
    
    damage_roll = None
    effect = None

    attack_roll = None
    damage_multiply = False
    if "attack" in json:
      attack_roll = vroll("+".join([
        "3d20kh1" if modifier == 2 else
        "2d20kh1" if modifier == 1 else
        "2d20kl1" if modifier == -1 else
        "1d20",
        json["attack"]["bonus"]
      ] + hit_bonus))
      crit = attack_roll.result.crit == 1
      hit = crit or attack_roll.result.crit != 2 and attack_roll.total >= target.ac
      if hit:
        damage_multiply = crit
        damage_roll = "+".join([json["attack"]["hit"]["damage"]] + damage_bonus) if "damage" in json["attack"]["hit"] else None
        if crit and "crit" in json["attack"]:
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
      fail = save_roll.total < save_dc
      fail5 = save_roll.total < save_dc - 4 # DC 11: 6 is failing by 5
      if fail:
        if save_damage:
          damage_roll = save_damage.consolidated() if save_damage else None
        elif "fail" in json["save"] and "damage" in json["save"]["fail"]:
          damage_roll = "+".join(x for x in [damage_roll, json["save"]["fail"]["damage"]] if x)
        if fail5 and "fail5" in json["save"]:
          if "effect" in json["save"]["fail5"]:
            effect = json["save"]["fail5"]["effect"]
        elif "fail" in json["save"] and "effect" in json["save"]["fail"]:
            effect = json["save"]["fail"]["effect"]
      elif "pass" in json["save"]:
        if save_damage:
          damage_roll = json["save"]["pass"]["damage"].replace("{Damage}", save_damage.consolidated() if save_damage else "0") if "damage" in json["save"]["pass"] else None
        elif "damage" in json["save"]["pass"]:
          damage_roll = "+".join(x for x in [damage_roll, json["save"]["pass"]["damage"]] if x)
        if "effect" in json["save"]["pass"]:
            effect = json["save"]["pass"]["effect"]

    effect_name, _, effect_args = effect.partition("|") if effect else [None, None, None]
    target.add_effect(effect_name, effect_args)
    damage = target.damage(damage_roll, crit=damage_multiply)["damage"] if damage_roll else None
    summary = "\n".join(x for x in [
      f"**To Hit**: {attack_roll}" if attack_roll else "",
      f"""**{save_ability.upper()} save**: {save_roll}; {"Success" if save_roll.total >= save_dc else "Failure"}!""" if save_roll else "",
      damage if damage else 'Miss' if attack_roll else "",
      f"**Effect**: {effect_name}" if effect_name else ""
    ] if x)
    fields += f"""-f "{target.name}|{summary}" """
    target_info += f"{target.name} {target.hp_str()}\n" if damage else ""
#END test.py

</drac2>
-title "{{title}}"
{{fields}}
-footer "{{target_info or "!custom_attack | kbsletten#5710"}}"
