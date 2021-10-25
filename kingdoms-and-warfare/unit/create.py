embed
<drac2>
args = argparse(&ARGS&)

unit_name = args.last("name", "Unnamed Unit")
unit_attack = int(args.last("atk", 0))
unit_defense = int(args.last("def", 10))
unit_power = int(args.last("pow", 0))
unit_toughness = int(args.last("tou", 10))
unit_morale = int(args.last("mor", 0))
unit_command = int(args.last("com", 0))
unit_size = int(args.last("size", 6))
unit_damage = int(args.last("dam", 1))
unit_traits = args.get("trait")

unit_json = {
  "name": unit_name,
  "attack": unit_attack,
  "defense": unit_defense,
  "power": unit_power,
  "toughness": unit_toughness,
  "morale": unit_morale,
  "command": unit_command,
  "size": unit_size,
  "damage": unit_damage,
  "traits": unit_traits
}

units = load_json(get("_warfareUnits", "{}"))
units[unit_name] = unit_json
set_uvar("_warfareUnits", dump_json(units))

</drac2>
-title "Defining unit {{unit_name}}"
-f "Attack|{{"+" if unit_attack >= 0 else ""}}{{unit_attack}}|inline"
-f "Defense|{{unit_defense}}|inline"
-f "Power|{{"+" if unit_power >= 0 else ""}}{{unit_power}}|inline"
-f "Toughness|{{unit_toughness}}|inline"
-f "Morale|{{"+" if unit_morale >= 0 else ""}}{{unit_morale}}|inline"
-f "Command|{{"+" if unit_command >= 0 else ""}}{{unit_command}}|inline"
-f "Size|{{unit_size}}|inline"
-f "Damage|{{unit_damage}}|inline"
-f "Traits|{{"\n".join(f" - {trait}" for trait in unit_traits)}}"
-footer "!unit create | kbsletten#5710"
