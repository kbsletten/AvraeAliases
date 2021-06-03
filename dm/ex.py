embed
<drac2>
args = argparse(&ARGS&)

init = combat()
targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    if each.effects:
      fields += f"""-f "{each.name}|"""
      for effect in each.effects:
        fields += f"{effect.name}\n"
        each.remove_effect(effect.name)
      fields += """" """
</drac2>
-title "Removing Effects"
{{fields}}
-footer "!ex | kbsletten#5710"
-color <color>
