embed
<drac2>
argv = &ARGS&
args = argparse(argv)

char = character()
name = char.name if char else name
proficiency_bonus = char.stats.prof_bonus if char else 2
init = combat()
me = init.me if init else None
name = me.name if me else name
proficiency_bonus = me.stats.prof_bonus if me else proficiency_bonus
max_damage = int(args.last("d", 0))
target_expr = args.last("t")
target = init.get_combatant(target_expr) if init and target_expr else None

title = "[name] uses Interception".replace("[name]", name)
fields = ""
target_info = ""

damage_roll = vroll(f"1d10+{proficiency_bonus}")
cap = f" (capped at {max_damage})" if max_damage and damage_roll.total > max_damage else ""

fields += f"""-f "Damage Reduction|{damage_roll}{cap}" """

if target and max_damage:
  healing = min(max_damage, damage_roll.total)
  target.mod_hp(healing)
  target_info += f"{target.name} {target.hp_str()} (+{healing})"

</drac2>
-title "{{title}}"
{{fields}}
-f "Effect|When a creature you can see hits a target, other than you, within 5 feet of you with an attack, you can use your reaction to reduce the damage the target takes by 1d10 + your proficiency bonus (to a minimum of 0 damage). You must be wielding a shield or a simple or martial weapon to use this reaction."
-footer "{{target_info if target_info else "Fighting Style: Interception | TCoE"}}"