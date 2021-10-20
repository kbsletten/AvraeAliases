embed
<drac2>
current_character = character()
current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
if not current_combatant:
  current_combatant = current_character
combatant_name = current_combatant.name if current_combatant else name

fields = ""

count = max(1, int(current_character.levels.total_level / 2))
for die in [12, 10, 8, 6]:
  cc = f"Hit Dice (d{die})"
  if not current_character.cc_exists(cc):
    continue
  cc_val = current_character.get_cc(cc)
  cc_max = current_character.get_cc_max(cc)
  if cc_val < cc_max:
    mod = min(count, cc_max - cc_val)
    current_character.mod_cc(cc, mod)
    count -= mod
    fields += f"""-f "{cc}|{current_character.cc_str(cc)} (+{mod})" """
  else:
    fields += f"""-f "{cc}|{current_character.cc_str(cc)}" """
</drac2>
-title "{{combatant_name}} recovers Hit Dice"
-description "At the end of a long rest, the character also regains spent Hit Dice, up to a number of dice equal to half of the character's total number of them (minimum of one die)."
{{fields}}
-footer "!hd lr | kbsletten#5710"
-color <color> -thumb <image>
