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
  notes = [note[10:] for note in each.note.split(' | ') if note.startswith("Location: ")] if each.note else None
  location = notes[0] if notes else None
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
  minX = max(1, min(minX, horizontal - border))
  minY = max(1, min(minY, vertical - border))
  maxX = min(100, max(maxX, horizontal + border))
  maxY = min(100, max(maxY, vertical + border))

coord = ""
n = minX
for _ in range(0, 3):
  if n > 0:
    remainder = (n - 1) % 26
    n = (n - 1) // 26
    coord = CHARS[remainder] + coord

width = max(1, maxX - minX + 1)
height = max(1, maxY - minY + 1)

</drac2>
-title "Resizing map to fit"
-f "Resize|`!map -view \"{{coord}}{{minY}}:{{width}}x{{height}}\"`"
-footer "!mx | kbsletten#5710"
-color <color>
