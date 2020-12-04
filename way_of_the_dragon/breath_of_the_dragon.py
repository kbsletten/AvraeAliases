embed
<drac2>
args = argparse(&ARGS&)
command = "&1&"

current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

monk_level = int(get("MonkLevel", 0))
proficiency_bonus = int(get("proficiencyBonus", 2))
wisdom_modifier = int(get("wisdomMod", 0))
dc = int(args.last("dc", 8 + proficiency_bonus + wisdom_modifier))
die_count = 2 + (1 if monk_level > 10 else 0)
monk_die = 4 + (2 if monk_level > 4 else 0) + (2 if monk_level > 10 else 0) + (2 if monk_level > 16 else 0)

cc1 = "Breath of the Dragon"
cc2 = "Ki Points"
cc1_ex = cc_exists(cc1)
cc1_value = (cc1_ex and get_cc(cc1)>0)
cc2_ex = cc_exists(cc2)
cc2_value = (cc2_ex and get_cc(cc2)>0)
cc = cc1 if cc1_value else cc2
cc_ex = cc1_ex or cc2_ex
cc_value = cc1_value or cc2_value

title = "Invalid alias"
description = "You do not have this ability."
fields = ""
target_info = ""

damage_roll = vroll(args.last("d", f"{die_count}d{monk_die}[magical {command}]"))

if command == "cc" or command == "help":
  title = "Breath of the Dragon"
  description = """You can channel your ki into destructive waves of energy like the dragons you emulate. When you take the Attack action on your turn, you can replace one of the attacks with an exhalation of draconic energy in either a 20-foot cone or a 30-foot line that is 5 feet wide (your choice). Choose a damage type: acid, cold, fire, lightning, or poison. Each creature in the area must make a Dexterity saving throw against your ki save DC, taking damage of the chosen type equal to two rolls of your Martial Arts die on a failure, or half as much damage on a success.
At 11th level, the damage of your breath increases to three rolls of your Martial Arts die.
You can use this feature a number of times equal to your proficiency bonus, and you regain all expended uses when you finish a long rest. While you have no uses available, you can spend 1 ki point to use this feature again."""
  if command == "cc":
    create_cc(cc1, minVal=0, maxVal=proficiency_bonus, reset='long', dispType='bubble')
  else:
    fields = """-f "Usage|!botd {acid, cold, fire, lightning, poison} [-t TARGET] """
elif cc_value:
  if command in ["acid", "cold", "fire", "lightning", "poison"]:
    title = f"{combatant_name} uses Breath of the Dragon"
    description = ""
    fields = f"""-f "Meta|**Damage**: {damage_roll}
**DC**: {dc}"
"""
    mod_cc(cc,-1)
    if current_combat:
      for target_name in args.get("t", default=[]):
        target = current_combat.get_combatant(target_name) if current_combat else None
        if target:
          target_save = target.save('dex')
          target_passed = target_save.total>=dc
          damage = damage_roll.consolidated()
          if target_passed:
            damage = f"{damage}/2"
          target_damage = target.damage(damage)["damage"]
          fields += f"""
  -f "{target.name}|**WIS Save**: {target_save}; {"Success!" if target_passed else "Failure!"}
{target_damage}"
"""
          target_info += f"{target.name} {target.hp_str()}\n"
    two_or_three = "two" if die_count == 2 else "three"
    fields+= f"""
-f "Effect|When you take the Attack action on your turn, you can replace one of the attacks with an exhalation of draconic energy in either a 20-foot cone or a 30-foot line that is 5 feet wide (your choice). Choose a damage type: acid, cold, fire, lightning, or poison. Each creature in the area must make a Dexterity saving throw against your ki save DC, taking damage of the chosen type equal to {two_or_three} rolls of your Martial Arts die on a failure, or half as much damage on a success."
"""
  else:
    title = "Invalid type"
    description = "You must specify type acid, cold, fire, lightning, or poison"
elif cc_ex:
  title = f"{combatant_name} tries to use Breath of the Dragon"
  description = "You must finish a long rest or recover Ki before you can use this ability again."
elif monk_level >= 3:
  description = f"""Missing a **c**ustom **c**ounter named `{cc1}`. See `!help cc create` for how to make one manually, or run `!cc create "{cc1}" -reset long -min 0 -max {proficiency_bonus} -type bubble`."""

</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-f "{cc}|{cc_str(cc)}" """ if cc_value and damage_roll else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "UNEARTHED ARCANA 2020 Subclasses, Part 5" """}}
-color <color> -thumb <image>
