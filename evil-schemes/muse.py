embed
<drac2>
args = argparse("&*&")

init = combat()

title = "!muse - Monster !use"
error = ""
meta = ""
fields = ""
target_info = ""

damage = args.get("d")
effect = args.get("effect")
save = args.last("save")
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
  f"""**DC**: {dc}""" if save else "",
  f"""{save.upper()} save""" if save else "",
  f"""**Bonus**: {"+".join(bonuses)}""" if bonuses else "",
  f"""**Advantage**: {"dis" if advantage == -1 else "adv"}""" if advantage else ""
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
    target_effect = target_args.get("effect")
    target_save = target_args.last("save", save)
    target_dc = int(target_args.last("dc", dc))
    target_bonuses = target_args.get("b")
    target_advantage = target_args.adv()
    target_auto_success = "pass" in args
    target_auto_failure = "fail" in args

    total_bonuses = bonuses + target_bonuses
    total_advantage = target_advantage or advantage
    total_auto_success = target_auto_success or auto_success
    total_auto_failure = target_auto_failure or auto_failure

    target_damage_roll = vroll("+".join(x for x in target_damage)) if target_damage else None

    if target_save:
      base_adv = True if total_advantage == 1 else False if total_advantage == -1 else None
      target_base = target.saves.get(target_save).d20(base_adv=base_adv)
      target_save_roll = vroll("+".join([target_base] + total_bonuses))
      target_success = target_save_roll.total >= target_dc
    else:
      target_success = false

    total_damage = "+".join(x.consolidated() for x in [damage_roll, target_damage_roll] if x)

    result_damage = target.damage(total_damage)['damage'] if total_damage else ""

    target_lines = [
      f"""**Extra Damage**: {target_damage_roll}""" if target_damage_roll else "",
      f"""**{save.upper()} Save**: {target_save_roll}; {"Success!" if target_success else "Failure!"}""",
      f"""**Bonus**: {"+".join(total_bonuses)}""" if total_bonuses else "",
      f"""**Advantage**: {"adv" if total_advantage == 1 else "dis"}""" if total_advantage else "",
      result_damage
    ]
    field = "\n".join([x for x in target_lines if x])
    fields += f"""-f "{target_name}|{field}" """
</drac2>
-title "{{title}}"
{{f"""-f "Meta|{meta}" """ if meta else ""}}
{{fields if not error else error}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "!muse" """}}
-color <color>