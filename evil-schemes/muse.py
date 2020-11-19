embed
<drac2>
abilities = ["strength", "dexterity", "constitution", "wisdom", "intelligence", "charisma"]
abbr = { "str": "strength", "dex": "dexterity", "con": "constitution", "wis": "wisdom", "int": "intelligence", "cha": "charisma" }
sname = { "str": "Strength", "dex": "Dexterity", "con": "Constitution", "wis": "Wisdom", "int": "Intelligence", "cha": "Charisma" }

argv = &ARGS&
args = argparse(argv)

save = args.last('save', 'dex')[:3].lower()
if save not in abbr:
  save = 'dex'

title = args.last("title", "Make a [sname] Save!").replace('[name]', name).replace('[sname]', sname[save])
fields = ""


ability = args.last('a', None)
if ability in abbr:
  ability = abbr[ability]
if ability not in abbr.values():
  ability = None

init = combat()
current = init.current if init else None
stats = current.stats if current else None
default_dc = 8 + stats.prof_bonus + int(stats.get_mod(ability)) if stats and ability else 10

dc = args.last('dc', default_dc)
damage = args.last('d', None)
if current and damage:
  for ab in abilities:
    damage = damage.replace(f'{{{ab}Mod}}', str(current.stats.get_mod(ab)))
targets = args.get("t")
bonuses = ''.join([f"+{bonus}" for bonus in args.get('b')])

damage_roll = vroll(damage) if damage else None

meta = "" if "-h" in argv else f"""**DC**: {dc}
{f"**Damage**: {damage_roll}" if damage_roll else ""}
"""
target_info = ""

for target_expr in targets:
  target_name, _, target_arg = target_expr.partition('|')
  target_argv = target_arg.split(' ')
  target_args = argparse(target_arg)
  target = init.get_combatant(target_name) if init else None
  if target:
    has_adv = "adv" in argv or "adv" in target_argv
    has_dis = "dis" in argv or "dis" in target_argv
    auto_pass = "pass" in argv or "pass" in target_argv
    auto_fail = "fail" in argv or "fail"
    target_save = target.saves.get(save).d20(base_adv=True if has_adv else False if has_dis else None)
    target_bonuses = ''.join([f"+{bonus}" for bonus in target_args.get('b')])
    target_roll = vroll(f"{target_save}{bonuses}{target_bonuses}")
    target_saved = target_roll.total > dc
    target_damage = damage_roll.consolidated() if damage_roll else ""
    if "avoid" in argv or "avoid" in target_argv:
      if target_saved:
        target_damage = f""
      else:
        target_damage = f"({target_damage})/2"
    elif "half" in argv:
      if target_saved:
        target_damage = f"({target_damage})/2"
    elif target_saved:
      target_damage = ""
    target_damage = target.damage(target_damage)["damage"] if target_damage else ""
    fields += f"""-f "{target_name}|**{save.upper()} Save**: {target_roll}; {"Success!" if target_saved else "Failure!"}
{target_damage}" """
    target_info += f"{target.name} {target.hp_str()}\n"
</drac2>
-title "{{title}}"
{{f"""-f "Meta|{meta}" """ if meta else ""}}
{{fields}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "!muse" """}}
-color <color>