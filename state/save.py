embed
<drac2>
argv = &ARGS&

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

</drac2>
-title "Save State"
{{f"""-f "State Saved!|Saved state: {current_state}" """ if current_state else """-f "Current State|(not set)" """}}
-footer "!state save | kbsletten#5710"
-color <color> -thumb <image>
-t 20
