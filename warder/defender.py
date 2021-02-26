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

title = "[name] uses Sworn Defender".replace("[name]", name)
fields = ""
target_info = ""

damage_roll = vroll(f"1d10+{proficiency_bonus}")
cap = f" (capped at {max_damage})" if max_damage and damage_roll.total > max_damage else ""

fields += f"""-f "Damage Reduction|{damage_roll}{cap}" """

if me and max_damage:
  healing = min(max_damage, damage_roll.total)
  me.mod_hp(healing, overflow=False)
  target_info += f"{me.name} {me.hp_str()} (+{healing})"
elif char and max_damage:
  healing = min(max_damage, damage_roll.total)
  char.modify_hp(healing, overflow=False)
  target_info += f"{char.name} {char.hp_str()} (+{healing})"

</drac2>
-title "{{title}}"
{{fields}}
-f "Effect|While you are within 30 feet of your warded creature, when a creature you can see hits you with an attack, you can use your reaction to reduce the damage you take by 1d10 + your proficiency bonus (to a minimum of 0 damage). You must be wielding a shield or a simple or martial weapon to use this reaction."
-footer "{{target_info if target_info else "Sworn Defender | Warder"}}"