embed
<drac2>
char = character()

saved_states = load_json(char.cvars["_state"]) if "_state" in char.cvars else None
current_state = char.cvars["_currentState"] if "_currentState" in char.cvars else None
json = {
  "hp": { "current": char.hp, "temp": char.temp_hp },
  "ss": {},
  "cc": [{"name": cc.name, "value": cc.value} for cc in char.consumables]
}

for l in range(1, 10):
  json["ss"][f"{l}"] = char.spellbook.get_slots(l)

</drac2>
-title "Save/Load State"
-f "Saved States|{{', '.join(saved_states.keys()) if saved_states else '(no saved states)'}}"
-f "Current State|{{current_state or '(not set)'}}"
-f "HP|{{char.hp}}|inline" -f "THP|{{char.temp_hp}}|inline"
{{' '.join([f"""-f "Level {l}|{char.spellbook.get_slots(l)}|inline" """ for l in range(1, 10) if char.spellbook.get_max_slots(l)])}}
{{' '.join([f"""-f "{cc.name}|{cc.value}|inline" """ for cc in char.consumables])}}
-footer "!state | kbsletten#5710"
-color <color> -thumb <image>
-t 20
