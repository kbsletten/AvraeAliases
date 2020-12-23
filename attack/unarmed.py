embed
<drac2>
argv = &ARGS&
args = argparse(argv)

init = combat()
current = init.current if init else character()
if args.last("as"):
  current = init.get_combatant(args.last("as")) if init else current
name = current.name if current else name

title = args.last("title", "[name] attacks with an Unarmed Strike!").replace("[name]", name)
fields = ""
target_info = ""

prof = current.stats.prof_bonus if current else 2
str_mod = current.stats.get_mod("str") if current else 0

base = "3d20kh1" if args.adv() == 2 else "2d20kh1" if args.adv() == 1 else "2d20kl1" if args.adv() == -1 else "1d20"
to_hit = prof + str_mod
bonus = args.get("b")
damage_type = args.last("type", "bludgeoning")
attack = f"{max(0, 1 + str_mod)}[{damage_type}]"
damage = args.get("d")

attack_roll = vroll('+'.join([base, str(to_hit)] + bonus))
is_miss = attack_roll.result.crit == 2
is_crit = attack_roll.result.crit == 1
damage_roll = vroll('+'.join([attack] + damage), multiply=2 if is_crit else 1)
damage_message = "**Miss!**" if is_miss else f"**Damage{'(CRIT)' if is_crit else ''}**: {damage_roll}"

meta = f"""
-f "Meta|**To Hit:** {attack_roll}
{damage_message}"
"""

for target_expr in args.get("t"):
  target_name, _, target_argv = target_expr.partition("|")
  target = init.get_combatant(target_name) if init else None
  if target:
    target_args = argparse(target_argv)

    if target_args.adv() == 0:
      target_base = base
    else:
      target_base = "3d20kh1" if target_args.adv() == 2 else "2d20kh1" if target_args.adv() == 1 else "2d20kl1"
    target_bonus = bonus + target_args.get("b")
    target_damage = damage + target_args.get("d")

    target_attack_roll = vroll('+'.join([target_base, str(to_hit)] + target_bonus))
    target_is_miss = int(target_attack_roll.result.crit) == 2
    target_is_crit = int(target_attack_roll.result.crit) == 1
    target_hit = target_is_crit or (not target_is_miss and target_attack_roll.total >= target.ac)
    target_damage_message = "**Miss!**"
    if target_hit:
      target_damage_roll = '+'.join([attack] + damage)
      target_damage_message = target.damage(target_damage_roll, crit=target_is_crit)["damage"]
    fields += f"""-f "{target.name}|**To Hit:** {target_attack_roll}
{target_damage_message}"
"""
    target_info += f"{target.name} {target.hp_str()}\n"

</drac2>
-title "{{title}}"
{{fields if fields else meta}}
{{'\n'.join(f"""-f "{field}" """ for field in args.get("f"))}}
-f "Effect|***Melee Weapon Attack:*** +{{to_hit}} to hit, reach 5 ft., one target. *Hit:* {{max(0, 1 + str_mod)}} {{damage_type}} damage."
-footer "{{target_info if target_info else "Unarmed Strike | PHB 195"}}"