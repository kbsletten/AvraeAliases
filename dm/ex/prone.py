embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()

effect_name = args.last("name", "Prone")
effect_duration = args.last("duration", None)
if effect_duration:
  effect_duration = int(effect_duration)
effect_parent = args.last("parent", None)
if effect_parent:
  comb, _, eff = effect_parent.partition("|")
  comb = init.get_combatant(comb)
  effect_parent = comb.get_effect(eff) if comb else None
effect_concentration = "conc" in argv
effect_end = "end" in argv
effect_desc = args.last("desc", """A prone creature's only movement option is to crawl, unless it stands up and thereby ends the condition.
 - The creature has disadvantage on attack rolls.
 - An attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the attack roll has disadvantage.""")

targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    eff = each.add_effect(
      effect_name,
      passive_effects={
        "attack_advantage": -1
      },
      buttons=[{
        "label": "Stand Up",
        "verb": "stands up",
        "style": 1,
        "automation": [{
          "type": "remove_ieffect"
        }]
      }],
      duration=effect_duration,
      concentration=effect_concentration,
      parent=effect_parent,
      end=effect_end,
      desc=effect_desc,
    )
    fields += f"""-f "{each.name}|{eff.name}|inline" """
</drac2>
-title "Knocking combatants prone!"
{{fields}}
-footer "!ex prone | kbsletten#5710"
