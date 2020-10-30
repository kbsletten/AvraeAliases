embed
<drac2>
command = "&1&"

current_character=character()
current_combat=combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

fighter_level=int(get("FighterLevel", 0))

cc="Second Wind"
cc_ex=cc_exists(cc)
cc_value=(cc_ex and get_cc(cc)>0)

title = "Invalid alias"
description = "You do not have this ability."
fields = ""
target_info = ""

healing_roll = vroll(f"1d10+{fighter_level}")

if command == "help":
  title = "Second Wind"
  description = """You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again."""
elif cc_value:
  title = f"{combatant_name} gets their Second Wind"
  description = ""
  fields = f"""-f "Meta|**Healing**: {healing_roll}" """
  mod_cc(cc,-1)
  if current_combatant:
    current_combatant.modify_hp(healing_roll.total, overflow=False)
    target_info = f"{combatant_name} {current_combatant.hp_str()}"
  else:
    current_character.modify_hp(healing_roll.total, overflow=False)
    target_info = f"{combatant_name}: {current_character.hp_str()} (+{healing_roll.total})"
elif cc_ex:
  title = f"{combatant_name} tries to get their Second Wind"
  description = "You must finish a short rest before you can use this ability again."
elif fighter_level >= 2:
  description = f"Missing a **c**ustom **c**ounter named `{cc}`. See `!help cc create` for how to make one manually, or run the `!level` alias as a Fighter and it will make one for you."
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f""" -f "{cc} {cc_str(cc)}" """ if cc_value else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Fighter | PHB 72" """}}
-color <color>
