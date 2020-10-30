embed
<drac2>
args = &ARGS&
command = args[0]
count = int(command) if command.isdigit() else 0

current_character = character()
current_combat=combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
if not current_combatant:
  current_combatant = current_character
combatant_name = current_combatant.name if current_combatant else name

con_mod = int(get("constitutionMod", 0))
barbarian_level = int(get("BarbarianLevel", 0))
bard_level = int(get("BardLevel", 0))
cleric_level = int(get("ClericLevel", 0))
druid_level = int(get("DruidLevel", 0))
fighter_level = int(get("FighterLevel", 0))
monk_level = int(get("MonkLevel", 0))
paladin_level = int(get("PaladinLevel", 0))
ranger_level = int(get("RangerLevel", 0))
rogue_level = int(get("RogueLevel", 0))
sorcerer_level = int(get("SorcererLevel", 0))
warlock_level = int(get("WarlockLevel", 0))
wizard_level = int(get("WizardLevel", 0))

hd12 = barbarian_level
hd10 = fighter_level + paladin_level + ranger_level
hd8 = bard_level + cleric_level + druid_level + monk_level + rogue_level + warlock_level
hd6 = sorcerer_level + wizard_level

cc_hd12 = "Hit Dice (d12)"
cc_hd10 = "Hit Dice (d10)"
cc_hd8 = "Hit Dice (d8)"
cc_hd6 = "Hit Dice (d6)"

cc_hd12_ex = current_character.cc_exists(cc_hd12)
cc_hd10_ex = current_character.cc_exists(cc_hd10)
cc_hd8_ex = current_character.cc_exists(cc_hd8)
cc_hd6_ex = current_character.cc_exists(cc_hd6)

cc_hd12_max = current_character.get_cc_max(cc_hd12) if cc_hd12_ex else 0
cc_hd10_max = current_character.get_cc_max(cc_hd10) if cc_hd10_ex else 0
cc_hd8_max = current_character.get_cc_max(cc_hd8) if cc_hd8_ex else 0
cc_hd6_max = current_character.get_cc_max(cc_hd6) if cc_hd6_ex else 0

cc_hd12_val = current_character.get_cc(cc_hd12) if cc_hd12_ex else 0
cc_hd10_val = current_character.get_cc(cc_hd10) if cc_hd10_ex else 0
cc_hd8_val = current_character.get_cc(cc_hd8) if cc_hd8_ex else 0
cc_hd6_val = current_character.get_cc(cc_hd6) if cc_hd6_ex else 0

cc_hd_max = cc_hd12_max + cc_hd10_max + cc_hd8_max + cc_hd6_max
cc_hd_total = cc_hd12_val + cc_hd10_val + cc_hd8_val + cc_hd6_val

title = "Hit Dice"
description = f"Invalid command `{command}`."
fields = ""
target_info = ""

if command != "cc":
  if hd12 != cc_hd12_max:
    fields += f"""-f "{cc_hd12}|You do not have the correct number of d12 hit dice (expected {hd12}, got {cc_hd12_max}).
Run `!hd cc` to fix this." """
  if hd10 != cc_hd10_max:
    fields += f"""-f "{cc_hd10}|You do not have the correct number of d10 hit dice (expected {hd10}, got {cc_hd10_max}).
Run `!hd cc` to fix this." """
  if hd8 != cc_hd8_max:
    fields += f"""-f "{cc_hd8}|You do not have the correct number of d8 hit dice (expected {hd8}, got {cc_hd8_max}).
Run `!hd cc` to fix this." """
  if hd6 != cc_hd6_max:
    fields += f"""-f "{cc_hd6}|You do not have the correct number of d6 hit dice (expected {hd6}, got {cc_hd6_max}).
Run `!hd cc` to fix this." """

if command == "help":
  description = """
`help` - you know what this is, this is this
`cc` - set up the CCs appropriate for your class and level
`max` - max out your hit dice, recovering all of them
`lr` - recover the number specified in the rules on long rest (half of your total, minimum of one)
# - use a number of hit dice and apply the healing
"""
elif command == "cc":
  description = "Setting up CCs to match your character's class and level."
  if hd12 > 0:
    current_character.create_cc(cc_hd12, minVal=0, maxVal=hd12, reset='none')
    fields += f"""-f "{cc_hd12}|{current_character.cc_str(cc_hd12)}" """
  if hd10 > 0:
    current_character.create_cc(cc_hd10, minVal=0, maxVal=hd10, reset='none')
    fields += f"""-f "{cc_hd10}|{current_character.cc_str(cc_hd10)}" """
  if hd8 > 0:
    current_character.create_cc(cc_hd8, minVal=0, maxVal=hd8, reset='none')
    fields += f"""-f "{cc_hd8}|{current_character.cc_str(cc_hd8)}" """
  if hd6 > 0:
    current_character.create_cc(cc_hd6, minVal=0, maxVal=hd6, reset='none')
    fields += f"""-f "{cc_hd6}|{current_character.cc_str(cc_hd6)}" """
elif command == "max":
  title = f"{combatant_name} recovers all Hit Dice"
  description = ""
  if cc_hd12_ex:
    current_character.set_cc(cc_hd12, cc_hd12_max)
    fields += f"""-f "{cc_hd12}|{current_character.cc_str(cc_hd12)}" """
  if cc_hd10_ex:
    current_character.set_cc(cc_hd10, cc_hd10_max)
    fields += f"""-f "{cc_hd10}|{current_character.cc_str(cc_hd10)}" """
  if cc_hd8_ex:
    current_character.set_cc(cc_hd8, cc_hd8_max)
    fields += f"""-f "{cc_hd8}|{current_character.cc_str(cc_hd8)}" """
  if cc_hd6_ex:
    current_character.set_cc(cc_hd6, cc_hd6_max)
    fields += f"""-f "{cc_hd6}|{current_character.cc_str(cc_hd6)}" """
elif command == "lr":
  title = f"{combatant_name} recovers Hit Dice"
  description = "At the end of a long rest, the character also regains spent Hit Dice, up to a number of dice equal to half of the character's total number of them (minimum of one die)."
  count = max(1, int(cc_hd_max / 2))
  if cc_hd12_val < cc_hd12_max:
    mod = min(count, cc_hd12_max - cc_hd12_val)
    current_character.mod_cc(cc_hd12, mod)
    count -= mod
    fields += f"""-f "{cc_hd12}|{current_character.cc_str(cc_hd12)} (+{mod})" """
  if count > 0 and cc_hd10_val < cc_hd10_max:
    mod = min(count, cc_hd10_max - cc_hd10_val)
    current_character.mod_cc(cc_hd10, mod)
    count -= mod
    fields += f"""-f "{cc_hd10}|{current_character.cc_str(cc_hd10)} (+{mod})" """
  if count > 0 and cc_hd8_val < cc_hd8_max:
    mod = min(count, cc_hd8_max - cc_hd8_val)
    current_character.mod_cc(cc_hd8, mod)
    count -= mod
    fields += f"""-f "{cc_hd8}|{current_character.cc_str(cc_hd8)} (+{mod})" """
  if count > 0 and cc_hd6_val < cc_hd6_max:
    mod = min(count, cc_hd6_max - cc_hd6_val)
    current_character.mod_cc(cc_hd6, mod)
    count -= mod
    fields += f"""-f "{cc_hd6}|{current_character.cc_str(cc_hd6)} (+{mod})" """
elif count > cc_hd_total:
  title = f"{combatant_name} tries to use Hit Dice"
  description = f"You do not have enough hit dice to take this action (using {count}, remaining {cc_hd_total})"
elif count > 0:
  title = f"{combatant_name} uses Hit Dice"
  description = ""
  healing_total = 0
  if cc_hd12_val > 0:
    dice = min(count, cc_hd12_val)
    healing_roll = vroll(f"{dice}d12+{con_mod*dice}")
    fields+= f"""-f "Healing (d12)|{healing_roll}" """
    count -= dice
    healing_total += healing_roll.total
    current_character.mod_cc(cc_hd12, -dice)
  if count > 0 and cc_hd10_val > 0:
    dice = min(count, cc_hd10_val)
    healing_roll = vroll(f"{dice}d10+{con_mod*dice}")
    fields+= f"""-f "Healing (d10)|{healing_roll}" """
    count -= dice
    healing_total += healing_roll.total
    current_character.mod_cc(cc_hd10, -dice)
  if count > 0 and cc_hd8_val > 0:
    dice = min(count, cc_hd8_val)
    healing_roll = vroll(f"{dice}d8+{con_mod*dice}")
    fields+= f"""-f "Healing (d8)|{healing_roll}" """
    count -= dice
    healing_total += healing_roll.total
    current_character.mod_cc(cc_hd8, -dice)
  if count > 0 and cc_hd6_val > 0:
    dice = min(count, cc_hd6_val)
    healing_roll = vroll(f"{dice}d6+{con_mod*dice}")
    fields+= f"""-f "Healing (d6)|{healing_roll}" """
    count -= dice
    healing_total += healing_roll.total
    current_character.mod_cc(cc_hd6, -dice)
  current_combatant.modify_hp(healing_total, overflow=False)
  target_info = f"{combatant_name}: {current_combatant.hp_str()} (+{healing_total})"
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Resting | PHB 186" """}}