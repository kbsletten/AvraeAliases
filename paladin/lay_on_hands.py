embed
<drac2>
args = argparse(&ARGS&)
target_name = args.last("t", "self")
command = "&1&"

current_character = character()
current_combat = combat()
current_combatant = current_combat.get_combatant(name) if current_combat else None
combatant_name = current_combatant.name if current_combatant else name

paladin_level = int(get("PaladinLevel", 0))

cc = "Lay on Hands Pool"
cc_ex = cc_exists(cc)
cc_value = (cc_ex and get_cc(cc)>0)

title = "Invalid alias"
description = "You do not have this ability."
fields = ""
target_info = ""

if command == "help":
  title = "Lay on Hands"
  description = """Your blessed touch can heal wounds. You have a pool of healing power that replenishes when you take a long rest. With that pool, you can restore a total number of hit points equal to your paladin level × 5.
As an action, you can touch a creature and draw power from the pool to restore a number of hit points to that creature, up to the maximum amount remaining in your pool.
Alternatively, you can expend 5 hit points from your pool of healing to cure the target of one disease or neutralize one poison affecting it. You can cure multiple diseases and neutralize multiple poisons with a single use of Lay on Hands, expending hit points separately for each one.
This feature has no effect on undead and constructs.
"""
elif cc_value:
  hp = int(command)
  effects = args.get("effect")
  target = None
  if current_combat:
    target = current_combat.get_combatant(target_name) if target_name != 'self' else current_combatant
    hp = min(hp, target.max_hp - target.hp)
    effects = [target.get_effect(name).name for name in effects if target.get_effect(name) is not None] if target else effects
  elif target_name == "self":
    hp = min(hp, current_character.max_hp - current_character.hp)
  cost = hp + len(effects) * 5
  if get_cc(cc) < cost:
    title = f"{combatant_name} tries to use Lay on Hands"
    description = "You must finish a long rest before you can use this ability again."
  else:
    title = f"{combatant_name} uses Lay on Hands"
    description = ""
    fields = f"""-f "Meta|**Healing**: {hp}
{f"**Effects**: {', '.join(effects)}" if len(effects) else ""}"
"""
    mod_cc(cc,-cost)
    if target:
      target.modify_hp(hp, overflow=False)
      target_info = f"{target.name} {target.hp_str()}"
      for effect in effects:
        target.remove_effect(effect)
    elif target_name == "self":
      current_character.modify_hp(hp, overflow=False)
      if hp > 0:
        target_info = f"{combatant_name}: {current_character.hp_str()} (+{hp})"
    fields+= f"""
-f "Effect|As an action, you can touch a creature and draw power from the pool to restore a number of hit points to that creature, up to the maximum amount remaining in your pool."
"""
elif cc_ex:
  title = f"{combatant_name} tries to use Lay on Hands"
  description = "You must finish a long rest before you can use this ability again."
elif paladin_level > 0:
  description = f"""Missing a **c**ustom **c**ounter named `{cc}`. See `!help cc create` for how to make one manually, or run `!cc create "{cc}" -reset long -min 0 -max {proficiency_bonus} -type bubble`."""

</drac2>
-title "{{title}}"
{{f"""-desc "{description}" """ if description else ""}}
{{fields}}
{{f"""-f "{cc}|{cc_str(cc)}" """ if cc_value else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Paladin | PHB 84" """}}
-color <color> -thumb <image>
