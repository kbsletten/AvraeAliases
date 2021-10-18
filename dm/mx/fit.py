embed
<drac2>
args = argparse(&ARGS&)
init = combat()

border = max(0, int(args.last("b", 1)))

minX = 100
minY = 100
maxX = 1
maxY = 1

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMS = "0123456789"

for each in init.combatants if init else []:
  location = (([note[len("Location: "):] for note in each.note.split(' | ') if note.startswith("Location: ")] if each.note else []) + [None])[0]
  size = (([note[len("Size :"):len("Size :")+1].lower() for note in each.note.split(' | ') if note.startswith("Size: ")] if each.note else []) + [None])[0]
  if not location:
    continue
  vertical = 0
  horizontal = 0
  if location:
    for ch in location:
      if ch in CHARS:
        horizontal = horizontal * 26 + CHARS.index(ch) + 1
      elif ch in NUMS:
        vertical = vertical * 10 + NUMS.index(ch)
  diameter = 4 if size == "c" else 3 if size == "g" else 2 if size == "h" else 1 if size == "l" else 0
  minX = max(1, min(minX, horizontal - border))
  minY = max(1, min(minY, vertical - border))
  maxX = min(100, max(maxX, horizontal + border + diameter))
  maxY = min(100, max(maxY, vertical + border + diameter))

coord = ""
n = minX
for _ in range(0, 3):
  if n > 0:
    remainder = (n - 1) % 26
    n = (n - 1) // 26
    coord = CHARS[remainder] + coord

width = max(1, maxX - minX + 1)
height = max(1, maxY - minY + 1)

for comb in init.combatants if init else []:
  map_effect = comb.get_effect("map")
  if not map_effect:
    continue
  map_parameters = [f"View: {coord}{minY}:{width}x{height}"] + [effect for effect in map_effect.effect["attack"]["details"].split(" ~ ") if not effect.startswith("View: ")]
  comb.add_effect("map", f"""-attack "||{" ~ ".join(map_parameters)}" """)

</drac2>
-title "Resizing map to fit"
-desc "{{coord}}{{minY}}:{{width}}x{{height}}"
-footer "!mx | kbsletten#5710"
-color <color>
