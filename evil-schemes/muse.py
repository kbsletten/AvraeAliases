embed
<drac2>
argv = &ARGS&
args = argparse(argv)

init = combat()
current = init.current if init else None
user = init.get_combatant(args.last("as")) if args.last("as") else current
name = user.name if user else name

title = args.last("title", "!muse - Monster !use").replace("[name]", name)
desc = args.last("desc", "")
error = ""
meta = ""
fields = ""
target_info = ""

damage = args.get("d")
effect = args.last("effect")
duration = int(args.last("duration")) if args.last("duration") else None
end = "end" in args
save = args.last("save", "dex")
dc = int(args.last("dc", 10))
bonuses = args.get("b")
advantage = args.adv()
half = "half" in args
avoid = "avoid" in args
auto_success = "pass" in args
auto_failure = "fail" in args

damage_roll = vroll("+".join(x for x in damage)) if damage else None

meta_lines = [
  f"""**Damage**: {damage_roll}""" if damage_roll else "",
  f"""**Effect**: {effect}""" if effect else "",
  f"""**DC**: {dc}""",
  f"""{save.upper()} save""",
]
meta = "\n".join([x for x in meta_lines if x])

if init:
  for target_expr in args.get("t"):
    target_name, _, target_argv = target_expr.partition("|")
    target_args = argparse(target_argv)

    target = init.get_combatant(target_name)

    if not target:
      continue

    target_damage = target_args.get("d")
    target_effect = target_args.last("effect")
    target_save = target_args.last("save", save)
    target_dc = int(target_args.last("dc", dc))
    target_bonuses = target_args.get("b")
    target_advantage = target_args.adv()
    target_avoid = "avoid" in target_args
    target_auto_success = "pass" in target_args
    target_auto_failure = "fail" in target_args

    total_bonuses = bonuses + target_bonuses
    total_effect = target_effect or effect
    total_advantage = target_advantage or advantage
    total_avoid = target_avoid or avoid
    total_auto_success = target_auto_success or auto_success
    total_auto_failure = target_auto_failure or auto_failure

    target_damage_roll = vroll("+".join(x for x in target_damage)) if target_damage else None

    if target_save:
      base_adv = True if total_advantage == 1 else False if total_advantage == -1 else None
      target_base = target.saves.get(target_save).d20(base_adv=base_adv)
      target_save_roll = vroll("+".join([target_base] + total_bonuses))
      target_success = target_save_roll.total >= target_dc
    else:
      target_success = False

    total_damage = "+".join(x.consolidated() for x in [damage_roll, target_damage_roll] if x)

    if total_avoid:
      total_damage = "" if target_success else f"({total_damage})/2"
    elif target_success:
      total_damage = f"({total_damage})/2" if half else ""
    
    effect_name, _, effect_expr = total_effect.partition("|") if total_effect else ["", None, ""]
    if effect_name and not target_success:
      target.add_effect(effect_name, effect_expr, duration=duration, end=end)

    result_damage = target.damage(total_damage)['damage'] if total_damage else ""

    target_lines = [
      f"""**Extra Damage**: {target_damage_roll}""" if target_damage_roll else "",
      f"""**{save.upper()} Save**: {target_save_roll}; {"Success!" if target_success else "Failure!"}""" if save else "",
      result_damage,
      f"""**Effect**: {effect_name}""" if effect_name and not target_success else ""
    ]
    field = "\n".join([x for x in target_lines if x])
    fields += f"""-f "{target.name}|{field}" """
    target_info += f"{target.name} {target.hp_str()}\n"
</drac2>
-title "{{title}}"
{{f"""-f "Meta|{meta}" """ if meta else ""}}
{{fields if not error else error}}
{{f"""-f "Effect|{desc}" """ if args.last(desc) else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "!muse" """}}
-color <color>