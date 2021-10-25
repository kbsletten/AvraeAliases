embed
<drac2>
argv = &ARGS&
args = argparse(argv)
init = combat()

unit = init.current if init.current.controller == ctx.author.id else ([x for x in init.combatants if x.controller == ctx.author.id] + [None])[0]
unit_name = unit.name if unit else ""
unit_notes = unit.note.split(" | ") if unit and unit.note else []
unit_attack = int(args.last("atk", ([x for x in unit_notes if x.startswith("Attack: ")] + ["Attack: +0"])[0][len("Attack: "):]))
unit_defense = int(args.last("def", ([x for x in unit_notes if x.startswith("Defense: ")] + ["Defense: 10"])[0][len("Defense: "):]))
unit_power = int(args.last("pow", ([x for x in unit_notes if x.startswith("Power: ")] + ["Power: +0"])[0][len("Power :"):]))
unit_toughness = int(args.last("tou", ([x for x in unit_notes if x.startswith("Toughness: ")] + ["Toughness: 10"])[0][len("Toughness: "):]))
unit_morale = int(args.last("mor", ([x for x in unit_notes if x.startswith("Morale: ")] + ["Morale: 0"])[0][len("Morale: "):]))
unit_command = int(args.last("com", ([x for x in unit_notes if x.startswith("Command: ")] + ["Command: 0"])[0][len("Command: "):]))
unit_damage = int(args.last("dam", ([x for x in unit_notes if x.startswith("Damage: ")] + ["Damage: 1"])[0][len("Damage: "):]))

unit_effects = [e.name for e in unit.effects] if unit else []
unit_art = "Artillery" in unit_effects
unit_cav = "Cavalry" in unit_effects
unit_inf = "Infantry" in unit_effects

target = init.get_combatant(args.last("t")) if init and args.last("t") else None
target_name = target.name if target else "Meta"
target_notes = target.note.split(" | ") if target and target.note else []
target_attack = int(args.last("atk", ([x for x in target_notes if x.startswith("Attack: ")] + ["Attack: +0"])[0][len("Attack: "):]))
target_defense = int(args.last("def", ([x for x in target_notes if x.startswith("Defense: ")] + ["Defense: 10"])[0][len("Defense: "):]))
target_power = int(args.last("pow", ([x for x in target_notes if x.startswith("Power: ")] + ["Power: +0"])[0][len("Power :"):]))
target_toughness = int(args.last("tou", ([x for x in target_notes if x.startswith("Toughness: ")] + ["Toughness: 10"])[0][len("Toughness: "):]))
target_morale = int(args.last("mor", ([x for x in target_notes if x.startswith("Morale: ")] + ["Morale: 0"])[0][len("Morale: "):]))
target_command = int(args.last("com", ([x for x in target_notes if x.startswith("Command: ")] + ["Command: 0"])[0][len("Command: "):]))
target_damage = int(args.last("dam", ([x for x in target_notes if x.startswith("Damage: ")] + ["Damage: 1"])[0][len("Damage: "):]))

target_effects = [e.name for e in target.effects] if target else []
target_inf = "Infantry" in target_effects
target_react = "Reaction" not in target_effects
target_dim = "Diminished" in target_effects
target_dr = "Damage Resistant" in target_effects
target_rel = "Relentless" in target_effects
target_ttd = "To the Death" in target_effects
target_stal = "Stalwart" in target_effects

fields = ""
target_info = ""

attack_adv = "adv" in argv or "aadv" in argv
attack_dis = "dis" in argv or "adis" in argv
attack_base = "2d20kh1" if attack_adv and not attack_dis else "2d20kl1" if attack_dis and not attack_adv else "1d20"
attack_roll = vroll("+".join([attack_base, str(unit_attack)] +
  args.get("a") +
  (["-2[fort]"] if any([fort in target_effects for fort in ["City Wall"]]) else [])
))

power_adv = "adv" in argv or "padv" in argv
power_dis = "dis" in argv or "pdis" in argv
if target_stal and target_dim and (unit_inf or unit_cav):
  power_dis = True
  fields += """-f "Stalwart|While this unit is diminished, opposed infantry and cavalry units have disadvantage on Power tests against it." """
  
power_base = "2d20kh1" if power_adv and not power_dis else "2d20kl1" if power_dis and not power_adv else "1d20"
power_roll = vroll("+".join([power_base, str(unit_power)] +
  args.get("p") +
  (["2[fort]"] if unit_art and any([fort in unit_effects for fort in ["City Wall"]]) else [])
))

rolls = f"""
**Attack**: {attack_roll}
**Power**: {power_roll}
"""

damage = 0
if target:
  hit = attack_roll.result.crit == 1 or attack_roll.result.crit != 2 and attack_roll.total >= target_defense
  casualties = power_roll.total >= target_toughness
  rolls = f"""
**Attack**: {attack_roll}
{f"**Power**: {power_roll}" if hit else "**Miss!**"}
"""
  if hit:
    if target_dr:
      fields += """-f "Damage Resistant|Successful Attack tests against this unit inflict no casualties. Successful Power tests inflict casualties normally." """
    else:
      damage += 2 if attack_roll.result.crit == 1 else 1
    if casualties:
      damage += unit_damage
  if damage:
    target.mod_hp(-damage)
    target_info += f"""{target.name} {target.hp_str()} (-{damage})
"""
    if target.hp <= target.max_hp / 2:
      if not target_dim:
        morale_roll = vroll("+".join(["1d20", str(target_morale)] + 
          (["2[fort]"] if any([fort in target_effects for fort in ["City Wall"]]) else [])
        ))
        rolls += f"""**Diminished**: {morale_roll}
"""
        target.add_effect("Diminished", "")
        if morale_roll.total < 13:
          target.mod_hp(-1)
          target_info += f"""{target.name} {target.hp_str()} (-1)
"""
          fields += """-f "Diminished|A unit is diminished when its current casualties are half or less than its starting casualties. The first
time a unit becomes diminished, it must succeed on a DC 13 Morale test or suffer another casualty. Each unit does this only once per battle." """
    if target.hp <= 0:
      if target_react and target_rel:
        power_roll = vroll(f"1d20+{target_power}")
        rolls += f"""**Relentless**: {power_roll}
"""
        target.add_effect("Reaction", "", duration=0)
        if power_roll.total >= 13:
          target.set_hp(1)
          fields += """-f "Relentless|As a reaction to suffering a casualty that would cause this unit to break, this unit makes a DC 13 Power test. On a success, this unit does not break and has 1 casualty." """
          target_info += f"""{target.name} {target.hp_str()}
"""
    if target.hp <= 0:
      if target_ttd:
        unit.mod_hp(-1)
        fields += f"""-f "To the Death|If this unit breaks as a result of an opposed unit’s Attack or Power test, the attacking unit suffers 1 casualty." """
        target_info += f"""{unit.name} {unit.hp_str()} (-1)
"""
    if target.hp > 0 and unit_cav and target_inf and damage > 0:
      command_roll = vroll(f"1d20+{target_command}")
      rolls += f"""**Set for Charge**: {command_roll}"""
      fields += """-f "Set for Charge|As a reaction to suffering a casualty from a cavalry or aerial unit, this unit makes a DC 13 Command
test. On a success, the attacking unit suffers 1 casualty." """
      if command_roll.total >= 13:
        unit.mod_hp(-1)
        target_info += f"""{unit.name} {unit.hp_str()} (-1)
"""
</drac2>
-title "{{unit_name}} Attacks!"
-f "{{target_name}}|{{rolls}}"
{{fields}}
-footer "{{target_info if target_info else "!unit attack | kbsletten#5710"}}"
