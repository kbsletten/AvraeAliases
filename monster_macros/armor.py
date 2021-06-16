embed
<drac2>
argv = &ARGS&
args = argparse(argv[1:])
armor = argv[0] if argv else None

armors = {
  'none': ('Unarmored', 10, 5),
  'leather': ('Leather', 11, 5),
  'padded': ('Padded', 11, 5),
  'studdedLeather': ('Studded leather', 12, 5),
  'hide': ('Hide', 12, 2),
  'chainShirt': ('Chain shirt', 13, 2),
  'scaleMail': ('Scale mail', 14, 2),
  'breastplate': ('Breastplate', 14, 2),
  'halfPlate': ('Half plate', 15, 2),
  'ringMail': ('Ring mail', 14, 0),
  'chainMail': ('Chain mail', 16, 0),
  'splint': ('Splint', 17, 5),
  'plate': ('Plate', 18, 5),
}

init = combat()

fields = ""

if armor in armors:
  name, base_ac, max_dex = armors[armor]
  shield_bonus = 0
  if "shield" in argv:
    name += ", shield"
    shield_bonus = 2
  for target_name in args.get("t"):
    combatant = init.get_combatant(target_name) if init else None
    group = init.get_group(target_name) if init else None
    combatants = group.combatants if group else [combatant] if combatant else []
    for each in combatants:
      dex_mod = min(each.stats.get_mod("dex"), max_dex) if max_dex else 0
      ac = base_ac+dex_mod+shield_bonus
      each.add_effect(name, f"-ac {ac}")
      fields += f"""-f "{each.name}|{name}. AC {ac}" """
else:
  fields += f"""-f "Unknown Armor|Options: {', '.join(armors.keys())}" """
</drac2>
-title "Equpping Armor!"
{{fields}}
-footer "!armor"
