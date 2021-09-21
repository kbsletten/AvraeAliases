embed
<drac2>
KEYWORDS = ["damage", "healing", "thp", "maxhp", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail5", "fail", "pass"]

argv = &ARGS&
json = {}
index = 0
if index < len(argv) and argv[index] == "attack":
  index += 1
  json["attack"] = { "bonus": argv[index] }
  index += 1
  for attack in ATTACK:
    if index < len(argv) and argv[index] == attack:
      index += 1
      json["attack"][attack] = {}
      for keyword in KEYWORDS:
        if index < len(argv) and argv[index] == keyword:
          index += 1
          json["attack"][attack][keyword] = argv[index]
          index += 1
if index < len(argv) and argv[index] == "save":
  index += 1
  json["save"] = { "save": argv[index] }
  index += 1
  json["save"]["dc"] = argv[index]
  index += 1
  for save in SAVE:
    if index < len(argv) and argv[index] == save:
      index += 1
      json["save"][save] = {}
      for keyword in KEYWORDS:
        if index < len(argv) and argv[index] == keyword:
          index += 1
          json["save"][save][keyword] = argv[index]
          index += 1
      if index < len(argv) and argv[index] == "half":
        index += 1
        json["save"][save]["damage"] = "({Damage})/2"
if index < len(argv) and argv[index] == "self":
  index += 1
  json["self"] = {}
  for keyword in KEYWORDS:
    if index < len(argv) and argv[index] == keyword:
      index += 1
      json["self"][keyword] = argv[index]
      index += 1
for keyword in KEYWORDS:
  if index < len(argv) and argv[index] == keyword:
    index += 1
    json[keyword] = argv[index]
    index += 1
</drac2>
-title "Parsing Attack!"
-desc "{{dump_json(json).replace("\"", "\\\"").replace(": ", ":")}}"
-footer "!parse | kbsletten#5710"
