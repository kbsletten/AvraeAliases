embed
<drac2>
argv = &ARGS&
flags = [arg for arg in argv if arg.startswith("-")]
first_arg = argv.index(flags[0]) if flags else len(argv)
arg_damage = [" ".join(argv[:first_arg])] if first_arg else []
args = argparse(argv[first_arg:])

init = combat()
damage_expr = "+".join(arg_damage + args.get("d"))
damage_roll = vroll(f"({damage_expr})/2" if "half" in args else damage_expr)

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
