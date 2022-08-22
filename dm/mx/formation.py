embed
<drac2>
using (
  util="f90efd6e-d7ce-44e0-b0c9-0b3438a14271"
)

positions = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

argv = &ARGS&
args = argparse(argv)

init = combat()

fields = ""

for group_expr in args.get("t"):
  group_name, _, location = group_expr.partition("|")
  group = init.get_group(group_name)
  gX, gY = util.parse_coord(location)
  pos = 0
  group_fields = ""
  for comb in group.combatants:
    x, y = positions[pos]
    x += gX
    y += gY
    pos += 1
    coord = util.to_alpha(x, y)
    settings = util.get_settings(comb)
    settings["Location"] = coord
    util.set_settings(comb, settings)
    group_fields += f"{comb.name} ({coord})\n"
  fields += f""" -f "{group.name}|{group_fields}" """
    
</drac2>
-title "Get in formation!"
{{fields}}
-footer "!mx formation | kbsletten#5710"
-color <color>
