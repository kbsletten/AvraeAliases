embed
<drac2>
argv = %*%

first_open = argv.index("{")
last_close = argv.rindex("}")

args = argparse(argv[last_close+1:]) if last_close != -1 else argparse(argv)
json = load_json(argv[first_open:last_close+1]) if argv else {}

title = "Custom Attack!"
target_info = ""

init = combat()
current = init.current if init else None

modifier = None
hit_bonus = args.get("b")
damage_bonus = args.get("d")

if current:
  title = f"{current.name} makes a Custom Attack!"
  for effects in current.effects:
    if "adv" in effects.effect:
      modifier = 1
    if "b" in effects.effect:
      hit_bonus = hit_bonus + [effects.effect["b"]]
    if "d" in effects.effect:
      damage_bonus = damage_bonus + [effects.effect["d"]]

if "dis" in argv:
  modifier = 0 if modifier == 1 or "adv" in argv else -1
elif "adv" in argv:
  modifier = 2 if "ea" in argv else 1

fields = ""

for target_expr in args.get("t"):
  target_name, _, target_argv = target_expr.partition("|")
  target_group = init.get_group(target_name)
  target_combatants = target_group.combatants if target_group else [init.get_combatant(target_name)]
  for target in target_combatants:
    if "attack" in json:
      attack_roll = vroll("+".join([
        "3d20kh1" if modifier == 2 else
        "2d20kh1" if modifier == 1 else
        "2d20kl1" if modifier == -1 else
        "1d20",
        json["attack"]["bonus"]
      ] + hit_bonus))
      crit = attack_roll.result.crit == 1
      hit = crit or attack_roll.result.crit != 2 and attack_roll.total >= target.ac
      if hit:
        if crit and "crit" in json["attack"]:
          damage_roll = vroll("+".join([json["attack"]["crit"]["damage"]] + damage_bonus)) if "damage" in json["attack"]["crit"] else None
        else:
          damage_roll = vroll("+".join([json["attack"]["hit"]["damage"]] + damage_bonus), multiply=(2 if crit else 1)) if "damage" in json["attack"]["hit"] else None
      else:
        damage_roll = vroll("+".join([json["attack"]["miss"]["damage"]] + damage_bonus)) if "damage" in json["attack"]["miss"] else None
      fields += f"""-f "{target.name}|**To Hit:** {attack_roll}
{f'**Damage:** {target.damage(damage_roll)}' if damage_roll else 'Miss'}" """

</drac2>
-title "{{title}}"
{{fields}}
-footer "{{target_info or "!mm attack | kbsletten#5710"}}"
