embed
<drac2>
current_combat = combat()
command = "&1&"
monk_level = int(get("MonkLevel", 0))
proficiency_bonus = int(get("proficiencyBonus", 2))
current_combatant = current_combat.get_combatant(name) if current_combat else None
cc1 = "Wings Unfurled"
cc2 = "Ki Points"
cc1_ex = cc_exists(cc1)
cc1_value = (cc1_ex and get_cc(cc1)>0)
cc2_ex = cc_exists(cc2)
cc2_value = (cc2_ex and get_cc(cc2)>0)
cc = cc1 if cc1_value else cc2
cc_ex = cc1_ex or cc2_ex
cc_value = cc1_value or cc2_value
combatant_name = current_combatant.name if current_combatant else name
title = "Invalid alias"
description = "You do not have this ability."
fields = ""

if command == "cc" or command == "help":
  title = "Wings Unfurled"
  description = """When you use your Step of the Wind, you can unfurl spectral draconic wings from your backthat vanish at the end of your turn. While the wings exist, you have a flying speed equal to your walking speed.
You can use this feature a number of times equal to your proficiency bonus, and you regain all expended uses when you finish a long rest. While you have no uses available, you can spend1 additional ki point when you activate Step of the Wind to use this feature again."""
  if command == "cc":
    create_cc(cc1, minVal=0, maxVal=proficiency_bonus, reset='long', dispType='bubble')
elif cc_value:
  title = f"{combatant_name} uses Wings Unfurled"
  description = ""
  mod_cc(cc,-1)
  fields = """-f "Effect|When you use your Step of the Wind, you have a flying speed equal to your walking speed until the end of your turn." """
elif cc_ex:
  title = f"{combatant_name} tries to use Wings Unfurled"
  description = "You must finish a long rest or recover Ki before you can use this ability again."
elif monk_level >= 6:
  description = f"""Missing a **c**ustom **c**ounter named `{cc1}`. See `!help cc create` for how to make one manually, or run `!cc create "{cc1}" -reset long -min 0 -max {proficiency_bonus} -type bubble`."""

</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-f "{cc}|{cc_str(cc)}" """ if cc_value else ""}}
-footer "UNEARTHED ARCANA 2020 Subclasses, Part 5"
-color <color> -thumb <image>
