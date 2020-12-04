embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = "&1&"
spell_level = int(command)
unholy = "undead" in argv or "fiend" in argv
critical = "crit" in argv

current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

paladin_level = int(get("PaladinLevel", 0))
has_slot = paladin_level > 2 and spell_level > 0 and spell_level < 5 and get_slots(spell_level) > 0

title = "Invalid alias"
description = "You do not have this ability."
fields = ""
target_info = ""

damage_roll = vroll(f"{(1 + spell_level + (1 if unholy else 0)) * (2 if critical else 1)}d8[magical radiant]")

if command == "help":
  title = "Divine Smite"
  description = """Starting at 2nd level, when you hit a creature with a melee weapon attack, you can expend one spell slot to deal radiant damage to the target, in addition to the weapon’s damage. The extra damage is 2d8 for a 1st-level spell slot, plus 1d8 for each spell level higher than 1st, to a maximum of 5d8. The damage increases by 1d8 if the target is an undead or a fiend, to a maximum of 6d8."""
  fields = """-f "Usage|!smite LEVEL [-t TARGET] [undead|fiend] [crit]" """
elif has_slot:
    title = f"{combatant_name} uses Divine Smite"
    description = ""
    fields = f"""-f "Meta|**Damage{" (CRIT!)" if critical else ""}**: {damage_roll}" """
    use_slot(spell_level)
    target_name = args.last("t")
    target = current_combat.get_combatant(target_name) if current_combat and target_name else None
    if target:
      damage = damage_roll.consolidated()
      target_damage = target.damage(damage)["damage"]
      fields += f"""-f "{target.name}|{target_damage}" """
      target_info = f"{target.name} {target.hp_str()}\n"
    fields+= f"""
-f "Effect|When you hit a creature with a melee weapon attack, you can expend one spell slot to deal extra radiant damage to the target in addition to the weapon's damage."
"""
    if unholy:
      fields += f"""-f "Bonus Damage|The damage increases by 1d8 if the target is an undead or a fiend, to a maximum of 6d8." """
elif paladin_level >= 2:
  title = f"{combatant_name} tries to use Divine Smite"
  description = "You must finish a long rest before you can use this ability again."
</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-f "Spell Slots|{slots_str(spell_level)}" """ if has_slot else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Paladin | PHB 85" """}}
-color <color> -thumb <image>
