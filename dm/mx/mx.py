embed
<drac2>
using (
  util="f90efd6e-d7ce-44e0-b0c9-0b3438a14271"
)

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
    settings = util.get_settings(each)
    location = settings["Location"] if "Location" in settings else None
    if not location:
      continue
    horizontal, vertical = util.parse_coords(location)
    vertical_destination = vertical + vertical_movement
    horizontal_destination = horizontal + horizontal_movement
    coord = util.to_alpha(horizontal_destination, vertical_destination)
    settings["Location"] = coord
    util.set_settings(each, settings)
    fields += f"""-f "{each.name}|{location} -> {coord}|inline" """

</drac2>
-title "Moving by ({{horizontal_movement}}, {{vertical_movement}}) [{{0 if not horizontal_movement + vertical_movement else int(sqrt(horizontal_movement * horizontal_movement + vertical_movement * vertical_movement)) * 5}} ft.]"
{{fields}}
-footer "!mx | kbsletten#5710"
-color <color>
