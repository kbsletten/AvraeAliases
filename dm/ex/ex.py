embed
<drac2>
args = argparse(&ARGS&)

duration = args.last("dur", "10m")
rounds = 0
hours, _, duration = duration.partition("h") if "h" in duration else ["", "", duration]
minutes, _, duration = duration.partition("m") if "m" in duration else ["", "", duration]
if hours:
  rounds += 600 * int(hours)
if minutes:
  rounds += 10 * int(minutes)
rounds += int(duration) if duration else 0

init = combat()
targets = [(init.get_group(target), init.get_combatant(target)) for target in args.get("t")] if init else []
if not args.get("t"):
  targets = [(None, each) for each in init.combatants] if init else []

fields = ""

for group, combatant in targets:
  combatants = group.combatants if group else [combatant] if combatant else []
  for each in combatants:
    if each.effects:
      fields += f"""-f "{each.name}|"""
      for effect in each.effects:
        should_remove = effect.name != "map" and effect.duration and effect.duration <= rounds
        fields += f"{effect.name}{'' if should_remove else ' (not removed)'}\n"
        if should_remove:
          each.remove_effect(effect.name)
      fields += """" """
</drac2>
-title "Removing Effects"
{{fields}}
-footer "!ex | kbsletten#5710"
-color <color>
