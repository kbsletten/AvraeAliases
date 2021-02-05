embed
<drac2>
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
  "constitution": "Constitution",
  "intelligence": "Intelligence",
  "wisdom": "Wisdom",
  "charisma": "Charisma"
}

argv = &ARGS&
args = argparse(argv)
skill = argv[0] if argv else ""

init = combat()
party = init.combatants if init else []
dc = int(args.last("dc")) if args.last("dc") else None
proficient = "prof" in argv

fields = f"""-f "Meta|**DC**: {dc}" """ if dc else ""
passed = 0

if skill:
  for member in party:
    member_skill = member.skills[skill]
    if proficient and member_skill.prof < 1:
      fields += f"""-f "{member.name}|Not proficient." """
      continue
    member_skill_roll = vroll(member_skill.d20())
    member_passed = "; Pass" if dc and member_skill_roll.total >= dc else "; Fail" if dc else ""
    fields += f"""-f "{member.name}|{member_skill_roll}{member_passed}" """
    if dc and member_skill_roll.total >= dc:
      passed += 1

</drac2>
-title "{{init.name if init and init.name else "The party"}} makes a group {{NAMES[skill] if skill in NAMES else ""}} check!"
{{fields}}
-footer "{{f"{init.name if init and init.name else 'Party'} <{passed}/{len(party)}> | " if dc else ""}}!gc"