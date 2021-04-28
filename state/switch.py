embed
<drac2>
argv = &ARGS&
new_state = argv[0] if argv else None

char = character()

saved_states = load_json(char.cvars["_state"]) if "_state" in char.cvars else {}
current_state = char.cvars["_currentState"] if "_currentState" in char.cvars else None
json = {
  "hp": { "current": char.hp, "temp": char.temp_hp },
  "ss": {},
  "cc": [{"name": cc.name, "value": cc.value} for cc in char.consumables]
}

for l in range(1, 10):
  json["ss"][f"{l}"] = char.spellbook.get_slots(l)

if current_state:
  saved_states[current_state] = json
  char.set_cvar("_state", dump_json(saved_states))

loaded_state = saved_states[new_state] if saved_states and new_state in saved_states else None

if loaded_state:
  char.set_cvar("_currentState", new_state)
  if "hp" in loaded_state:
    if "current" in loaded_state["hp"]:
      char.set_hp(loaded_state["hp"]["current"])
    if "temp" in loaded_state["hp"]:
      char.set_temp_hp(loaded_state["hp"]["temp"])
  if "ss" in loaded_state:
    for l in range(1, 10):
      if f"{l}" in loaded_state["ss"]:
        char.spellbook.set_slots(l, loaded_state["ss"][f"{l}"])
  if "cc" in loaded_state:
    for cc in loaded_state["cc"]:
      char.set_cc(cc["name"], cc["value"])

</drac2>
-title "Switch States"
{{f"""-f "State Saved!|Saved state: {current_state}" """ if current_state else """-f "Previous State|(not set)" """}
{{f"""-f "State Loaded!|Loaded state: {new_state}" """ if loaded_state else """-f "No Name Provided|`!state switch <NAME (e.g. \\"Side Quest\\")>"` """}}
-f "HP|{{char.hp}}|inline" -f "THP|{{char.temp_hp}}|inline"
{{' '.join([f"""-f "Level {l}|{char.spellbook.get_slots(l)}|inline" """ for l in range(1, 10) if char.spellbook.get_max_slots(l)])}}
{{' '.join([f"""-f "{cc.name}|{cc.value}|inline" """ for cc in char.consumables])}}
-footer "!state switch | kbsletten#5710"
-color <color> -thumb <image>
-t 20
