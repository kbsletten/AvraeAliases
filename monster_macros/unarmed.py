embed
<drac2>
args = argparse(&ARGS&)

init = combat()

fields = ""

for target_name in args.get("t"):
  combatant = init.get_combatant(target_name) if init else None
  group = init.get_group(target_name) if init else None
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    to_hit = each.stats.get_mod("str")+each.stats.prof_bonus
    damage = max(0, 1+each.stats.get_mod("str"))
    each.add_effect("Unarmed", f"""-attack "{to_hit}|{damage}[bludgeoning]|You can punch, kick, head-butt, or use a similar forceful blow and deal bludgeoning damage equal to 1 + STR modifier." """)
    fields += f"""-f "{each.name}|Unarmed Strike. +{to_hit} to hit, {damage} bludgeoning damage" """
</drac2>
-title "Adding Unarmed Attacks!"
{{fields}}
-footer "!unarmed"
