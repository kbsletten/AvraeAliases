embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()

targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

delete_notes = args.get("delete")
edit_notes = [note.split(": ", maxsplit=1) for note in args.get("edit") if ": " in note]
add_notes = args.get("add")

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    notes = [note.split(": ", maxsplit=1) if ": " in note else [note, None] for note in (each.note or "").split(" | ") if note]
    notes = [note for note in notes if not any(delete in note[0] for delete in delete_notes)]
    for name, value in edit_notes:
      notes = [[note[0], value] if name in note[0] else note for note in notes]
    each.set_note(" | ".join([f"{note[0]}: {note[1]}" if note[1] else note[0] for note in notes] + add_notes) if notes or add_notes else None)
    fields += f"""-f "{each.name}|{each.note or "(none)"}" """
</drac2>
-title "Updating Notes"
{{fields}}
-footer "!nx | kbsletten#5710"
