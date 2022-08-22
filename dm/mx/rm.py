embed
<drac2>
using (
  util="f90efd6e-d7ce-44e0-b0c9-0b3438a14271"
)

args = argparse(&ARGS&)

init = combat()

fields = ""

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    settings = util.get_settings(each)
    location = settings["Location"] if "Location" in settings else None
    overlay = settings["Overlay"] if "Overlay" in settings else None
    util.set_settings({ key: value for key, value in settings.items() if key not in ["Location", "Overlay"] })
    fields += f"""-f "{each.name}|{f'Removed from {location}' if location else 'Not placed'}{f' (Overlay {overlay})' if overlay else ''}|inline" """
</drac2>
-title "Removing Combatants"
{{fields}}
-footer "!mx rm | kbsletten#5710"
-color <color>
