embed
<drac2>
argv = &ARGS&
args = argparse(argv)

effect_name = argv[0] if len(argv) > 0 else "Not Found"

init = combat()
targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    effect = each.get_effect(effect_name)
    fields += f"""-f "{each.name}|{effect.name if effect else "(not found)"}|inline" """
    if effect:
      each.remove_effect(effect.name)
</drac2>
-title "Removing Effects"
{{fields}}
-footer "!ex remove | kbsletten#5710"
-color <color>
