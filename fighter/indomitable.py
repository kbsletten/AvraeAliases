embed
<drac2>
command = "&1&"

current_character=character()
current_combat=combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

fighter_level=int(get("FighterLevel", 0))

cc="Indomitable"
cc_ex=cc_exists(cc)
cc_value=(cc_ex and get_cc(cc)>0)

title = "Invalid alias"
description = "You do not have this ability."
fields = ""

if command == "help":
  title = "Indomitable"
  description = """Beginning at 9th level, you can reroll a saving throw that you fail. If you do so, you must use the new roll, and you can’t use this feature again until you finish a long rest.
You can use this feature twice between long rests starting at 13th level and three times between long rests starting at 17th level."""
elif cc_value:
  if command in ["str", "dex", "con", "int", "wis", "cha"]:
    title = f"{combatant_name} Rerolls a Save"
    description = ""
    fields = """-f "Effect|On your turn, you can take one additional action." """
    mod_cc(cc,-1)
  else:
    title = "Invalid save"
    description = "You must specify str, dex, con, int, wis, or cha"
elif cc_ex:
  title = f"{combatant_name} tries to Reroll a Save"
  description = "You must finish a short rest before you can use this ability again."
elif fighter_level >= 9:
  description = f"Missing a **c**ustom **c**ounter named `{cc}`. See `!help cc create` for how to make one manually, or run the `!level` alias as a Fighter and it will make one for you."
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f""" -f "{cc} {cc_str(cc)}" """ if cc_value else ""}}
-footer "Fighter | PHB 72"
-color <color>
