embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()
current = init.current if init else None
if current and current.type == "group":
  current = current.combatants[0]
if args.last("as"):
  current = init.get_combatant(args.last("as")) if init else current
if not current:
  current = character()
name = current.name if current else name

shove_adv = "adv" in argv
shove_dis = "dis" in argv
shove_mod = True if shove_adv and not shove_dis else False if shove_dis and not shove_adv else None
shove_base = "2d20kh1" if shove_mod == True else "2d20kl1" if shove_mod == False else "1d20"
shove_expr = current.skills.athletics.d20(base_adv=shove_mod) if current else shove_base
shove_bonus = ''.join([f"+{bonus}" for bonus in args.get("b")])
shove_roll = vroll(f"{shove_expr}{shove_bonus}")

effect_expr = args.last("effect", "")
effect_name, _, effect_args = effect_expr.partition('|')
fields = ""

for target_expr in args.get("t"):
  target_name, _, target_arg = target_expr.partition('|')
  target_argv = target_arg.split(' ')
  target_args = argparse(target_arg)
  target = init.get_combatant(target_name) if init else None
  escape_adv = "adv" in target_argv
  escape_dis = "dis" in target_argv
  escape_pass = "pass" in target_argv
  escape_fail = "fail" in target_argv
  escape_result = True if escape_pass and not escape_fail else False if escape_fail and not escape_pass else None
  escape_mod = True if escape_adv and not escape_dis else False if escape_dis and not escape_adv else None
  escape_base = "2d20kh1" if escape_mod == True else "2d20kl1" if escape_mod == False else "1d20"
  escape_skill = None
  skill_name = "Athletics"
  if target:
    escape_skill = target.skills.athletics
    if target.skills.acrobatics.value > target.skills.athletics.value:
      skill_name = "Acrobatics"
      escape_skill = target.skills.acrobatics
  escape_expr = escape_skill.d20(base_adv=escape_mod) if escape_skill else escape_base
  escape_bonus = ''.join([f"+{bonus}" for bonus in args.get("b")])
  escape_roll = vroll(f"{escape_expr}{escape_bonus}")
  escape_success = escape_roll.total >= shove_roll.total if escape_result is None else escape_result
  if target and effect_name and not escape_success:
    target.add_effect(effect_name, effect_args)
  escape_message = "Automatic Pass!" if escape_result == True else "Automatic Fail!" if escape_result == False else f"{escape_roll}; {'Success!' if escape_success else 'Failure!'}"
  fields += f"""-f "{target.name if target else target_name}|**{skill_name}**: {escape_message}
{f"**Effect**: {effect_name}" if effect_name and not escape_success else ""}" """
</drac2>
-title "{{name}} attempts to Shove!"
-f "{{name}}|**Athletics**: {{shove_roll}}"
{{fields}}
-f "Effect|Using the Attack action, you can make a special melee attack to shove a creature, either to knock it prone or push it away from you. If you're able to make multiple attacks with the Attack action, this attack replaces one of them.
The target must be no more than one size larger than you and must be within your reach. Instead of making an attack roll, you make a Strength (Athletics) check contested by the target's Strength (Athletics) or Dexterity (Acrobatics) check (the target chooses the ability to use). You succeed automatically if the target is incapacitated. If you succeed, you either knock the target prone or push it 5 feet away from you."
-footer "Grappling"
-color <color>