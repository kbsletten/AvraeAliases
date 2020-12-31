embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if argv else "help"

cc = "Wild Shape"

char = character()
spellbook = char.spellbook if char else None
druid_level = char.levels.get("Druid") if char else 0
has_wildshape = char.cc_exists(cc) if char else False
wildshape = char.get_cc(cc) if has_wildshape else 0
name = char.name if char else name

init = combat()
me = init.me if init else None
spellbook = me.spellbook if me else spellbook
name = me.name if me else name

spirit_name = args.last("name", "a Wildfire Spirit")

title = "Circle of Wildfire"
fields = ""

adv = True if "adv" in args else False if "dis" in args else None
auto = True if "pass" in args else False if "fail" in args else None

if command == "summon":
  title = f"{name} summons {spirit_name}"
  dc = int(args.last("dc", spellbook.dc if spellbook else 10))
  damage_roll = vroll("2d6[magical fire]")
  fields += f"""-f "Meta|**DC**: {dc}
**Damage**: {damage_roll}
DEX save" """
  if wildshape:
    for target_expr in args.get("t"):
      target_name, _, target_arg = target_expr.partition("|")
      target_args = argparse(target_arg)
      target = init.get_combatant(target_name) if init else None

      if not target:
        continue
      
      target_adv = True if "adv" in target_args else False if "dis" in target_args else None
      target_auto = True if "pass" in target_args else False if "fail" in target_args else None

      total_adv = adv if target_adv is None else target_adv
      total_auto = auto if target_auto is None else target_auto

      target_save_roll = vroll("+".join([target.saves.get("dex").d20(base_adv=total_adv)] + args.get("b") + target_args.get("b")))
      save_success = target_save_roll.total > dc if total_auto is None else total_auto

      save_message = "Automatic Pass!" if total_auto == True else "Automatic Fail!" if total_auto == False else f"{save_roll}; {'Success!' if save_success else 'Failure!'}"
      fields += f"""-f "{target.name}|**DEX Save**: {save_message}" """
  char.mod_cc(cc, -1)
  fields += f"""-f "{cc}|{char.cc_str(cc)}" """
else:
  title = "Circle of Wildfire"

</drac2>
-title "{{title}}"
{{fields}}
-footer "Wildfire Druid | TCoE"
