embed
<drac2>
current_character = character()
current_combat = combat()
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

fields = ""

for die, val in hd.items():
  if not val:
    continue
  cc = f"Hit Dice (d{die})"
  current_character.create_cc(cc, minVal=0, maxVal=val, reset='none')
  fields += f"""-f "{cc}|{current_character.cc_str(cc)}|inline" """
</drac2>
-title "Creating Hit Dice for {{combatant_name}}"
{{fields}}
-footer "!hd cc | kbsletten#5710"
-color <color> -thumb <image>
