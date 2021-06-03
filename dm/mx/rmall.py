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
    notes = each.note.split(' | ') if each.note else None
    other_notes = [note for note in notes if not note.startswith("Location:") and not note.startswith("Overlay:")] if notes else None
    location = [note[10:] for note in notes if note.startswith("Location:")] if notes else None
    location = location[0] if location else None
    overlay = [note[9:] for note in notes if note.startswith("Overlay:")] if notes else None
    overlay = overlay[0] if overlay else None
    each.set_note(' | '.join(other_notes) if other_notes else None)
    fields += f"""-f "{each.name if each else name}|{f'Removed from {location}' if location else 'Not placed'}{f' (Overlay {overlay})' if overlay else ''}|inline" """
</drac2>
-title "Removing All Combatants"
{{fields}}
-footer "!mx rmall | kbsletten#5710"
-color <color>
