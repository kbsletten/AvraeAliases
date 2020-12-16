embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()
current = init.current if init else character()
if args.last("as"):
  current = init.get_combatant(args.last("as")) if init else current
name = current.name if current else name

grapple_adv = "adv" in argv
grapple_dis = "dis" in argv
grapple_mod = True if grapple_adv and not grapple_dis else False if grapple_dis and not grapple_adv else None
grapple_base = "2d20kh1" if grapple_mod == True else "2d20kl1" if grapple_mod == False else "1d20"
grapple_expr = current.skills.athletics.d20(base_adv=grapple_mod) if current else grapple_base
grapple_bonus = ''.join([f"+{bonus}" for bonus in args.get("b")])
grapple_roll = vroll(f"{grapple_expr}{grapple_bonus}")

fields = ""
grapple_effect = current.get_effect("Grappling") if current and init else None

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
  escape_success = escape_roll.total >= grapple_roll.total if escape_result is None else escape_result
  if current and init and not grapple_effect and not escape_success:
    current.add_effect("Grappling", "")
    grapple_effect = current.get_effect("Grappling")
  if target and not escape_success:
    target.add_effect(f"Grappled by {name}", "", parent=grapple_effect)
  escape_message = "Automatic Pass!" if escape_result == True else "Automatic Fail!" if escape_result == False else f"{escape_roll}; {'Success!' if escape_success else 'Failure!'}"
  fields += f"""-f "{target.name if target else target_name}|**{skill_name}**: {escape_message}
{f"**Effect**: Grappled by {name}" if not escape_success else ""}" """
</drac2>
-title "{{name}} attempts to Grapple!"
-f "{{name}}|**Athletics**: {{grapple_roll}}"
{{fields}}
-f "Effect|When you want to grab a creature or wrestle with it, you can use the Attack action to make a special melee attack, a grapple. If you're able to make multiple attacks with the Attack action, this attack replaces one of them.
The target of your grapple must be no more than one size larger than you and must be within your reach. Using at least one free hand, you try to seize the target by making a grapple check instead of an attack roll: a Strength (Athletics) check contested by the target's Strength (Athletics) or Dexterity (Acrobatics) check (the target chooses the ability to use). You succeed automatically if the target is incapacitated. If you succeed, you subject the target to the grappled condition. The condition specifies the things that end it, and you can release the target whenever you like (no action required)."
-footer "Grappling"
-color <color>