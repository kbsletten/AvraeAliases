embed
<drac2>
argv = &ARGS&
args = argparse(argv)

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
ret_image = get("_retainerImage")
ret_hp = char.get_cc("Retainer HP") if char.cc_exists("Retainer HP") else None

set_name = args.last("name", ret_name)
set_class = args.last("class", ret_class)
set_level = int(args.last("level", ret_level))
set_image = args.last("image", ret_image)

ret_hp = min(set_level, set_level if ret_hp is None else ret_hp)

cl_info = [c for c in CLASSES if set_class.lower() in c["name"].lower()]
cl_info = cl_info[0] if cl_info else None

set_class = cl_info["name"] if cl_info else None

title = f"{char.name} doesn't have a retainer!"
if set_name and set_class and set_level:
  title = f"{char.name} has {set_name} a level {set_level} {set_class} retainer!"

if char:
  char.set_cvar("_retainerName", set_name)
  char.set_cvar("_retainerClass", set_class)
  char.set_cvar("_retainerLevel", set_level)
  char.set_cvar("_retainerImage", set_image)
  char.create_cc("Retainer HP", minVal=0, maxVal=set_level, dispType='bubble', reset='long', desc="""A retainer has health levels equal in number to their level. Each time a retainer is hit by an attack, they make a Constitution saving throw. The DC is the average damage from the attack.
If they succeed, they take no damage. If they fail, they lose one health level per die of damage from the attack. If they lose their final health level, they drop unconscious and use the normal rules for dying.
They save against spells just like PCs do, but if they succeed on a save, they lose health levels equal to half the spell level. If they fail they lose heath levels equal to the spell level. So a retainer who saves against a fireball (3rd-level spell) loses 1 health level (3 rounded down).""")
  char.set_cc("Retainer HP", ret_hp)
  char.create_cc("Retainer HD", minVal=0, maxVal=set_level, dispType='bubble', reset='long', reset_by=min(1, int(floor(set_level/2))), desc="""A retainer can spend one or more Hit Dice at the end of a short rest, up to the retainer’s maximum number of Hit Dice, which is equal to the retainer’s level. For each Hit Die spent in this way, the retainer regains one Health Level. At the end of a long rest, a retainer regains spent Hit Dice, up to a number of dice equal to half of the retainer's total number of them (minimum of one die).""")
  char.set_cc("Retainer HD", set_level)

fields = ""

if cl_info:
  fields += f"""-f "HP|{ret_hp}/{set_level}|inline" """
  fields += f"""-f "AC|{cl_info["ac"]}|inline" """
  fields += f"""-f "Primary Ability|{DISPLAY[cl_info["primary"]]}|inline" """
  fields += f"""-f "Saves|{", ".join(DISPLAY[x] for x in cl_info["saves"])}|inline" """
  fields += f"""-f "Skills|{", ".join(DISPLAY[x] for x in cl_info["skills"])}|inline" """
  attack_text = [node for node in cl_info["attack"]["automation"] if node["type"] == "text"]
  fields += f"""-f "{cl_info["attack"]["name"]}|{attack_text[0]["text"] if attack_text else ""}" """
  for action in cl_info["actions"]:
    if set_level < action["level"]:
      continue
    if action["cc"]:
      char.create_cc(action["cc"], minVal=0, maxVal=action["cc_max"], dispType='bubble', reset='long')
    attack_text = [node for node in action["attack"]["automation"] if node["type"] == "text"]
    fields += f"""-f "{action["attack"]["name"]} ({action["cc_max"]}/Day)|{attack_text[0]["text"] if attack_text else ""}
{char.cc_str(action["cc"]) if char and action["cc"] and char.cc_exists(action["cc"]) else ""}" """
</drac2>
-title "{{title}}"
{{fields}}
-footer "!retainer set | kbsletten#5710"
-color <color> -thumb {{get("_retainerImage")}}
