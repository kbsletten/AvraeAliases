embed
<drac2>
using (
  util='f90efd6e-d7ce-44e0-b0c9-0b3438a14271'
)

args = argparse(&ARGS&)
init = combat()

border = max(0, int(args.last("b", 1)))

minX = 100
minY = 100
maxX = 1
maxY = 1

for each in init.combatants if init else []:
  topLeft, bottomRight = util.get_coords(each)
  if not topLeft:
    continue
  x1, y1 = topLeft
  x2, y2 = bottomRight
  minX = max(1, min(minX, x1 - border))
  minY = max(1, min(minY, y1 - border))
  maxX = min(100, max(maxX, x2 + border))
  maxY = min(100, max(maxY, y2 + border))

coord = util.to_alpha(minX, minY)

width = max(1, maxX - minX + 1)
height = max(1, maxY - minY + 1)

map_options, comb = util.get_map_options(init)
map_options["View"] = f"{coord}:{width}x{height}"
if comb:
  util.set_map_options(comb, map_options)

</drac2>
-title "Resizing map to fit"
-desc "{{map_options["View"]}} ({{f"saved on {comb.name}" if comb else "not saved"}})"
-footer "!mx fit | kbsletten#5710"
-color <color>
