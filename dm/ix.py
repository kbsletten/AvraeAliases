embed
<drac2>
args = argparse(&ARGS&)

init = combat()

adv = [init.get_combatant(t).name for t in args.get("adv") if init.get_combatant(t)]
dis = [init.get_combatant(t).name for t in args.get("dis") if init.get_combatant(t)]

group = {}
for g in args.get("group"):
  group_name, _, combatant_name = g.partition("|")
  group_name = init.get_group(group_name).name if init.get_group(group_name) else None
  if not group_name:
    continue
  combatant = init.get_combatant(combatant_name) if init.get_combatant(combatant_name) and init.get_combatant(combatant_name).group == group_name else None
  if not combatant:
    continue
  group[group_name] = combatant

place = {}
for p in args.get("p"):
  combatant_name, _, value = p.partition("|")
  combatant_name = init.get_combatant(combatant_name).name if init.get_combatant(combatant_name) else None
  if not combatant_name:
    continue
  place[combatant_name] = value

targets = [init.get_combatant(t) for t in args.get("t")]
if not targets:
  targets = init.groups + [comb for comb in init.combatants if not comb.group]

fields = ""

for target in targets:
  if not target:
    continue
  roller = target
  if target.type == "group":
    if target.name in group:
      roller = group[target.name]
    else:
      roller = target.combatants[0]
      for comb in target.combatants[1:]:
        if comb.initmod > roller.initmod:
          roller = comb
  modifier = 0 + (1 if roller.name in adv else 0) + (-1 if roller.name in dis else 0)
  init_roll = vroll(place[roller.name] if roller.name in place else roller.skills.initiative.d20(base_adv=[False, None, True][modifier + 1]))
  target.set_init(init_roll.total)
  fields += f"""-f "{roller.name}{f" (for {target.name})" if target.name != roller.name else ""}|{init_roll}|inline" """

init. end_round()
init.set_round(0)

</drac2>
-title "Rerolling Initiative"
{{fields}}
-footer "!ix | kbsletten#5710"
