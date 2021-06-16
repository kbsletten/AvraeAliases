embed
<drac2>
argv = &ARGS&
args = argparse(argv)
skill_name = argv[0] if argv else None

NAMES = {
  "acrobatics": "Acrobatics",
  "animalHandling": "Animal Handling",
  "arcana": "Arcana",
  "athletics": "Athletics",
  "deception": "Deception",
  "history": "History",
  "initiative": "Initiative",
  "insight": "Insight",
  "intimidation": "Intimidation",
  "investigation": "Investigation",
  "medicine": "Medicine",
  "nature": "Nature",
  "perception": "Perception",
  "performance": "Performance",
  "persuasion": "Persuasion",
  "religion": "Religion",
  "sleightOfHand": "Sleight of Hand",
  "stealth": "Stealth",
  "survival": "Survival",
  "strength": "Strength",
  "dexterity": "Dexterity",
  "constitution": "Constitituion",
  "intelligence": "Intelligence",
  "wisdom": "Wisdom",
  "charisma": "Charisma"
}

init = combat()
targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    skills = [value for name, value in each.skills if skill_name.lower() in name] if skill_name else None
    skill = skills[0] if skills else None
    if skill:
      fields += f"""-f "{each.name}|{10+skill.value}|inline" """
</drac2>
-title "Passive {{NAMES[skill_name] if skill_name in NAMES else skill_name or "Skill"}}!"
{{fields}}
-footer "!px | kbsletten#5710"