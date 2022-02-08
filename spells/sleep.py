embed
<drac2>
args = argparse(&ARGS&)
level = int(args.last("l", 1))
init = combat()
current = init.me if init and init.me else init.current if init else None
title = f"{current.name} cannot cast Sleep!" if current else f"{name} is not in initiative!"
fields = ""

can_cast = current and current.spellbook and current.spellbook.can_cast("Sleep", level)

if can_cast:
  title = f"{current.name} casts Sleep!"
  current.spellbook.cast("Sleep", level)
  sleep_roll = vroll("5d8" if level == 1 else  f"5d8+{(level-1)*2}d8[higher level]")
  fields += f"""-f "Meta|**Damage**: {sleep_roll}" """

  used = 0
  targets = [init.get_combatant(target) for target in args.get("t") if init.get_combatant(target)]
  for _ in range(0, len(targets)):
    lowest_hp = None
    for target in [init.get_combatant(target.name) for target in targets]:
      if any(effect.name == "Asleep" for effect in target.effects):
        continue
      if lowest_hp == None or target.hp < lowest_hp.hp:
        lowest_hp = target
    if lowest_hp and lowest_hp.hp + used <= sleep_roll.total:
      used += lowest_hp.hp
      lowest_hp.add_effect("Asleep", "", duration=10, concentration=True, desc="Each creature affected by this spell falls unconscious until the spell ends, the sleeper takes damage, or someone uses an action to shake or slap the sleeper awake.")
      fields += f"""-f "{lowest_hp.name}|**Effect**: Asleep" """
    else:
      break

if current:
  remaining = current.spellbook.remaining_casts_of("Sleep", level)
  if can_cast and "At Will" not in remaining:
    remaining = f"{remaining} (-1)"
  fields += """-f "Effect|Roll 5d8; the total is how many hit points of creatures this spell can affect. Creatures within 20 feet of a point you choose within range are affected in ascending order of their current hit points (ignoring unconscious creatures).
Starting with the creature that has the lowest current hit points, each creature affected by this spell falls unconscious until the spell ends, the sleeper takes damage, or someone uses an action to shake or slap the sleeper awake. Subtract each creature's hit points from the total before moving on to the creature with the next lowest hit points. A creature's hit points must be equal to or less than the remaining total for that creature to be affected" """
  fields += f"""-f "Spell Slots|{remaining}" """
</drac2>
-title "{{title}}"
{{fields}}
-footer "!sleep | kbsletten#5710"
-color <color> -thumb <image>
