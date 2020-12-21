embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if argv else "help"
cc = "Psyonic Charges"

char = character()
name = char.name if char else name
char_has_cc = char.cc_exists(cc) if char else False
char_cc = char.get_cc(cc) if char_has_cc else 0
char_has_dc = char.cvars["psyDC"] if char and "psyDC" in char.cvars else False
char_dc = char.cvars["psyDC"] if char_has_dc else 10

init = combat()
me = init.me if init else None

title = "Psyonics"
fields = ""
target_info = ""
footer = "Strongholds & Followers"

if command == "amplify":
  title = f"{name} uses Amplify!"
  fields = """-f "Effect|The dragon focuses the power of its mind and wreaths its teeth, claws, and tail in glowing psionic force. For the next minute, all of its melee attacks deal an extra 3d8 psychic damage." """
  if char_cc < 4:
    title = title.replace("uses", "tries to use")
    fields += f"""-f "{cc}|{char.cc_str(cc)}" """
  else:
    char.mod_cc(cc, -4)
    if me:
      me.add_effect("Amplify", "", duration=10, desc="For the next minute, all of your melee attacks deal an extra 3d8 psychic damage.")
    fields += f"""-f "{cc}|{char.cc_str(cc)} (-4)" """
elif command == "distance":
  dc = int(args.last("dc", char_dc))

  title = f"{name} uses Distance!"
  fields += f"""-f "Meta|**DC**: {dc}" """
  
  targets = args.get("t")
  if len(targets) > char_cc:
    title = title.replace("uses", "tries to use")
    fields += f"""-f "{cc}|{char.cc_str(cc)}" """
  else:
    for target_expr in targets:
      target_name, _, target_args = target_expr.partition("|")
      target = init.get_combatant(target_name) if init else None
      if not target:
        continue
      target_save_roll = vroll(target.saves.get("int").d20())
      target_success = target_save_roll.total >= dc
      fields += f"""-f "{target.name}|**INT Save**: {target_save_roll}; {"Success!" if target_success else "Failure!"}" """
    fields += """-f "Effect|Space contorts and twists. Choose any number of targets the dragon can see within 30 feet. Each target must succeed on an Intelligence saving throw or be pushed back 30 feet." """
    char.mod_cc(cc, -len(targets))
    fields += f"""-f "{cc}|{char.cc_str(cc)} (-{len(targets)})" """
elif command == "flay":
  dc = int(args.last("dc", char_dc))
  number = int(args.last("n", 1))

  if number > char_cc:
    title = title.replace("uses", "tries to use")
    fields += f"""-f "{cc}|{char.cc_str(cc)}" """
  else:
    damage_roll = vroll(f"{number}d6")

    title = f"{name} uses Flay!"
    fields += f"""-f "Meta|**DC**: {dc}
  **Damage**: {damage_roll}" """
    
    if number > char_cc:
      title = title.replace("uses", "tries to use")
      fields += f"""-f "{cc}|{char.cc_str(cc)}" """
      break

    for target_expr in args.get("t"):
      target_name, _, target_args = target_expr.partition("|")
      target = init.get_combatant(target_name) if init else None
      if not target:
        continue
      target_save_roll = vroll(target.saves.get("int").d20())
      target_success = target_save_roll.total >= dc
      target_damage = damage_roll.consolidated()
      if target_success:
        target_damage = f"({target_damage})/2"
      target_damage_info = target.damage(target_damage)['damage']
      fields += f"""-f "{target.name}|**INT Save**: {target_save_roll}; {"Success!" if target_success else "Failure!"}
  {target_damage_info}" """
      target_info += f"{target.name} {target.hp_str()}"
    fields += """-f "Effect|Space contorts and twists. Choose any number of targets the dragon can see within 30 feet. Each target must succeed on an Intelligence saving throw or be pushed back 30 feet." """
    char.mod_cc(cc, -number)
    fields += f"""-f "{cc}|{char.cc_str(cc)} (-{number})" """
else:
  fields += f"""-f "Getting Started|To add a CC run the following command depending on the size:
`!cc create \\"{cc}\\" -min 0 -max 8 -reset long -resetby 1d4 -type bubble`
Make sure to also set your Psyonic Save DC:
`!cvar \\"psyDC\\" 13` " """
  if char_has_cc:
    fields += f"""-f "{cc}|{char.cc_str(cc)}" """
  if char_has_dc:
    fields += f"""-f "Psyonic Save DC|{char_dc}" """
</drac2>
-title "{{title}}"
{{fields}}
-footer "{{target_info if target_info else footer}}"
-color <color> -thumb <image>