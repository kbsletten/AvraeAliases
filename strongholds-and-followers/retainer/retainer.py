embed
<drac2>
GVARS = load_json(get_gvar("c1ee7d0f-750d-4f92-8d87-70fa22c07a81"))
CLASSES = [load_json(get_gvar(gvar)) for gvar in GVARS]
DISPLAY = {
  "acrobatics": "Acrobatics",
  "animalhandling": "Animal Handling",
  "athletics": "Athletics",
  "arcana": "Arcana",
  "deception": "Deception",
  "dex": "Dexterity",
  "dexterity": "Dexterity",
  "cha": "Charisma",
  "charisma": "Charisma",
  "con": "Constitution",
  "constitution": "Constitution",
  "history": "History",
  "investigation": "Investigation",
  "insight": "Insight",
  "int": "Intelligence",
  "intelligence": "Intelligence",
  "intimidation": "Intimidation",
  "medicine": "Medicine",
  "nature": "Nature",
  "perception": "Perception",
  "performance": "Performance",
  "persuasion": "Persuasion",
  "religion": "Religion",
  "sleightofhand": "Sleight of Hand",
  "survival": "Survival",
  "stealth": "Stealth",
  "str": "Strength",
  "strength": "Strength",
  "wis": "Wisdom",
  "wisdom": "Wisdom"
}

char = character()
ret_name = get("_retainerName")
ret_class = get("_retainerClass")
ret_level = int(get("_retainerLevel", 0))
ret_hp = char.get_cc("Retainer HP") if char and char.cc_exists("Retainer HP") else 0

title = f"{char.name} doesn't have a retainer!"
if ret_name and ret_class and ret_level:
  title = f"{char.name} has {ret_name} a level {ret_level} {ret_class} retainer!"

cl_info = [c for c in CLASSES if c["name"] == ret_class]
cl_info = cl_info[0] if cl_info else None

fields = ""

if cl_info:
  fields += f"""-f "HP|{ret_hp}/{ret_level}|inline" """
  fields += f"""-f "AC|{cl_info["ac"]}|inline" """
  fields += f"""-f "Primary Ability|{DISPLAY[cl_info["primary"]]}|inline" """
  fields += f"""-f "Saves|{", ".join(DISPLAY[x] for x in cl_info["saves"])}|inline" """
  fields += f"""-f "Skills|{", ".join(DISPLAY[x] for x in cl_info["skills"])}|inline" """
  attack_text = [node for node in cl_info["attack"]["automation"] if node["type"] == "text"]
  fields += f"""-f "{cl_info["attack"]["name"]}|{attack_text[0]["text"] if attack_text else ""}" """
  for action in cl_info["actions"]:
    if ret_level < action["level"]:
      continue
    attack_text = [node for node in action["attack"]["automation"] if node["type"] == "text"]
    fields += f"""-f "{action["attack"]["name"]} ({action["cc_max"]}/Day)|{attack_text[0]["text"] if attack_text else ""}
{char.cc_str(action["cc"]) if char and action["cc"] and char.cc_exists(action["cc"]) else ""}" """

</drac2>
-title "{{title}}"
{{fields}}
-footer "!retainer | kbsletten#5710"
-color <color> -thumb {{get("_retainerImage")}}
