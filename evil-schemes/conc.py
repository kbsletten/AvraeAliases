embed
<drac2>
args = argparse("&*&")
command = "&1&"

init = combat()

dc = int(args.last("dc", 10))
bonuses = args.get("b")
advantage = args.adv()
auto = 1 if "pass" in args else 2 if "fail" in args else None

fields = f"""-f "Meta|**DC**: {dc}" """
errors = ""

if command == "help":
  fields += """-f "Usage|**Make a Concentration Check**
`!conc -dc 12 -t Player1`
**Make Multiple Concentration Checks**
`!conc -dc 17 -t Player1 -t Player2`" """
elif init:
  for target_expr in args.get("t"):
    target_name, _, target_argv = target_expr.partition("|")
    target_args = argparse(target_argv)

    target_bonuses = target_args.get("b")
    target_advantage = target_args.adv()
    target_auto = 1 if "pass" in target_args else 2 if "fail" in target_args else None

    total_bonuses = bonuses + target_bonuses
    total_advantage = target_advantage or advantage
    total_auto = target_auto or auto

    target = init.get_combatant(target_name)

    if total_auto is None and target.hp > 0:
      base_adv = True if total_advantage == 1 else False if total_advantage == -1 else None
      target_base = target.saves.get("con").d20(base_adv=base_adv)
      target_save_roll = vroll("+".join([target_base] + total_bonuses))
      target_success = target_save_roll.total >= dc
      target_message = f"""{target_save_roll}; {"Success!" if target_success else "Failure!"}"""
    else:
      target_success = total_auto == 1
      target_message = "Automatic Success!" if target_success else "Automatic Fail!"
    effect_desc = ""
    if not target_success:
      conc_effects = [e for e in target.effects if e.conc]
      target_effect = conc_effects[0] if conc_effects else None
      if target_effect:
        effect_desc = target_effect.name
        if target_effect.children:
          effect_desc += f" (+ {len(target_effect.children)} child effects)"
        target.remove_effect(target_effect.name)
    fields += f"""-f "{target.name}|**CON Save**: {target_message}
{f"**Removed effect**: {effect_desc}" if effect_desc else "No effect"}" """
</drac2>
-title "Concentration Check"
{{f"""-f "Errors|{errors}" """ if errors else fields}}
-footer "Concentration Check | PHB 203"
-color <color>