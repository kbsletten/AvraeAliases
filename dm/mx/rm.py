embed
<drac2>
args = argparse(&ARGS&)

init = combat()

fields = ""

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    notes = each.note.split(' | ') if each.note else None
    other_notes = [note for note in notes if not note.startswith("Location:")] if notes else None
    location = [note[10:] for note in notes if note.startswith("Location:")] if notes else None
    location = location[0] if location else None
    each.set_note(' | '.join(other_notes) if other_notes else None)
    fields += f"""-f "{each.name if each else name}|{f'Removed from {location}' if location else 'Not placed'}|inline" """
</drac2>
-title "Removing Combatants"
{{fields}}
-footer "!mx rm | kbsletten#5710"
-color <color>
