multiline
<drac2>
commands = ""

argv = &ARGS&
args = argparse(argv)

name = args.last("name")

spells = args.get("spell") or [name]
dc = args.last("dc", None)
attackBonus = args.last("attackBonus", None)
castingMod = args.last("castingMod", None)
level = args.last("level", None)

cc_name = args.last("cc", name)
cc_min = args.last("min", "0")
cc_max = args.last("max", "1")
cc_value = args.last("value", cc_max)
cc_type = args.last("type", "default")
cc_reset = args.last("reset", "none")

SPELLS = load_json(get_gvar("de308fc5-3fdc-4381-b90e-10161d78c0d2"))

options = []
for spell in spells:
  exact_match = None
  partial_matches = []
  for spell_name, spell_id in SPELLS.items():
    if spell == spell_name:
      exact_match = (spell_name, spell_id)
      break
    elif spell.lower() in spell_name.lower():
      partial_matches = partial_matches + [(spell_name, spell_id)]
  options += [exact_match] if exact_match else partial_matches

if not options:
  commands += f"""!embed -title "Add Spell Action" -desc "Unable to find a spell matching: {", ".join(spells)}" -footer "!homebrew spell | kbsletten#5710"
"""
else:
  commands += f"""!embed -title "Add Spell Action" -desc "Adding Spell Action: {cc_name}"
"""
  commands += f"""!customcounter create "{cc_name}" -min {cc_min} -max {cc_max} -value {cc_value} -type {cc_type} -reset {cc_reset}
"""
  for spell_name, spell_id in options:
    action_name = f"{spell_name} ({cc_name})" if spell_name != cc_name else spell_name
    overrides = ""
    if dc:
      overrides += f"""    dc: {dc}
"""
    if attackBonus:
      overrides += f"""    attackBonus: {attackBonus}
"""
    if castingMod:
      overrides += f"""    castingMod: {castingMod}
"""
    if level:
      overrides += f"""    level: {level}
"""
    commands += f"""!action import name: "{action_name}"
automation:
  - type: counter
    counter: "{cc_name}"
    amount: "1"
  - type: spell
    id: {spell_id}
{overrides}_v: 2
proper: true
verb: casts
"""

</drac2>
{{commands}}