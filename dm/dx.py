embed
<drac2>
args = argparse(&ARGS&)

init = combat()
damage_roll = vroll(f"({'+'.join(args.get('d'))})/2" if "half" in args else '+'.join(args.get("d")))

fields = f"""-f "Meta|**Damage:** {damage_roll}" """

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    damage = each.damage(damage_roll.consolidated())["damage"]
    fields += f"""-f "{each.name} {each.hp_str()}|{damage}" """

</drac2>
-title "Applying Damage"
{{fields}}
-footer "!dx | kbsletten#5710"
-color <color>
