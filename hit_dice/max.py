embed
<drac2>
current_character = character()
current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
if not current_combatant:
  current_combatant = current_character
combatant_name = current_combatant.name if current_combatant else name

fields = ""

for die in [6, 8, 10, 12]:
  cc = f"Hit Dice (d{die})"
  if not current_character.cc_exists(cc):
    continue
  increase = current_character.get_cc_max(cc) - current_character.get_cc(cc)
  current_character.set_cc(cc, current_character.get_cc_max(cc))
  fields += f"""-f "{cc}|{current_character.cc_str(cc)} (+{increase})|inline" """
</drac2>
-title "{{combatant_name}} recovers all Hit Dice"
{{fields}}
-footer "!hd max | kbsletten#5710"
-color <color> -thumb <image>