embed
<drac2>
argv = &ARGS&
uvar = "muse"
abilities = load_json(get(uvar, "{}"))

ability_name = argv[0] if argv else ""
old_value = abilities[ability_name] if ability_name in abilities else ""
ability_expr = argv[1:] if argv else []

if ability_name and ability_expr:
  abilities[ability_name] = ability_expr

set_uvar(uvar, dump_json(abilities))
</drac2>
-tile "!muse set - save for later"
{{f"""-f "Abilities|{", ".join(abilities.keys())}" """ if abilities else ""}}
{{f"""-f "Ability|{ability_name}" """ if ability_name else ""}}
{{f"""-f "Old Value|{" ".join(old_value)}" """ if old_value else ""}}
{{f"""-f "New Value|{" ".join(ability_expr)}" """ if ability_expr else ""}}
-color <color>