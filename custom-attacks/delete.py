embed
<drac2>
argv = &ARGS&
index = 2

saved_json = load_json(get("_customAttacks", "{}"))

monster_name = argv[0] if argv else None
monster_options = [key for key in saved_json.keys() if monster_name.lower() in key.lower()]
monster_name = monster_options[0] if monster_options else monster_name

attack_name = argv[1] if argv and len(argv) > 1 else None
attack_options = [key for key in saved_json[monster_name].keys() if attack_name.lower() in key.lower()] if monster_name in saved_json else None
attack_name = attack_options[0] if attack_options else attack_name

json = {}
for name, attacks in saved_json.items():
  if name != monster_name:
    json[name] = attacks
    continue
  monster = {}
  for attack, automation in attacks.items():
    if attack != attack_name:
      monster[attack] = automation
  if monster.keys():
    json[name] = monster

fields = ""
for name in json.keys():
  attacks = "\n".join(json[name].keys())
  fields += f"""-f "{name}|{attacks}|inline" """

set_uvar("_customAttacks", dump_json(json))
</drac2>
-title "Deleting attack {{attack_name}} on {{monster_name}}!"
{{fields}}
-footer "!custom_attack delete | kbsletten#5710"