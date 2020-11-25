embed
<drac2>
command = "&1&"

current_combat=combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

fighter_level=int(get("FighterLevel", 0))

cc="Action Surge"
cc_ex=cc_exists(cc)
cc_value=(cc_ex and get_cc(cc)>0)

title = "Invalid alias"
description = "You do not have this ability."
fields = ""

if command == "help":
  title = "Action Surge"
  description = """Starting at 2nd level, you can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action.
Once you use this feature, you must finish a short or long rest before you can use it again. Starting at 17th level, you can use it twice before a rest, but only once on the same turn."""
elif cc_value:
  title = f"{combatant_name} Action Surges"
  description = ""
  fields = """-f "Effect|On your turn, you can take one additional action." """
  mod_cc(cc,-1)
elif cc_ex:
  title = f"{combatant_name} tries to Action Surge"
  description = "You must finish a short rest before you can use this ability again."
elif fighter_level >= 2:
  description = f"Missing a **c**ustom **c**ounter named `{cc}`. See `!help cc create` for how to make one manually, or run the `!level` alias as a Fighter and it will make one for you."
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f""" -f "{cc}|{cc_str(cc)}" """ if cc_value else ""}}
-footer "Fighter | PHB 72"
-color <color>
