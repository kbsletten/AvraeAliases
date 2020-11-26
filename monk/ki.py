embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if len(argv) else "help"

class_name = "Monk"
cc_name = "Ki Points"
ability = "wisdom"

init = combat()

current = character()
name = current.name if current else name
monk_level = current.levels.get(class_name) if current else 0
has_ki = current.cc_exists(cc_name) if current else False
ki_val = current.get_cc(cc_name) if has_ki else 0
ki_max = current.get_cc_max(cc_name) if has_ki else 0
ki_str = current.cc_str(cc_name) if has_ki else "0"
ki_dc = 8 + current.stats.prof_bonus + current.stats.get_mod(ability) if current else 10

title = f"{name} does not have Ki Points"
ki_mod = 0
fields = ""
errors = ""

if monk_level >= 2 and ki_max < monk_level:
  errors += f"""-f "Incorrect Ki|Expected {monk_level} Ki Points but got {ki_max}. Run `!level` or `!ki cc` to fix this." """

if command == "flurry":
  title = f"{name} uses Flurry of Blows"
  fields += """-f "Effect|Immediately after you take the Attack action on your turn, you can spend 1 ki point to make two unarmed strikes as a bonus action." """
  ki_mod = -1
elif command == "patient":
  title = f"{name} uses Patient Defense"
  fields += """-f "Effect|You can spend 1 ki point to take the Dodge action as a bonus action on your turn." """
  ki_mod = -1
elif command == "step":
  title = f"{name} uses Step of the Wind"
  fields += """-f "Effect|You can spend 1 ki point to take the Disengage or Dash action as a bonus action on your turn, and your jump distance is doubled for the turn." """
  ki_mod = -1
elif command == "stun":
  title = f"{name} uses Stunning Strike"
  combatant = init.me if init else None
  stun_effect = combatant.get_effect("Stunning Strike") if combatant and init else None
  targets = args.get("t")
  bonuses = args.get("b")
  if len(targets) <= ki_val:
    for target_expr in targets:
      target_name, _, target_arg = target_expr.partition('|')
      target_argv = target_arg.split(' ')
      target_args = argparse(target_arg)
      target = init.get_combatant(target_name) if init else None
      save_adv = "adv" in target_argv
      save_dis = "dis" in target_argv
      save_pass = "pass" in target_argv
      save_fail = "fail" in target_argv
      save_result = True if save_pass and not save_fail else False if save_fail and not save_pass else None
      save_mod = True if save_adv and not save_dis else False if save_dis and not save_adv else None
      save_base = "2d20kh1" if save_mod == True else "2d20kl1" if save_mod == False else "1d20"
      save_expr = target.saves.get("con").d20(base_adv=save_mod) if target else save_base
      save_bonus = ''.join([f"+{bonus}" for bonus in target_args.get("b") + bonuses])
      save_roll = vroll(f"{save_expr}{save_bonus}")
      save_success = save_roll.total >= ki_dc if save_result is None else save_result
      if combatant and not stun_effect and not save_success:
        on_turn = init.current == combatant
        combatant.add_effect("Stunning Strike", "", duration=1 if on_turn else 0, end=True)
        stun_effect = combatant.get_effect("Stunning Strike")
      if target and not save_success:
        target.add_effect(f"Stunned by {name}", "", parent=stun_effect)
      save_message = "Automatic Pass!" if save_result == True else "Automatic Fail!" if save_result == False else f"{save_roll}; {'Success!' if save_success else 'Failure!'}"
      fields += f"""-f "{target.name if target else target_name}|**CON Save**: {save_message}
{f"**Effect**: Stunned by {name}" if not save_success else ""}" """
      ki_mod -= 1
  fields += f"""-f "Effect|When you hit another creature with a melee weapon attack, you can spend 1 ki point to attempt a stunning strike. The target must succeed on a DC {ki_dc} Constitution saving throw or be stunned until the end of your next turn." """
else:
  title = f"{name} has Ki" if monk_level > 0 else title
  fields += f"""-f "Meta|**Monk Level**: {monk_level}
**Ki Points**: {ki_str}
**Ki Save DC**: {ki_dc}" """
  if monk_level >= 2:
    fields += """-f "Flurry of Blows `!ki flurry`|Immediately after you take the Attack action on your turn, you can spend 1 ki point to make two unarmed strikes as a bonus action." """
    fields += """-f "Patient Defense `!ki patient`|You can spend 1 ki point to take the Dodge action as a bonus action on your turn." """
    fields += """-f "Step of the Wind `!ki step`|You can spend 1 ki point to take the Disengage or Dash action as a bonus action on your turn, and your jump distance is doubled for the turn." """
  if monk_level >= 5:
    fields += f"""-f "Stunning Strike `!ki stun -t TARGET`|When you hit another creature with a melee weapon attack, you can spend 1 ki point to attempt a stunning strike. The target must succeed on a DC {ki_dc} Constitution saving throw or be stunned until the end of your next turn." """
  if monk_level >= 14:
    fields += """-f "Diamond Soul `!ki soul`|Whenever you make a saving throw and fail, you can spend 1 ki point to reroll it and take the second result." """
  if monk_level >= 18:
    fields += """-f "Empty Body `!ki invis`|You can use your action to spend 4 ki points to become invisible for 1 minute. During that time, you also have resistance to all damage but force damage." """
    fields += """-f "Empty Body `!ki astral`|You can spend 8 ki points to cast the astral projection spell, without needing material components. When you do so, you can’t take any other creatures with you." """
if has_ki:
  if ki_val + ki_mod >= 0:
    current.mod_cc(cc_name, ki_mod)
  else:
    title = title.replace("uses", "tries to use")
    fields = f"""-f "Insufficient Ki|This ability uses {str(+ki_mod)} Ki Points. You must take a short rest before you can use this ability again." """
    ki_mod = 0
</drac2>
-title "{{title}}"
{{fields}}
{{errors}}
{{f""" -f "{cc_name}|{current.cc_str(cc_name)}{f" ({ki_mod})" if ki_mod != 0 else ""}" """ if has_ki else ""}}
-color <color>