embed
<drac2>
saved_json = load_json(get("_customAttacks", "{}"))
fields = ""

for monster_name in saved_json.keys():
  attacks = "\n".join(saved_json[monster_name].keys())
  fields += f"""-f "{monster_name}|{attacks}|inline" """
</drac2>
-title "Your Custom Attacks"
{{fields}}
-footer "!custom_attack list | kbsletten#5710"
