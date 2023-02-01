multiline
<drac2>
args = argparse(&ARGS&)

init = combat()

fields = ""

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    fields += f"""!init remove {each.name}\n"""
</drac2>
{{fields}}
