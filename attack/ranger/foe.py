embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if argv else ""

cc = "Favored Foe"

char = character()
ranger_level = char.levels.get("Ranger") if char else 0
char_has_cc = char.cc_exists(cc) if char else False
char_cc_val = char.get_cc(cc) if char_has_cc else 0

init = combat()
me = init.me if init else None

name = me.name if me else char.name if char else name

title = f"{char.name if char else name} marks a Favored Foe"
fields = ""
cc_used = ""
target_info = ""

if command == "help":
  title = "Favored Foe"
  fields = """-f "Effect|When you hit a creature with an attack roll, you can call on your mystical bond with nature to mark the target as your favored enemy for 1 minute or until you lose your concentration (as if you were concentrating on a spell).
The first time on each of your turns that you hit the favored enemy and deal damage to it, including when you mark it, you can increase that damage by 1d4.
You can use this feature to mark a favored enemy a number of times equal to your proficiency bonus, and you regain all expended uses when you finish a long rest.
This feature’s extra damage increases when you reach certain levels in this class: to 1d6 at 6th level and to 1d8 at 14th level." """
elif char_has_cc:
  target_name = args.last("t")
  target = init.get_combatant(target_name) if init and target_name else None
  damage_roll = vroll("1d4" if ranger_level < 6 else "1d6" if ranger_level < 14 else "1d8")
  fields += f"""-f "Meta|**Damage**: {damage_roll}" """
  if me and target:
    me.add_effect("Favored Foe", "", concentration=True, duration=10)
    parent = me.get_effect("Favored Foe")
    target.add_effect(f"Favored Foe of {name}", "", parent=parent)
  if target:
    target.damage(damage_roll.consolidated())
    target_info = f"{target.name} {target.hp_str()} (-{damage_roll.total})"
  if char:
    char.mod_cc(cc, -1)
  fields += """-f "Effect|When you hit a creature with an attack roll, you can call on your mystical bond with nature to mark the target as your favored enemy for 1 minute or until you lose your concentration (as if you were concentrating on a spell).
The first time on each of your turns that you hit the favored enemy and deal damage to it, including when you mark it, you can increase that damage by 1d4." """
  fields += f"""-f "{cc}|{char.cc_str(cc) if char_has_cc else "N/A"} (-1)" """
</drac2>
-title "{{title}}"
{{fields}}
-footer "{{target_info if target_info else "Favored Foe | TCoE"}}"