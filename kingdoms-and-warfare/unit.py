embed
<drac2>
args = argparse(&ARGS&)
init = combat()

target = init.get_combatant(args.last("t")) if init and args.last("t") else None
target_name = target.name if target else ""
target_notes = target.note.split(" | ") if target and target.note else []
target_attack = int(args.last("atk", ([x for x in target_notes if x.startswith("Attack: ")] + ["Attack: +0"])[0][len("Attack: "):]))
target_defense = int(args.last("def", ([x for x in target_notes if x.startswith("Defense: ")] + ["Defense: 10"])[0][len("Defense: "):]))
target_power = int(args.last("pow", ([x for x in target_notes if x.startswith("Power: ")] + ["Power: +0"])[0][len("Power :"):]))
target_toughness = int(args.last("tou", ([x for x in target_notes if x.startswith("Toughness: ")] + ["Toughness: 10"])[0][len("Toughness: "):]))
target_morale = int(args.last("mor", ([x for x in target_notes if x.startswith("Morale: ")] + ["Morale: 0"])[0][len("Morale: "):]))
target_command = int(args.last("com", ([x for x in target_notes if x.startswith("Command: ")] + ["Command: 0"])[0][len("Command: "):]))
target_damage = int(args.last("dam", ([x for x in target_notes if x.startswith("Damage: ")] + ["Damage: 1"])[0][len("Damage: "):]))

notes = [x for x in target_notes if not any(x.startswith(pre) for pre in ["Attack: ", "Defense: ", "Power: ", "Toughness: ", "Morale: ", "Command: ", "Damage: "])] + [
  f"""Attack: {"+" if target_attack > 0 else ""}{target_attack}""",
  f"""Defense: {target_defense}""",
  f"""Power: {"+" if target_power > 0 else ""}{target_power}""",
  f"""Toughness: {target_toughness}""",
  f"""Morale: {target_morale}""",
  f"""Command: {"+" if target_command > 0 else ""}{target_command}""",
  f"""Damage: {target_damage}"""
]

if target:
  target.set_note(" | ".join(notes))

</drac2>
-title "{{target_name}}"
-f "Attack|{{"+" if target_attack >= 0 else ""}}{{target_attack}}|inline"
-f "Defense|{{target_defense}}|inline"
-f "Power|{{"+" if target_power >= 0 else ""}}{{target_power}}|inline"
-f "Toughness|{{target_toughness}}|inline"
-f "Morale|{{target_morale}}|inline"
-f "Command|{{"+" if target_command >= 0 else ""}}{{target_command}}|inline"
-f "Damage|{{target_damage}}|inline"
-footer "!unit | kbsletten#5710"
