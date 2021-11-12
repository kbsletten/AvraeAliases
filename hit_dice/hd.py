embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if argv else ""
command_count, _, command_die = command.partition("d")
count = int(command_count) if command_count.isdigit() else 0

current_character = character()
current_combat=combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
if not current_combatant:
  current_combatant = current_character
combatant_name = current_combatant.name if current_combatant else name

HIT_DICE = {
  "Artificer": 8,
  "Barbarian": 12,
  "Bard": 8,
  "Cleric": 8,
  "Druid": 8,
  "Fighter": 10,
  "Monk": 8,
  "Paladin": 10,
  "Ranger": 10,
  "Rogue": 8,
  "Sorcerer": 6,
  "Warlock": 8,
  "Wizard": 6,
}

con_mod = current_character.stats.get_mod("con")

hd = {
  12: 0,
  10: 0,
  8: 0,
  6: 0,
}

for name, level in current_character.levels:
  die = HIT_DICE[name] if name in HIT_DICE else None
  if not die:
    continue
  hd[die] += level

title = "Hit Dice"
description = f"Invalid command `{command}`."
fields = ""
target_info = ""

for die in [12, 10, 8, 6]:
  cc = f"Hit Dice (d{die})"
  cc_max = current_character.get_cc_max(cc) if current_character.cc_exists(cc) else 0
  if hd[die] > cc_max:
    fields += f"""-f "{cc}|You do not have the correct number of d{die} hit dice (expected {hd[die]}, got {cc_max}).
Run `!hd cc` to fix this." """

if count > current_character.levels.total_level:
  title = f"{combatant_name} tries to use Hit Dice"
  description = f"You do not have enough hit dice to take this action (using {count}, remaining {current_character.levels.total_level})"
elif count > 0:
  title = f"{combatant_name} uses Hit Dice"
  description = ""
  healing = []
  used = ""
  con_healing = f"{con_mod*count}"
  for die in [12, 10, 8, 6]:
    if command_die and str(die) != command_die:
      continue
    cc = f"Hit Dice (d{die})"
    if not current_character.cc_exists(cc) or current_character.get_cc(cc) < 1:
      continue
    cc_val = current_character.get_cc(cc)
    cc_max = current_character.get_cc_max(cc)
    dice = min(count, cc_val)
    healing.append(f"{dice}d{die}{f'mi{-con_mod}' if con_mod < 0 else ''}")
    count -= dice
    current_character.mod_cc(cc, -dice)
    used += f"""-f "{cc}|{current_character.cc_str(cc)} (-{dice})" """
  if healing:
    healing.append(con_healing)
    healing.extend(args.get('b'))
    healing_roll = vroll('+'.join(healing))
    fields += f"""-f "Healing|{healing_roll}" """
    current_combatant.modify_hp(healing_roll.total, overflow=False)
    target_info = f"{combatant_name}: {current_combatant.hp_str()} (+{healing_roll.total})"
    fields += used
else:
  title = f"{combatant_name}'s current Hit Dice"
  description = ""
  for die in [12, 10, 8, 6]:
    cc = f"Hit Dice (d{die})"
    if not current_character.cc_exists(cc):
      continue
    fields += f"""-f "{cc}|{current_character.cc_str(cc)}|inline" """
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "!hd | kbsletten#5710" """}}
-color <color> -thumb <image>