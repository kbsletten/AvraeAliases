embed
<drac2>
argv = &ARGS&
args = argparse(argv)
command = argv[0] if argv else "help"
slot_level = int(args.last("l", 0))

cc = "Eldritch Cannon"

char = character()
artificer_level = char.levels.get("Artificer") if char else 0
char_has_cc = char.cc_exists(cc) if char else False
char_cc_val = char.get_cc(cc) if char_has_cc else 0
char_spells = char.spells if char else None
char_has_slot = char.get_slots(slot_level) if char and slot_level else False

init = combat()
me = init.me if init else None

name = me.name if me else char.name if char else name

title = "Eldritch Cannon"
fields = ""

if command == "summon":
  title = f"{name} summons an Eldritch Cannon"
  fields += f"""-f "Script|`!i add 0 \\"{name}'s Eldritch Cannon\\" -ac 18 -hp {artificer_level*5} -immune poison -immune psychic -p {me.init if me else 0}`" """
  fields += """-f "Effect|You've learned how to create a magical cannon. Using woodcarver’s tools or smith’s tools, you can take an action to magically create a Small or Tiny eldritch cannon in an unoccupied space on a horizontal surface within 5 feet of you. A Small eldritch cannon occupies its space, and a Tiny one can be held in one hand.
Once you create a cannon, you can’t do so again until you finish a long rest or until you expend a spell slot to create one. You can have only one cannon at a time and can’t create one while your cannon is present.
The cannon is a magical object. Regardless of size, the cannon has an AC of 18 and a number of hit points equal to five times your artificer level. It is immune to poison damage and psychic damage. If it is forced to make an ability check or a saving throw, treat all its ability scores as 10 (+0). If the mending spell is cast on it, it regains 2d6 hit points. It disappears if it is reduced to 0 hit points or after 1 hour. You can dismiss it early as an action." """
  if char_has_slot:
    char.use_slot(slot_level)
    fields += f"""-f "Spell Slots|{char.slot_str(slot_level)} (-1)" """
  elif char_cc_val > 0:
    char.mod_cc(cc, -1)
    fields += f"""-f "{cc}|{char.cc_str(cc)} (-1)" """
  elif artificer_level >= 3:
    title = title.replace("summons", "tries to summon")
    fields = """-f "Error|You don't have any uses of Eldritch Cannon. You regain uses when you take a long rest, or you can use a spell slot with `-l LEVEL` to summon it again." """
  else:
    title = title.replace("summons", "cannot summon")
    fields = """-f "Error|You don't have the Eldritch Cannon feature. It's available to 3rd-level Artillerist. Update your character to have the correct class levels and run `!level artificer artillerist` to set it up." """
elif command == "flame":
  dc = int(args.last("dc", char_spells.dc))
  bonuses = args.get("b")
  damage = args.get("d")
  advantage = args.adv()
  auto_success = "pass" in args
  auto_failure = "fail" in args

  damage_roll = vroll("+".join(["3d8[magical fire]"] + damage))

  for target_expr in args.get("t"):
    target_name, _, target_args = target_expr.partition("|")

    target_bonuses = target_args.get("b")
    target_damage = target_args.get("d")
    target_advantage = target_args.adv()
    target_avoid = "avoid" in target_args
    target_auto_success = "pass" in target_args
    target_auto_failure = "fail" in target_args

    total_bonuses = bonuses + target_bonuses
    total_damage = damage + target_damage
    total_advantage = target_advantage or advantage
    total_auto_success = target_auto_success or auto_success
    total_auto_failure = target_auto_failure or auto_failure

    target = init.get_combatant(target_name) if init else None
    if not target:
      continue
    base_adv = True if total_advantage == 1 else False if total_advantage == -1 else None
    target_base = target.saves.get("dex").d20(base_adv=base_adv)
    target_save_roll = vroll("+".join([target_base] + total_bonuses))
elif command == "protect":

    
</drac2>
-title {{title}}
{{fields}}
-footer "Artificer | TCoE"