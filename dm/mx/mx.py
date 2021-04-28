embed
<drac2>
args = argparse(&ARGS&)

init = combat()
vertical_movement = -int(args.last("up", 0)) if "up" in args else int(args.last("down", 0))
horizontal_movement = int(args.last("right", 0)) if "right" in args else -int(args.last("left", 0))
fields = ""

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMS = "0123456789"

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    notes = [note[10:] for note in each.note.split(' | ') if note.startswith("Location: ")] if each.note else None
    location = notes[0] if notes else None
    vertical = 0
    horizontal = 0
    if location:
      for ch in location:
        if ch in CHARS:
          horizontal = horizontal * 26 + CHARS.index(ch) + 1
        elif ch in NUMS:
          vertical = vertical * 10 + NUMS.index(ch)
      vertical_destination = vertical + vertical_movement
      horizontal_destination = horizontal + horizontal_movement
      coord = ""
      n = horizontal_destination
      for _ in range(0, 3):
        if n > 0:
          remainder = (n - 1) % 26
          n = (n - 1) // 26
          coord = CHARS[remainder] + coord
      new_location = f"Location: {coord}{vertical_destination}"
      each.set_note(' | '.join([new_location if note.startswith("Location: ") else note for note in each.note.split(' | ')] if each.note else new_location))
      fields += f"""-f "{each.name}|{location} -> {coord}{vertical_destination}|inline" """

</drac2>
-title "Moving by ({{horizontal_movement}}, {{vertical_movement}}) [{{0 if not horizontal_movement + vertical_movement else int(sqrt(horizontal_movement * horizontal_movement + vertical_movement * vertical_movement)) * 5}} ft.]"
{{fields}}
-footer "!mx | kbsletten#5710"
-color <color>
