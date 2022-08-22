embed
<drac2>
using (
  util="f90efd6e-d7ce-44e0-b0c9-0b3438a14271"
)
args = argparse(&ARGS&)

init = combat()
targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants if each.controller == ctx.author.id] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    if each.hp is not None and each.hp <= 0:
      settings = util.get_settings(each)
      location = settings["Location"] if "Location" in settings else None
      overlay = settings["Overlay"] if "Overlay" in settings else None
      util.set_settings({ key: value for key, value in settings.items() if key not in ["Location", "Overlay"] })
      fields += f"""-f "{each.name}|{f'Removed from {location}' if location else 'Not placed'}{f' (Overlay {overlay})' if overlay else ''}|inline" """
</drac2>
-title "Removing Dead Combatants"
{{fields}}
-footer "!mx rmdead | kbsletten#5710"