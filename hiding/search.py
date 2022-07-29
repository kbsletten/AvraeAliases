embed
<drac2>
argv = &ARGS&
args = argparse(argv)

char = character()
init = combat()

target = init.get_combatant(args.last("t")) if init and args.last("t") else init.me if init and init.me else init.current if init and init.current else None
name = target.name if target else char.name if char else name

modifier = None
if "adv" in argv:
  modifier = 1
if "dis" in argv:
  modifier = -1 if modifier is None else 0

fields = ""

if not target or target.type == "combatant":
  passive_perception = 10 + ((target or char).skills.perception.value if target or char else 0) + (modifier or 0) * 5
  fields += f"""-f "Passive Wisdom (Perception)|{passive_perception}" """
  for combatant in init.combatants if init else []:
    hidden_effect = combatant.get_effect("Hidden")
    if not hidden_effect or "(" not in hidden_effect.name or ")" not in hidden_effect.name:
      continue
    stealth_check = int(hidden_effect.name[hidden_effect.name.index("(")+1:hidden_effect.name.index(")")])
    if stealth_check >= passive_perception:
      fields += f"""-f "{combatant.name}|Hidden! ({stealth_check})|inline" """
    else:
      fields += f"""-f "{combatant.name}|Noticed! ({stealth_check})|inline" """
else:
  for each in target.combatants:
    passive_perception = 10 + each.skills.perception.value + (modifier or 0) * 5
    fields += f"""-f "{each.name}|Passive Wisdom (Perception): {passive_perception}" """
    for combatant in init.combatants if init else []:
      hidden_effect = combatant.get_effect("Hidden")
      if not hidden_effect or "(" not in hidden_effect.name or ")" not in hidden_effect.name:
        continue
      stealth_check = int(hidden_effect.name[hidden_effect.name.index("(")+1:hidden_effect.name.index(")")])
      if stealth_check >= passive_perception:
        fields += f"""-f "{combatant.name}|Hidden! ({stealth_check})|inline" """
      else:
        fields += f"""-f "{combatant.name}|Noticed! ({stealth_check})|inline" """
</drac2>
-title "{{name}} is Searching!"
{{fields}}
-footer "!notice | kbsletten#5710"
-color <color> {{"-thumb <image>" if not target or init.me and init.me.id == target.id else ""}}
