embed
<drac2>
KEYWORDS = ["damage", "effect"]
ATTACK = ["hit", "crit", "miss"]
SAVE = ["fail", "fail5", "pass"]

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
  json["save"] = { "ability": argv[index] }
  index += 1
  json["save"]["dc"] = int(argv[index])
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

</drac2>
-title "Parsing Attack!"
-desc "{{dump_json(json).replace("\"", "\\\"").replace(": ", ":")}}"
-footer "!custom_attack parse | kbsletten#5710"
