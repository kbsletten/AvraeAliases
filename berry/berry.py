embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if len(argv) > 0 else "help"

number = int(args.last("n", default=1))
article = "a" if number == 1 else str(number)
plural = "y" if number == 1 else "ies"

current_character = character()
current_spellbook = current_character.spellbook if current_character else None
current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

cc = "Goodberry"
has_cc = current_character.cc_exists(cc)

title = "Goodberry"
description = ""
fields = ""
target_info = ""
help = """**To create the CC**
!berry cc
**To cast goodberry and keep the berries**
!berry cast [-l LEVEL]
**To use a berry on yourself**
!berry eat [-n NUMBER]
**Give a berry to another character**
!berry give -t TARGET [-n NUMBER]
"""
effect = """-f "Effect|A creature can use its action to eat one berry. Eating a berry restores 1 hit point, and the berry provides enough nourishment to sustain a creature for one day." """

cc_mod = ""

if command == "cc":
  title = "Creating Goodberry CC"
  description = help
  current_character.create_cc(cc, minVal=0, reset="none")
elif command == "cast":
  title = f"{combatant_name} tries to cast Goodberry"
  fields += """-f "Effect|Up to ten berries appear in your hand and are infused with magic for the duration. A creature can use its action to eat one berry. Eating a berry restores 1 hit point, and the berry provides enough nourishment to sustain a creature for one day." """
  level = int(args.last("l", default=1))
  slots = current_spellbook.get_slots(level)
  if slots > 0 and has_cc:
    title = f"{combatant_name} casts Goodberry"
    current_spellbook.use_slot(level)
    current_character.mod_cc(cc, 10)
    cc_mod = " (+10)"
  fields += f"""-f "Spell Slots|{current_spellbook.slots_str(level)}" """
elif command == "eat":
  title = f"{combatant_name} tries to eat {article} Goodberr{plural}"
  berries = current_character.get_cc(cc) if has_cc else 0
  if number > 0 and berries >= number:
    title = f"{combatant_name} eats {article} Goodberr{plural}"
    fields += f"""-f "Meta|**Healing**: {number}" """
    if current_combatant:
      current_combatant.modify_hp(number, overflow=False)
      target_info = target_info = f"{combatant_name} {current_combatant.hp_str()} (+{number})"
    else:
      current_character.modify_hp(number, overflow=False)
      target_info = target_info = f"{combatant_name} {current_character.hp_str()} (+{number})"
    current_character.mod_cc(cc, -number)
    cc_mod = f" (-{number})"
  fields += effect
elif command == "give":
  title = f"{combatant_name} tries to give {article} Goodberr{plural}"
  berries = current_character.get_cc(cc) if has_cc else 0
  if number > 0 and berries >= number:
    title = f"{combatant_name} gives {article} Goodberr{plural}"
    target_name = args.last("t", default="Meta")
    target = current_combat.get_combatant(target_name) if current_combat else None
    if target:
      target.modify_hp(number, overflow=False)
      target_info = target_info = f"{target.name if target else target_name} {target.hp_str()} (+{number})"
    fields += f"""-f "{target.name if target else target_name}|**Healing**: {number}" """
    current_character.mod_cc(cc, -number)
    cc_mod = f" (-{number})"
  fields += effect
else:
  title = "Goodberry Help"
  description = help
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-f "{cc}|{current_character.cc_str(cc)}{cc_mod}" """ if has_cc else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Goodberry | PHB 246" """}}
-color <color> -thumb <image>