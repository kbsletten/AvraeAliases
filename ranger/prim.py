embed
<drac2>
argv = &ARGS&
args = argparse(argv)

char = character()
name = char.name if char else name
ranger_level = char.levels.get("Ranger") if char else 0
level = int(args.last("l", "1"))
spell_slots = char.spellbook.get_slots(level) if char else 0

init = combat()
me = init.me if init else None

title = "[name] uses Primeval Awareness".replace("[name]", name)
fields = """-f "Effect|Starting at 3rd level, you can use your action and expend one ranger spell slot to focus your awareness on the region around you. For 1 minute per level of the spell slot you expend, you can sense whether the following types of creatures are present within 1 mile of you (or within up to 6 miles if you are in your favored terrain): aberrations, celestials, dragons, elementals, fey, fiends, and undead. This feature doesn’t reveal the creatures’ location or number." """

if ranger_level < 3:
  title.replace("uses", "cannot use")
elif spell_slots < 1:
  title.replace("uses", "tries to use")
else:
  char.spellbook.use_slot(level)
  if me:
    me.add_effect("Primeval Awareness", "", duration=level*10, desc="You can sense whether the following types of creatures are present within 1 mile of you (or within up to 6 miles if you are in your favored terrain): aberrations, celestials, dragons, elementals, fey, fiends, and undead. This feature doesn’t reveal the creatures’ location or number.")
  fields += f"""-f "Spell Slots|{char.spellbook.slots_str(level)} (-1)" """

</drac2>
-title "{{title}}"
{{fields}}
-footer "Primeval Awareness | PHB 92"