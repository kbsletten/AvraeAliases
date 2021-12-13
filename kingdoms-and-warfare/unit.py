embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()

search = args.last("unit") if args.last("unit") else argv[0] if argv and not argv[0].startswith("-") else None

units = [unit for name, unit in load_json(get("_warfareUnits", "{}")).items() if search.lower() in name.lower()] if search else []

unit_name = units[0]["name"] if units else "Unnamed Unit"
unit_attack = units[0]["attack"] if units else 0
unit_defense = units[0]["defense"] if units else 10
unit_power = units[0]["power"] if units else 0
unit_toughness = units[0]["toughness"] if units else 10
unit_morale = units[0]["morale"] if units else 0
unit_command = units[0]["command"] if units else 0
unit_size = units[0]["size"] if units else 6
unit_damage = units[0]["damage"] if units else 1
unit_traits = units[0]["traits"] if units else []

target = init.get_combatant(args.last("t")) if init and args.last("t") else None
target_name = target.name if target else ""
target_notes = target.note.split(" | ") if target and target.note else []
target_traits = [effect.name for effect in target.effects] if target else []

target_attack = int(args.last("atk", ([x for x in target_notes if x.startswith("Attack: ")] + [f"Attack: {unit_attack}"])[0][len("Attack: "):]))
target_defense = int(args.last("def", ([x for x in target_notes if x.startswith("Defense: ")] + [f"Defense: {unit_defense}"])[0][len("Defense: "):]))
target_power = int(args.last("pow", ([x for x in target_notes if x.startswith("Power: ")] + [f"Power: {unit_power}"])[0][len("Power :"):]))
target_toughness = int(args.last("tou", ([x for x in target_notes if x.startswith("Toughness: ")] + [f"Toughness: {unit_toughness}"])[0][len("Toughness: "):]))
target_morale = int(args.last("mor", ([x for x in target_notes if x.startswith("Morale: ")] + [f"Morale: {unit_morale}"])[0][len("Morale: "):]))
target_command = int(args.last("com", ([x for x in target_notes if x.startswith("Command: ")] + [f"Command: {unit_command}"])[0][len("Command: "):]))
target_size = int(args.last("size", target.max_hp if target and target.max_hp else unit_size))
target_damage = int(args.last("dam", ([x for x in target_notes if x.startswith("Damage: ")] + [f"Damage: {unit_damage}"])[0][len("Damage: "):]))

notes = [x for x in target_notes if not any(x.startswith(pre) for pre in ["Attack: ", "Defense: ", "Power: ", "Toughness: ", "Morale: ", "Command: ", "Damage: "])] + [
  f"""Attack: {"+" if target_attack >= 0 else ""}{target_attack}""",
  f"""Defense: {target_defense}""",
  f"""Power: {"+" if target_power >= 0 else ""}{target_power}""",
  f"""Toughness: {target_toughness}""",
  f"""Morale: {"+" if target_morale >= 0 else ""}{target_morale}""",
  f"""Command: {"+" if target_command >= 0 else ""}{target_command}""",
  f"""Damage: {target_damage}"""
]

if target:
  target.set_note(" | ".join(notes))
  target.set_maxhp(target_size)
  for trait in unit_traits:
    target.add_effect(trait, "")

traits = "\n".join(f" - {trait}" for trait in unit_traits + [trait for trait in target_traits if trait not in unit_traits]) if unit_traits or target_traits else "(no traits)"

</drac2>
-title "{{target_name or unit_name}}"
-f "Attack|{{"+" if target_attack >= 0 else ""}}{{target_attack}}|inline"
-f "Defense|{{target_defense}}|inline"
-f "Power|{{"+" if target_power >= 0 else ""}}{{target_power}}|inline"
-f "Toughness|{{target_toughness}}|inline"
-f "Morale|{{"+" if target_morale >= 0 else ""}}{{target_morale}}|inline"
-f "Command|{{"+" if target_command >= 0 else ""}}{{target_command}}|inline"
-f "Size|{{target_size}}|inline"
-f "Damage|{{target_damage}}|inline"
-f "Traits|{{traits}}"
-footer "!unit | kbsletten#5710"
