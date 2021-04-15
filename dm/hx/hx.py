embed
<drac2>
argv = &ARGS&
args = argparse(argv)

init = combat()
healing_roll = vroll(argv[0] if argv and argv[0] != "-t" else "0")

fields = f"""-f "Meta|**Healing:** {healing_roll}" """

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    each.modify_hp(healing_roll.total, overflow="over" in argv)
    fields += f"""-f "{each.name} {each.hp_str()}|**Healing:** {healing_roll}" """

</drac2>
-title "Modifying HP"
{{fields}}
-footer "!hx | kbsletten#5710"
