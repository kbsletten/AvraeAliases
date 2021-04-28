embed
<drac2>
argv = &ARGS&
new_state = argv[0] if argv else None

char = character()

saved_states = load_json(char.cvars["_state"]) if "_state" in char.cvars else {}
json = {
  "hp": { "current": char.hp, "temp": char.temp_hp },
  "ss": {},
  "cc": [{"name": cc.name, "value": cc.value} for cc in char.consumables]
}

for l in range(1, 10):
  json["ss"][f"{l}"] = char.spellbook.get_slots(l)

if new_state:
  char.set_cvar("_currentState", new_state)
  saved_states[str(new_state)] = json
  char.set_cvar("_state", dump_json(saved_states))

</drac2>
-title "Create New State"
{{f"""-f "State Created!|Created new state: {new_state}" """ if new_state else """-f "No Name Provided|`!state new <NAME (e.g. \\"Side Quest\\")>"` """}}
-footer "!state new | kbsletten#5710"
-color <color> -thumb <image>
-t 20
