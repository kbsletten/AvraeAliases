embed
<drac2>
args = argparse("&*&")
command = "&1&"

init = combat()

dc = int(args.last("dc")) if args.last("dc") else None

fields = f"""-f "Meta|**DC**: {dc}
**Healing**: 1" """
errors = ""
target_info = ""

if not dc:
  errors += "Missing DC (`-dc DC`)\n"
elif init:
  for target_name in args.get("t"):
    target = init.get_combatant(target_name)
    if not target:
      continue
    target_save_roll = vroll(target.saves.get("con").d20())
    target_success = target_save_roll.total >= dc
    target_healed = target_success and target.hp < 1
    if target_healed:
      target.set_hp(1)
    fields += f"""-f "{target.name}|**CON Save**: {target_save_roll}; {"Success!" if target_success else "Failure!"}
{f"**Healing**: 1" if target_healed else "No effect"}" """
    target_info += f"{target.name} {target.hp_str()}\n"
fields += f"""-f "Effect|If damage reduces the creature to 0 hit points, it must make a Constitution saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the creature drops to 1 hit point instead." """
</drac2>
-title "Undead Fortitude"
{{f"""-f "Errors|{errors}" """ if errors else fields}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Undead Fortitude" """}}
-color <color>
