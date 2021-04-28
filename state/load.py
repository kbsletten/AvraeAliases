embed
<drac2>
argv = &ARGS&
new_state = argv[0] if argv else None

char = character()

saved_states = load_json(char.cvars["_state"]) if "_state" in char.cvars else None
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
-title "Load State"
{{f"""-f "State Loaded!|Loaded state: {new_state}" """ if loaded_state else """-f "No Name Provided|`!state load <NAME (e.g. \\"Side Quest\\")>"` """}}
-f "HP|{{char.hp}}|inline" -f "THP|{{char.temp_hp}}|inline"
{{' '.join([f"""-f "Level {l}|{char.spellbook.get_slots(l)}|inline" """ for l in range(1, 10) if char.spellbook.get_max_slots(l)])}}
{{' '.join([f"""-f "{cc.name}|{cc.value}|inline" """ for cc in char.consumables])}}
-footer "!state load | kbsletten#5710"
-color <color> -thumb <image>
-t 20
